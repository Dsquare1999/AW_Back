from rest_framework import serializers
from .models import Bilan

from alm.serializers import BondPortofolioSerializer

class BilanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bilan
        fields = '__all__'

class BilanListSerializer(serializers.ModelSerializer):
    bondPortofolios = serializers.SerializerMethodField()

    class Meta:
        model = Bilan
        exclude = ['deleted', 'created_at', 'updated_at']

    def get_bondPortofolios(self, instance):
        try:
            bondPortofolios = instance.bond_portofolio.filter(deleted=False)
            serializer_bondPortofolios = BondPortofolioSerializer(instance=bondPortofolios, many=True)
            return serializer_bondPortofolios.data
        except Exception as e:
            return None