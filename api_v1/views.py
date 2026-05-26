from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_extensions.cache.decorators import cache_response

from .models import Tariff, Client, Server, SupportTicket
from .serializers import (
    TariffSerializer,
    ClientSerializer,
    ServerSerializer,
    SupportTicketSerializer
)


class TariffViewSet(viewsets.ModelViewSet):
    """Представление для работы с тарифами хостинга."""

    serializer_class = TariffSerializer
    queryset = Tariff.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')

        if name:
            qs = qs.filter(name__icontains=name)

        return qs

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')

        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Tariff.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)


class ClientViewSet(viewsets.ModelViewSet):
    """Представление для работы с клиентами хостинга."""

    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        email = self.request.query_params.get('email')
        full_name = self.request.query_params.get('full_name')

        if email:
            qs = qs.filter(email__icontains=email)

        if full_name:
            qs = qs.filter(full_name__icontains=full_name)

        return qs

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')

        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Client.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)


class ServerViewSet(viewsets.ModelViewSet):
    """Представление для работы с серверами/VPS."""

    serializer_class = ServerSerializer
    queryset = Server.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        status_value = self.request.query_params.get('status')
        client_id = self.request.query_params.get('client_id')
        tariff_id = self.request.query_params.get('tariff_id')
        location = self.request.query_params.get('location')

        if status_value:
            qs = qs.filter(status=status_value)

        if client_id:
            qs = qs.filter(client_id=client_id)

        if tariff_id:
            qs = qs.filter(tariff_id=tariff_id)

        if location:
            qs = qs.filter(location__icontains=location)

        return qs

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')

        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Server.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['patch'], url_path='bulk-update')
    def bulk_update(self, request):
        serializer_data = request.data

        if not isinstance(serializer_data, list):
            return Response(
                {'error': 'Ожидался список объектов'},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_servers = []

        for item in serializer_data:
            server_id = item.get('id')

            if not server_id:
                return Response(
                    {'error': 'У каждого объекта должен быть id'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                server = Server.objects.get(id=server_id)
            except Server.DoesNotExist:
                return Response(
                    {'error': f'Сервер с id={server_id} не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = self.get_serializer(server, data=item, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            updated_servers.append(serializer.data)

        return Response(updated_servers, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.query_params.get('ids')

        if not ids:
            return Response(
                {'error': 'Передайте ids, например: ?ids=1,2,3'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ids_list = [int(pk) for pk in ids.split(',')]
        Server.objects.filter(id__in=ids_list).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SupportTicketViewSet(viewsets.ModelViewSet):
    """Представление для работы с обращениями в поддержку."""

    serializer_class = SupportTicketSerializer
    queryset = SupportTicket.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        server_id = self.request.query_params.get('server_id')
        status_value = self.request.query_params.get('status')

        if server_id:
            qs = qs.filter(server_id=server_id)

        if status_value:
            qs = qs.filter(status=status_value)

        return qs

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')

        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            SupportTicket.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)
