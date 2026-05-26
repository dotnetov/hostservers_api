from rest_framework import serializers
from .models import Tariff, Client, Server, SupportTicket


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = [
            'id',
            'name',
            'price_per_month',
            'cpu_cores',
            'ram_gb',
            'disk_gb',
            'description'
        ]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'registered_at'
        ]


class ServerSerializer(serializers.ModelSerializer):
    tariff = TariffSerializer(read_only=True)
    tariff_id = serializers.PrimaryKeyRelatedField(
        queryset=Tariff.objects.all(),
        source='tariff',
        write_only=True
    )

    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        source='client',
        write_only=True
    )

    class Meta:
        model = Server
        fields = [
            'id',
            'name',
            'ip_address',
            'location',
            'status',
            'tariff',
            'tariff_id',
            'client',
            'client_id',
            'created_at'
        ]


class SupportTicketSerializer(serializers.ModelSerializer):
    server = serializers.StringRelatedField(read_only=True)
    server_id = serializers.PrimaryKeyRelatedField(
        queryset=Server.objects.all(),
        source='server',
        write_only=True
    )

    class Meta:
        model = SupportTicket
        fields = [
            'id',
            'server',
            'server_id',
            'title',
            'message',
            'status',
            'created_at'
        ]