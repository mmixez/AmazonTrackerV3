from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=900, unique=True)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name or self.url


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name or self.product.url} - ${self.price} at {self.checked_at.strftime('%Y-%m-%d %H:%M')}"

