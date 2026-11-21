from rest_framework import serializers
from .models import RightsHolder, Contract, ContractAsset, SalesTransaction, RoyaltyCalculation, RoyaltyPayout

class RightsHolderSerializer(serializers.ModelSerializer):
    contracts_count = serializers.IntegerField(source='contracts.count', read_only=True)

    class Meta:
        model = RightsHolder
        fields = '__all__'


class ContractAssetSerializer(serializers.ModelSerializer):
    asset_title = serializers.CharField(source='asset.title', read_only=True)

    class Meta:
        model = ContractAsset
        fields = ['contract_asset_id', 'contract', 'asset', 'asset_title', 'exclusivity', 'royalty_split_percent']


class ContractSerializer(serializers.ModelSerializer):
    rights_holder_name = serializers.CharField(source='rights_holder.legal_name', read_only=True)
    contract_assets = ContractAssetSerializer(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'


class SalesTransactionSerializer(serializers.ModelSerializer):
    contract_code = serializers.CharField(source='contract.contract_code', read_only=True)
    asset_title = serializers.CharField(source='asset.title', read_only=True)

    class Meta:
        model = SalesTransaction
        fields = '__all__'


class RoyaltyCalculationSerializer(serializers.ModelSerializer):
    contract_code = serializers.CharField(source='contract.contract_code', read_only=True)
    rights_holder_name = serializers.CharField(source='rights_holder.legal_name', read_only=True)

    class Meta:
        model = RoyaltyCalculation
        fields = '__all__'


class RoyaltyPayoutSerializer(serializers.ModelSerializer):
    calculation_code = serializers.CharField(source='calculation.calculation_code', read_only=True)
    rights_holder_name = serializers.CharField(source='calculation.rights_holder.legal_name', read_only=True)

    class Meta:
        model = RoyaltyPayout
        fields = '__all__'
