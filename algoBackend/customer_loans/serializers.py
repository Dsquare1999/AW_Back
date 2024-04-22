from rest_framework import serializers
from .models import CustomerLoan

class CustomerLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLoan
        fields = '__all__'


class CustomerLoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLoan
        exclude = ['created_at', 
                   'updated_at', 
                   'loan_user_id', 
                   'loan_interest', 
                   'loan_cashflows'
                   ]
