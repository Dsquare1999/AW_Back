from datetime import datetime
from .models import SwapOperation, SwapProposition

from rest_framework import serializers
from alm.models import Bond

class SwapOperationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapOperation
        exclude = ['deleted', 'created_at', 'updated_at']

class SwapOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapOperation
        fields = '__all__'

    def validate_bond(self, value):
        """
        Méthode de validation personnalisée pour vérifier l'existence du bond.
        """
        if not Bond.objects.filter(id=value).exists():
            raise serializers.ValidationError("This Bond does not exist")
        return value
    
    def validate_validity(self, value):
        """
        Méthode de validation personnalisée pour vérifier la validité de la date de validité.
        """
        if value < datetime.date.today():
            raise serializers.ValidationError("This date is not valid")
        return value
    
    def validate_attractive(self, value):
        """
        Méthode de validation personnalisée pour vérifier la validité du tableau attractive.
        """
        if len(value) != 5:
            raise serializers.ValidationError("The attractive table must have 5 values")
        for val in value:
            if val != True and val != False:
                raise serializers.ValidationError("The attractive table must have boolean values")
        return value
    
class SwapPropositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapProposition
        exclude = ['deleted', 'created_at', 'updated_at']

class SwapPropositionSerializer(serializers.ModelField):
    class Meta:
        model = SwapProposition
        fields = '__all__'

    def validate_proposition(self, value):
        """
        Méthode de validation personnalisée pour vérifier l'existence du bond.
        """
        if not Bond.objects.filter(id=value).exists():
            raise serializers.ValidationError("This Bond does not exist")
        return value
    
    def validate_status(self, value):
        """
        Méthode de validation personnalisée pour vérifier la validité du status.
        """
        if value != 'P' and value != 'A' and value != 'R':
            raise serializers.ValidationError("This status is not valid")
        return value