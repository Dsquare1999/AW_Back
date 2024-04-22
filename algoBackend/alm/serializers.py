from rest_framework import serializers
from .models import Bond, BondPortofolio


class BondSerializer(serializers.ModelSerializer):
    annual_coupon = serializers.FloatField(required=False)

    class Meta:
        model = Bond
        exclude = ['deleted', 'created_at', 'updated_at']

    def create(self, validated_data):
        annual_coupon = validated_data.pop('annual_coupon', 0)
        cashflows = validated_data.pop('cashflows', {})
        valorisations = validated_data.pop('valorisations', {})
        duration_macaulay = validated_data.pop('duration_macaulay', {})

        bond = Bond.objects.create(**validated_data)

        bond.annual_coupon = annual_coupon
        bond.cashflows = cashflows
        bond.valorisations = valorisations
        bond.duration_macaulay = duration_macaulay
        bond.save()

        return bond


class BondPortofolioSerializer(serializers.ModelSerializer):
    bonds = serializers.SerializerMethodField()

    class Meta:
        model = BondPortofolio
        exclude = ['deleted', 'created_at', 'updated_at']

    def get_bonds(self, instance):
        try: 
            bonds = instance.bond.filter(deleted=False)
            serializer_bond = BondSerializer(instance=bonds, many=True)
            return serializer_bond.data
        except Exception as e:
            return None
        

