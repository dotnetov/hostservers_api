from django.db import models


class Tariff(models.Model):
    name = models.CharField(max_length=100)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    cpu_cores = models.PositiveIntegerField()
    ram_gb = models.PositiveIntegerField()
    disk_gb = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Server(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('stopped', 'Остановлен'),
        ('suspended', 'Заблокирован'),
    ]

    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(unique=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='servers')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='servers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыта'),
        ('in_progress', 'В работе'),
        ('closed', 'Закрыта'),
    ]

    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title