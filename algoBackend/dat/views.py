from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.

from .models import DAT
from .serializers import DATSerializer, DATCreateSerializer

from dateutil.relativedelta import relativedelta

class DATViewset(viewsets.ModelViewSet):
    queryset = DAT.objects.all()
    serializer_class = DATSerializer

    def get_serializer_class(self):
        return DATCreateSerializer if self.action == 'create' else DATSerializer
    
    def perform_create(self, serializer):
        data = serializer.validated_data

        outstanding = data['dat_outstanding']
        value_date = data['dat_value_date']
        due_date = data['dat_due_date']
        period = data['dat_period']

        # nombre de versements (norme 360 jours /an)
        nbre_versements = int((date_courante - value_date) / 360)
        taux_interet = data['dat_rate']
        ajout = 1
        if period == 'T':
            ajout = 4
        elif period == 'S':
            ajout = 2
        elif period == 'M':
            ajout = 12
        nbre_versements = nbre_versements * ajout
        taux_interet = ((1 + taux_interet)** (1/ajout)) - 1

        # Payable = Interest + Outstanding
        payable = outstanding * ((1 + taux_interet) ** nbre_versements)
        interest = payable - outstanding

        # Dates de paiement
        date_paiement = due_date
        
        

        cashflows = {}
        date_courante = value_date
        while date_courante < date_paiement:
            
            # Duration
            days_difference = (due_date - date_courante).days
            duration = max(0, days_difference / 360)      

            # nombre de versements entre la date de valeur et aujourd'hui
            nbre_versements = int((date_courante - value_date) / 360)
            valorisation = outstanding * ((1 + taux_interet) ** nbre_versements)

            cashflows[date_courante.strftime('%Y-%m-%d')] = {
                'interest': interest,
                'net_interest': interest / (due_date - date_courante).days,
                'payable': 0,
                'valorisation': valorisation,
                'duration' : duration,
                'duration_times_outstanding' : duration * payable
            }

            date_courante = date_courante + relativedelta(day=1)
        cashflows[date_paiement.strftime('%Y-%m-%d')]['payable'] = payable

        serializer.save(
            dat_interest=interest,
            dat_cashflows=cashflows
        )