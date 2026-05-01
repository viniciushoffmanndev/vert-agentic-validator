from rest_framework import serializers
from .models import FinancialOperation

class FinancialOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialOperation
        fields = ['id', 'asset_code', 'issuer', 'volume', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']