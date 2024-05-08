from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from bilan.models import Bilan
from backoffice.models import AdminBond

from .models import Bond, BondPortofolio
from .serializers import BondSerializer, BondPortofolioSerializer

# initializing packages 
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import math
import json
# Create your views here.

class BondPortofolioViewset(viewsets.ModelViewSet):
    queryset = BondPortofolio.objects.filter(deleted=False)
    serializer_class = BondPortofolioSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = BondPortofolio.objects.filter(user=user, deleted=False)
        return queryset

class BondsViewset(viewsets.ModelViewSet):
    serializer_class = BondSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Bond.objects.filter(user=user, deleted=False)
        return queryset
    
 
    def create(self, request, *args, **kwargs):

        try:
            user = request.user
            admin_bond = AdminBond.objects.get(isin=request.data['isin'])
            bilan, _ = Bilan.objects.get_or_create(user=user)
            portofolio, _ = BondPortofolio.objects.get_or_create(user=user, defaults={'name': 'My Portfolio', 'bilan': bilan})

            request.data["user"] = user.id
            request.data["isin"] = admin_bond.id
            request.data["portofolio"] = portofolio.id

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data

            # Coupon
            coupon = data['facial_rate'] * data['outstanding']

            value_date = data['value_date']
            due_date = data['due_date']
            period = data['period']
            differed = data['differed'] 

            # nombre de versements
                # ---------- Problème de division par 0 // A revoir
            nbre_versements = int((due_date - value_date).days / 365.25)
            taux_interet = data['facial_rate']
            ajout = 12
            if period == 'T':
                nbre_versements = nbre_versements * 4
                taux_interet = taux_interet / 4
                ajout = 3
            elif period == 'S':
                nbre_versements = nbre_versements * 2
                taux_interet = taux_interet / 2
                ajout = 6

            # Dates de paiement
            dates_paiement = [value_date]
            while dates_paiement[-1] < due_date:
                next_date = dates_paiement[-1] + relativedelta(months=ajout)
                dates_paiement.append(next_date)
            dates_ajustees = [self.ajust_date(date) for date in dates_paiement]

            # Amortissement
            amortization = 0
            if data['refund'] == 'ACD' or data['refund'] == 'AC':
                amortization = data['outstanding'] / (nbre_versements - differed)
            else:
                differed = 0

            # Cashflows 
                # OAT 
            cashflows = {}
            for i, date_ajustee in enumerate(dates_ajustees):
                if i < differed:
                    cashflow = data['outstanding'] * taux_interet 
                    daily_interest = data['outstanding'] * taux_interet
                else:
                    daily_interest = (data['outstanding'] - (i - differed) * amortization) * taux_interet
                    cashflow = (data['outstanding'] - (i - differed - 1) * amortization) * taux_interet + amortization

                cashflows[date_ajustee.strftime("%Y-%m-%d")] = {
                            'differed_remaining' : max(0, differed - i - 1),
                            'amortization': amortization,
                            'interest': daily_interest,
                            'cashflow': cashflow
                        }
                
            cashflows[dates_ajustees[-1].strftime("%Y-%m-%d")]['cashflow'] += data['outstanding']

            # Date courante
            liste_valorisations = {}
            date_courante = value_date

            # Ajout des dates à la liste
                #J'ai besoin des taux d'actualisation ici 
                    # La valorisation sera modifiée sur la base d'autres paramètres
            days_per_year = 365
            remaining_days_yearly = days_per_year / nbre_versements
            while date_courante <= due_date:
                # Initialisation
                valorisation = 0
                economicValue_plus_100bps, economicValue_minus_100bps, economicValue_steepening_shock, economicValue_flatenning_shock, economicValue_short_rates_shock_up, economicValue_short_rates_shock_down = 0, 0, 0, 0, 0, 0
                
                net_interest = 0
                for date, cashflow in cashflows.items():
                    this_cashflow = cashflow['cashflow']
                    cashflow_date = datetime.strptime(date, "%Y-%m-%d").date()

                    if(date_courante <= cashflow_date):
                        days_difference = max(0, (cashflow_date - date_courante).days)
                        days_difference_on_remaining_days_yearly = days_difference / remaining_days_yearly
                        
                        # Calul de l'interet net journalièrement
                        if not net_interest:
                            net_interest = cashflow['interest'] / 365

                        # taux_interet = taux d'actualisation 
                        rs = 0.025
                        rl = 0.02
                        plus_100bps = taux_interet + 0.01
                        minus_100bps = taux_interet - 0.01
                        steepening_shock = taux_interet - 0.65 * (rs * math.exp(-days_difference / (365 * 4))) + 0.9 * (rl * (1 - math.exp(-days_difference / (365 * 4))))
                        flatenning_shock = taux_interet + 0.8 * (rs * math.exp(-days_difference / (365 * 4))) - 0.6 * (rl * (1 - math.exp(-days_difference / (365 * 4))))
                        short_rates_shock_up = taux_interet + rs * math.exp(-days_difference / (365 * 4))
                        short_rates_shock_down = taux_interet - rs * math.exp(-days_difference / (365 * 4))


                        valorisation += this_cashflow / (1 + taux_interet) ** days_difference_on_remaining_days_yearly

                        # Economic Value 
                        economicValue_plus_100bps += this_cashflow / (1 + plus_100bps) ** days_difference_on_remaining_days_yearly
                        economicValue_minus_100bps += this_cashflow / (1 + minus_100bps) ** days_difference_on_remaining_days_yearly
                        economicValue_steepening_shock += this_cashflow / (1 + steepening_shock) ** days_difference_on_remaining_days_yearly
                        economicValue_flatenning_shock += this_cashflow / (1 + flatenning_shock) ** days_difference_on_remaining_days_yearly
                        economicValue_short_rates_shock_up += this_cashflow / (1 + short_rates_shock_up) ** days_difference_on_remaining_days_yearly
                        economicValue_short_rates_shock_down += this_cashflow / (1 + short_rates_shock_down) ** days_difference_on_remaining_days_yearly
                

                liste_valorisations[date_courante.strftime("%Y-%m-%d")] = {
                    'valorisation' : valorisation,
                    'net_interest' : net_interest,
                    'economicValue_plus_100bps' : economicValue_plus_100bps,
                    'economicValue_minus_100bps' : economicValue_minus_100bps,
                    'economicValue_steepening_shock' : economicValue_steepening_shock,
                    'economicValue_flatenning_shock' : economicValue_flatenning_shock,
                    'economicValue_short_rates_shock_up' : economicValue_short_rates_shock_up,
                    'economicValue_short_rates_shock_down' : economicValue_short_rates_shock_down
                }
                date_courante += timedelta(days=1)

            # Duration Macaulay
            liste_durations = {}
            for valorisation_date, valorisation in liste_valorisations.items():
                durationCashflow, tdurationCashflow = 0, 0
                this_valorisation = valorisation['valorisation']
                this_date = datetime.strptime(valorisation_date, "%Y-%m-%d").date()
                #yieldToMaturity = self.yieldToMaturity(this_date, cashflows, this_valorisation)

                periods = len(cashflows)
                for date, cashflow in cashflows.items():
                    this_cashflow = cashflow['cashflow']
                    cashflow_date = datetime.strptime(date, "%Y-%m-%d").date()
                    days_difference = max(0, (cashflow_date - this_date).days)

                    if(this_date <= cashflow_date):
                        yieldToMaturity = (((data['outstanding'] -  this_valorisation) / periods) + (data['outstanding'] * data['facial_rate'] / nbre_versements))/((data['outstanding'] +  this_valorisation) /2)
                        
                        days_difference_on_remaining_days_yearly = days_difference / remaining_days_yearly
                        durationCashflow += this_cashflow / (1 + yieldToMaturity) ** days_difference_on_remaining_days_yearly
                        tdurationCashflow += (days_difference / days_per_year) * this_cashflow / (1 + yieldToMaturity) ** days_difference_on_remaining_days_yearly
                    
                    periods -= 1

                liste_durations[this_date.strftime("%Y-%m-%d")] = {
                    'duration_macaulay' : tdurationCashflow / durationCashflow,
                    'duration_encours' : (tdurationCashflow / durationCashflow) * data['outstanding']
                }

            # Save
            serializer.validated_data["annual_coupon"] = coupon
            serializer.validated_data["cashflows"] = cashflows
            serializer.validated_data["valorisations"] = liste_valorisations 
            serializer.validated_data["duration_macaulay"] = liste_durations

            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            headers = self.get_success_headers(serializer.data)

            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
            
        except:
            return Response(
                {"message": "Something went wrong while uploading bond ..."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        
    def ajust_date(self, date):
        while date.weekday() >= 5:
            date += timedelta(days=1)
        return date
    
    def bondPrice(self, date_courante, taux, cashflows):
        this_bondPrice = 0
        remainingCashflows = 0
        for cashflow in cashflows:
            cashflow_date = datetime.strptime(cashflow['date'], "%Y-%m-%d").date()
            # Checker si c'est strictement inférieur ou bien inférieur ou égal
            if(date_courante <= cashflow_date):
                remainingCashflows += 1
                this_bondPrice += cashflow['cashflow'] / (1 + taux) ** ((cashflow_date - date_courante).days / 365.25 + remainingCashflows)
        return this_bondPrice
    
    def yieldToMaturity(self, date_courante, cashflows, price):
        epsilonABS = 0.0001
        epsilonSTEP = 0.0001
        niter = 0
        iLower = 0.001
        iUpper = 1

        while True:
            if niter >= 10 or (iUpper - iLower) < epsilonSTEP:
                break

            if math.fabs(self.bondPrice(date_courante, iLower, cashflows) - price) <= epsilonABS:
                break

            if math.fabs(self.bondPrice(date_courante, iUpper, cashflows) - price) <= epsilonABS:
                break

            iMid = (iUpper - iLower) / 2
            if math.fabs(self.bondPrice(date_courante, iMid, cashflows) - price) <= epsilonABS:
                break
            if((self.bondPrice(date_courante, iLower, cashflows) - price) * (self.bondPrice(date_courante, iUpper, cashflows) - price) < 0):
                iUpper = iMid
            else:
                iLower = iMid
            niter += 1

        return iLower
