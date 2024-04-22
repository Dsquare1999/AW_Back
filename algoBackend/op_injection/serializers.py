from rest_framework import serializers
from .models import OPInjection

class OPInjectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPInjection
        fields = '__all__'


class OPInjectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPInjection
        exclude = ['created_at', 
                   'updated_at', 
                   'op_injection_user_id', 
                   'op_injection_interest', 
                   'op_injection_cashflows'
                   ]
