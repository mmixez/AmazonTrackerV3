from django.db import models
from django.utils import timezone # Import timezone for clarity, though auto_now_add handles it

class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=900, unique=True)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        # Ensure 'name' is treated as a string. If it's an empty string or None,
        # fallback to 'url'. If 'url' is also potentially None (though unique=True
        # implies it must be set for saved objects), convert it to string.
        # Finally, provide a robust fallback if both name and url are unusable.
        if self.name:
            return str(self.name) # Ensure it's a string, even if it was None accidentally
        elif self.url:
            return str(self.url) # Ensure it's a string
        return f"Product ID: {self.pk or 'N/A'}" # Fallback for unsaved or truly empty cases


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      
        product_info = "N/A Product"
        if self.product: 
            if self.product.name:
                product_info = str(self.product.name)
            elif self.product.url: # If name is empty or None, try URL
                product_info = str(self.product.url)

       
        checked_at_str = "N/A Date"
        if self.checked_at:
            try:
                checked_at_str = self.checked_at.strftime('%Y-%m-%d %H:%M')
            except AttributeError:
               
                checked_at_str = "Invalid Date Format"

       
        return f"{product_info} - ${self.price} at {checked_at_str}"

