from rest_framework import viewsets
from .models import FinancialOperation
from .serializers import FinancialOperationSerializer

class FinancialOperationViewSet(viewsets.ModelViewSet):
    queryset = FinancialOperation.objects.all().order_by('-created_at')
    serializer_class = FinancialOperationSerializer