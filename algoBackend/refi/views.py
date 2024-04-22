from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.

from .models import Refi
from .serializers import RefiSerializer, RefiCreateSerializer

import math
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class RefiViewset(viewsets.ModelViewSet):
    queryset = Refi.objects.all()
    serializer_class = RefiSerializer

    def get_serializer_class(self):
        return RefiCreateSerializer if self.action == 'create' else RefiSerializer
    
    def perform_create(self, serializer):
        data = serializer.validated_data

        outstanding = data['refi_outstanding']
        value_date = data['refi_value_date']
        due_date = data['refi_due_date']
        taux_interet = data['refi_rate']
        type = data['refi_type']
        
        taux_actualisation = taux_interet
        interest = outstanding * taux_interet

        # Dates de paiement
        date_paiement = due_date

        payable = outstanding + outstanding * interest
        if type == 0:
            payable = outstanding

        valorisation = outstanding * ((1 + taux_interet) / (1 + taux_actualisation))

        duration = 0
        economicValue_plus_100bps, economicValue_minus_100bps, economicValue_steepening_shock, economicValue_flatenning_shock, economicValue_short_rates_shock_up, economicValue_short_rates_shock_down = 0, 0, 0, 0, 0, 0

        cashflows = {}
        date_courante = value_date
        while date_courante < date_paiement:
            days_difference = (due_date - date_courante).days
            duration = max(0, days_difference / 360)      
            
            rs = 0.025
            rl = 0.02
            plus_100bps = taux_actualisation + 0.01
            minus_100bps = taux_actualisation - 0.01
            steepening_shock = taux_actualisation - 0.65 * (rs * math.exp(-days_difference / (360 * 4))) + 0.9 * (rl * (1 - math.exp(-days_difference / (360 * 4))))
            flatenning_shock = taux_actualisation + 0.8 * (rs * math.exp(-days_difference / (360 * 4))) - 0.6 * (rl * (1 - math.exp(-days_difference / (360 * 4))))
            short_rates_shock_up = taux_actualisation + rs * math.exp(-days_difference / (360 * 4))
            short_rates_shock_down = taux_actualisation - rs * math.exp(-days_difference / (360 * 4))


            economicValue_plus_100bps = outstanding * ((1 + taux_interet) / (1 + plus_100bps))
            economicValue_minus_100bps = outstanding * ((1 + taux_interet) / (1 + minus_100bps))
            economicValue_steepening_shock = outstanding * ((1 + taux_interet) / (1 + steepening_shock))
            economicValue_flatenning_shock = outstanding * ((1 + taux_interet) / (1 + flatenning_shock))
            economicValue_short_rates_shock_up = outstanding * ((1 + taux_interet) / (1 + short_rates_shock_up))
            economicValue_short_rates_shock_down = outstanding * ((1 + taux_interet) / (1 + short_rates_shock_down))
        

            cashflows[date_courante.strftime('%Y-%m-%d')] = {
                'net_interest': interest / (due_date - value_date).days,
                'payable': 0,
                'valorisation': valorisation,
                'duration' : duration,
                'duration_times_outstanding' : duration * payable,
                'economicValue_plus_100bps': economicValue_plus_100bps,
                'economicValue_minus_100bps': economicValue_minus_100bps,
                'economicValue_steepening_shock': economicValue_steepening_shock,
                'economicValue_flatenning_shock': economicValue_flatenning_shock,
                'economicValue_short_rates_shock_up': economicValue_short_rates_shock_up,
                'economicValue_short_rates_shock_down': economicValue_short_rates_shock_down
            }

            date_courante = date_courante + relativedelta(day=1)
        cashflows[date_paiement.strftime('%Y-%m-%d')]['payable'] = payable

        serializer.save(
            refi_interest=interest,
            refi_cashflows=cashflows
        )