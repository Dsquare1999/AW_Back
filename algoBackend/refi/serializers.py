from rest_framework import serializers
from .models import Refi

class RefiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refi
        fields = '__all__'


class RefiCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refi
        exclude = ['created_at', 
                   'updated_at', 
                   'refi_user_id', 
                   'refi_interest', 
                   'refi_cashflows'
                ]
