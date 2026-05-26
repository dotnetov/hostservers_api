from django.contrib import admin
from .models import Tariff, Client, Server, SupportTicket


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'price_per_month',
        'cpu_cores',
        'ram_gb',
        'disk_gb'
    ]
    search_fields = ['name']
    list_filter = ['price_per_month', 'cpu_cores', 'ram_gb']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'full_name',
        'email',
        'phone',
        'registered_at'
    ]
    search_fields = ['full_name', 'email', 'phone']


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'ip_address',
        'location',
        'status',
        'tariff',
        'client',
        'created_at'
    ]
    search_fields = ['name', 'ip_address', 'location']
    list_filter = ['status', 'location', 'tariff']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'server',
        'title',
        'status',
        'created_at'
    ]
    search_fields = ['title', 'message']
    list_filter = ['status', 'created_at']