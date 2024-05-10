from datetime import datetime
from swaps.models import SwapOperation, SwapProposition

from rest_framework import serializers
from alm.models import Bond
from alm.serializers import BondSerializer

class SwapOperationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapOperation
        exclude = ['deleted', 'created_at', 'updated_at']

class SwapOperationSerializer(serializers.ModelSerializer):
    propositions = serializers.SerializerMethodField()
    offer_bond = serializers.SerializerMethodField()
    
    class Meta:
        model = SwapOperation
        fields = '__all__'

    def get_propositions(self, instance):
        try:
            propositions = instance.propositions.filter(deleted=False)
            serializer_proposition = SwapPropositionSerializer(instance=propositions, many=True)
            return serializer_proposition.data
        except Exception as e:
            return None
    
    def get_offer_bond(self, instance):
        try:
            offer_bond = instance.offer
            serializer_offer_bond = BondSerializer(instance=offer_bond)
            return serializer_offer_bond.data
        except Exception as e:
            return None

    def validate_offer(self, value):
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
    
    # def validate_attractive(self, value):
    #     """
    #     Méthode de validation personnalisée pour vérifier la validité du tableau attractive.
    #     """
    #     if len(value) != 5:
    #         raise serializers.ValidationError("The attractive table must have 5 values")
    #     for val in value:
    #         if val != True and val != False:
    #             raise serializers.ValidationError("The attractive table must have boolean values")
    #     return value
    
class SwapPropositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapProposition
        exclude = ['deleted', 'created_at', 'updated_at']

class SwapPropositionSerializer(serializers.ModelSerializer):
    proposition_bond = serializers.SerializerMethodField()
    class Meta:
        model = SwapProposition
        exclude = ['deleted']

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
    
    def get_proposition_bond(self, instance):
        try:
            proposition_bond = instance.proposition
            serializer_proposition_bond = BondSerializer(instance=proposition_bond)
            return serializer_proposition_bond.data
        except Exception as e:
            return None