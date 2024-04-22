from rest_framework import serializers
from .models import EIB

class EIBSerializer(serializers.ModelSerializer):
    class Meta:
        model = EIB
        fields = '__all__'


class EIBCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EIB
        exclude = ['created_at', 
                   'updated_at', 
                   'eib_user_id', 
                   'eib_interest', 
                   'eib_cashflows'
                   ]
