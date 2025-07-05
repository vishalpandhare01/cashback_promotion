from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CashbackRule(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    cashback_percentage = models.DecimalField(max_digits=5, decimal_places=2) 
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.cashback_percentage}%)"

    def is_active(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.status == 'active' and self.valid_from <= today <= self.valid_to


class CashbackTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('issued', 'Issued'),
        ('redeemed', 'Redeemed'),
    ]

    customer_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cashback_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    cashback_rule = models.ForeignKey(CashbackRule, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cashback {self.cashback_amount} for Order {self.order_id} ({self.status})"
