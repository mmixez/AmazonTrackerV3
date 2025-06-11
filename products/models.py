# products/models.py

from django.db import models
from django.utils import timezone # Import timezone for potential future use or clarity

class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=900, unique=True)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
       
        if self.name:
            return str(self.name)
        elif self.url:
            return str(self.url)
       
        return f"Product ID: {self.pk}"


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      
        product_info = "N/A Product"
        if self.product:
            if self.product.name:
                product_info = str(self.product.name)
            elif self.product.url:
                product_info = str(self.product.url)

      
        checked_at_str = "N/A Date"
        if self.checked_at:
            checked_at_str = self.checked_at.strftime('%Y-%m-%d %H:%M')

    
        return f"{product_info} - ${self.price} at {checked_at_str}"