from django.db import models
import uuid

class FinancialOperation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Validation'),
        ('VALIDATED', 'Validated'),
        ('REJECTED', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_code = models.CharField(max_length=50, verbose_name="Código do Ativo")
    issuer = models.CharField(max_length=100, verbose_name="Emissor do Título")
    volume = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor da Operação")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset_code} - {self.issuer} ({self.status})"