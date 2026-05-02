# validation/views.py
from rest_framework import viewsets
from .models import FinancialOperation
from .serializers import FinancialOperationSerializer
from .producer import send_operation_to_kafka

class FinancialOperationViewSet(viewsets.ModelViewSet):
    queryset = FinancialOperation.objects.all().order_by('-created_at')
    serializer_class = FinancialOperationSerializer

    def perform_create(self, serializer):
        # Salva o registro no PostgreSQL
        operation = serializer.save()
        
        # Prepara os dados para o Kafka
        operation_data = {
            'id': str(operation.id),
            'asset_code': operation.asset_code,
            'issuer': operation.issuer,
            'volume': str(operation.volume),
            'status': operation.status,
        }
        
        # Envia para o Kafka
        try:
            send_operation_to_kafka(operation_data)
        except Exception as e:
            print(f"Erro ao enviar para o Kafka: {e}")