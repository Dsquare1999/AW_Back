from rest_framework import serializers
from .models import OPRetrait

class OPRetraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPRetrait
        fields = '__all__'


class OPRetraitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPRetrait
        exclude = ['created_at', 
                   'updated_at', 
                   'op_retrait_user_id', 
                   'op_retrait_interest', 
                   'op_retrait_cashflows'
                   ]
