from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinancialOperationViewSet

router = DefaultRouter()
router.register(r'operations', FinancialOperationViewSet, basename='operation')

urlpatterns = [
    path('', include(router.urls)),
]