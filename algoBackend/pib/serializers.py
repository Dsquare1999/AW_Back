from rest_framework import serializers
from .models import PIB

class PIBSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIB
        fields = '__all__'


class PIBCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIB
        exclude = ['created_at', 
                   'updated_at', 
                   'pib_user_id', 
                   'pib_interest', 
                   'pib_cashflows'
                ]
