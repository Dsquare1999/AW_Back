from backoffice.serializers import AdminBondSerializer
from spreads.models import SpreadOperation, SpreadProposition
from rest_framework import serializers

from backoffice.models import AdminBond
from datetime import datetime

class SpreadOperationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpreadOperation
        exclude = ['deleted', 'created_at', 'updated_at', 'isPublic', 'isPublished']

class SpreadOperationSerializer(serializers.ModelSerializer):
    propositions = serializers.SerializerMethodField()
    admin_bond = serializers.SerializerMethodField()

    class Meta:
        model = SpreadOperation
        exclude = ['deleted', 'created_at', 'updated_at', 'isPublic', 'isPublished']

    def get_propositions(self, instance):
        try:
            propositions = instance.propositions.filter(deleted=False)
            serializer_proposition = SpreadPropositionSerializer(instance=propositions, many=True)
            return serializer_proposition.data
        except Exception as e:
            return None
    
    def get_admin_bond(self, instance):
        try:
            admin_bond = instance.admin_bond
            serializer_admin_bond = AdminBondSerializer(instance=admin_bond)
            return serializer_admin_bond.data
        except Exception as e:
            return None

    def validate_bond(self, value):
        """
        Méthode de validation personnalisée pour vérifier l'existence du bond.
        """
        if not AdminBond.objects.filter(id=value).exists():
            raise serializers.ValidationError("This Bond does not exist")
        return value
    
    def validate_quantity(self, value):
        """
        Méthode de validation personnalisée pour vérifier la quantité.
        """
        if value <= 0:
            raise serializers.ValidationError("The quantity must be positive")
        return value
    
    def validate_order(self, value):
        """
        Méthode de validation personnalisée pour vérifier la validité de l'ordre.
        """
        if value < 0 or value > 3:
            raise serializers.ValidationError("This order is not valid")
        return value
    
    def validate_type(self, value):
        """
        Méthode de validation personnalisée pour vérifier la validité du type.
        """
        if value != 'B' and value != 'S':
            raise serializers.ValidationError("This type is not valid")
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
            raise serializers.ValidationError("This array is not valid")
        for i in value:
            if i != True and i != False:
                raise serializers.ValidationError("This array is not valid")
        return value
    

class SpreadPropositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpreadProposition
        exclude = ['deleted', 'created_at', 'updated_at']

class SpreadPropositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpreadProposition
        exclude = ['deleted', 'created_at', 'updated_at']

    def validate_operation(self, value):
        """
        Méthode de validation personnalisée pour vérifier l'existence de l'opération.
        """
        if not SpreadOperation.objects.filter(id=value).exists():
            raise serializers.ValidationError("This Spread Operation does not exist")
        return value
    
    def validate_status(self, value):
        """
        Méthode de validation personnalisée pour vérifier la validité du status.
        """
        if value != 'P' and value != 'A' and value != 'R':
            raise serializers.ValidationError("This status is not valid")
        return value
    



