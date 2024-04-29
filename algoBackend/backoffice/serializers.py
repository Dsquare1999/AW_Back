from rest_framework import serializers
from .models import AdminBond

class AdminBondCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminBond
        exclude = ['deleted', 'created_at', 'updated_at']


class AdminBondSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminBond
        exclude = ['deleted', 'created_at', 'updated_at']

    def validate_isin(self, value):
        """
        Méthode de validation personnalisée pour vérifier l'unicité du champ isin.
        """
        if AdminBond.objects.filter(isin=value).exists():
            raise serializers.ValidationError("A Bond with this ISIN already exists")
        return value