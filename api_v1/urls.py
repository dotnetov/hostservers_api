from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TariffViewSet,
    ClientViewSet,
    ServerViewSet,
    SupportTicketViewSet
)


router = DefaultRouter()

router.register(r'tariffs', TariffViewSet, basename='tariff')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'servers', ServerViewSet, basename='server')
router.register(r'tickets', SupportTicketViewSet, basename='ticket')


urlpatterns = [
    path('', include(router.urls)),
]