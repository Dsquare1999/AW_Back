from rest_framework import serializers
from .models import DAT

class DATSerializer(serializers.ModelSerializer):
    class Meta:
        model = DAT
        fields = '__all__'


class DATCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DAT
        exclude = ['created_at', 
                   'updated_at', 
                   'dat_user_id', 
                   'dat_interest', 
                   'dat_cashflows'
                ]
