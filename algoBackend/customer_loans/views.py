from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.

from .models import CustomerLoan
from .serializers import CustomerLoanSerializer,CustomerLoanCreateSerializer

import numpy_financial as npf
import math
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class LoansViewSet(viewsets.ModelViewSet):
    queryset = CustomerLoan.objects.all()
    serializer_class = CustomerLoanSerializer   

    def get_serializer_class(self):
        return CustomerLoanCreateSerializer if self.action == 'create' else CustomerLoanSerializer

    def perform_create(self, serializer):
        
        data = serializer.validated_data

        interest = data['loan_outstanding'] * data['loan_rate'] 

        value_date = data['loan_value_date']
        due_date = data['loan_due_date']
        period = data['loan_period']

        # nombre de versements (norme 360 jours /an)
        nbre_versements = int((due_date - value_date).days / 360)
        taux_interet = data['loan_rate']
        ajout = 12
        if period == 'T':
            nbre_versements = nbre_versements * 4
            taux_interet = taux_interet / 4
            ajout = 3
        elif period == 'S':
            nbre_versements = nbre_versements * 2
            taux_interet = taux_interet / 2
            ajout = 6
        elif period == 'M':
            nbre_versements = nbre_versements * 12
            taux_interet = taux_interet / 12
            ajout = 1

        # Dates de paiement
            # On commence par le mois suivant la date de valeur
        dates_paiement = [value_date + relativedelta(months=ajout)]
        while dates_paiement[-1] <= due_date:
            next_date = dates_paiement[-1] + relativedelta(months=ajout)
            dates_paiement.append(next_date)

        # Cashflows
        cashflows = {}
        
        # Versement périodique
        versement = npf.pmt(taux_interet, nbre_versements, -data['loan_outstanding'])

        # Il me faut trouver le vrai taux d'actualisation ici
            # On utilise apparement une variable d multiple de 12
        taux_actualisation = taux_interet
        for index, date_paiement in enumerate(dates_paiement):
            # Initialisation
            days_difference = max(0, (due_date - date_paiement).days)
            fluxTotal, fluxPondere, valorisation = 0, 0, 0
            economicValue_plus_100bps, economicValue_minus_100bps, economicValue_steepening_shock, economicValue_flatenning_shock, economicValue_short_rates_shock_up, economicValue_short_rates_shock_down = 0, 0, 0, 0, 0, 0
            
            # taux_interet = taux d'actualisation 
            rs = 0.025
            rl = 0.02
            plus_100bps = taux_actualisation + 0.01
            minus_100bps = taux_actualisation - 0.01
            steepening_shock = taux_actualisation - 0.65 * (rs * math.exp(-days_difference / (365 * 4))) + 0.9 * (rl * (1 - math.exp(-days_difference / (365 * 4))))
            flatenning_shock = taux_actualisation + 0.8 * (rs * math.exp(-days_difference / (365 * 4))) - 0.6 * (rl * (1 - math.exp(-days_difference / (365 * 4))))
            short_rates_shock_up = taux_actualisation + rs * math.exp(-days_difference / (365 * 4))
            short_rates_shock_down = taux_actualisation - rs * math.exp(-days_difference / (365 * 4))

            for versement_index in range(index, nbre_versements - 1):
                fluxTotal += versement
                fluxPondere += versement * (versement_index + 1)
                valorisation += versement / ((1 + taux_actualisation) ** ((versement_index + 1)/12))
                economicValue_plus_100bps += versement / ((1 + plus_100bps) ** ((versement_index + 1)/12))
                economicValue_minus_100bps += versement / ((1 + minus_100bps) ** ((versement_index + 1)/12))
                economicValue_steepening_shock += versement / ((1 + steepening_shock) ** ((versement_index + 1)/12))
                economicValue_flatenning_shock += versement / ((1 + flatenning_shock) ** ((versement_index + 1)/12))
                economicValue_short_rates_shock_up += versement / ((1 + short_rates_shock_up) ** ((versement_index + 1)/12))
                economicValue_short_rates_shock_down += versement / ((1 + short_rates_shock_down) ** ((versement_index + 1)/12))
            else:
                duration = 0
                if fluxTotal != 0:
                    duration = fluxPondere / (fluxTotal * 12)

            cashflows[date_paiement.strftime("%Y-%m-%d")] = {
                        'interest_rate': taux_interet,
                        'net_interest' : (versement * nbre_versements - data['loan_outstanding']) / (due_date - value_date).days,
                        'actualisation_rate': taux_interet,
                        'versement': versement,
                        'duration' : duration,
                        'mean_duration': duration,
                        'duration_times_outstanding': duration * data['loan_outstanding'],
                        'fluxTotal': fluxTotal,
                        'fluxPondere': fluxPondere,
                        'valorisation' : valorisation,
                        'economicValue_plus_100bps': economicValue_plus_100bps,
                        'economicValue_minus_100bps': economicValue_minus_100bps,
                        'economicValue_steepening_shock': economicValue_steepening_shock,
                        'economicValue_flatenning_shock': economicValue_flatenning_shock,
                        'economicValue_short_rates_shock_up': economicValue_short_rates_shock_up,
                        'economicValue_short_rates_shock_down': economicValue_short_rates_shock_down
                    }

        serializer.save(loan_interest=interest, loan_cashflows=cashflows)