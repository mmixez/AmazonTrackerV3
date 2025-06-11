from django.db import models
from django.utils import timezone # Import timezone for clarity, though auto_now_add handles it

class Product(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=900, unique=True)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
       
        name_val = self.name
        url_val = self.url
        print(f"DEBUG Product __str__: PK={self.pk!r}, name={name_val!r} (type={type(name_val)}), url={url_val!r} (type={type(url_val)})")

        if name_val is not None and name_val != "": 
            return str(name_val)
        elif url_val is not None and url_val != "":
            return str(url_val)
        return f"Product ID: {self.pk or 'N/A'}" 


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # DEBUG: Print values and their types before concatenation
        product_obj = self.product
        price_val = self.price
        checked_at_val = self.checked_at
        
        print(f"DEBUG PriceHistory __str__: PK={self.pk!r}, product_obj={product_obj!r} (type={type(product_obj)}), price={price_val!r} (type={type(price_val)}), checked_at={checked_at_val!r} (type={type(checked_at_val)})")

      
        product_info = "N/A Product"
        if product_obj: # Check if product object exists
            product_name_val = product_obj.name
            product_url_val = product_obj.url
            print(f"DEBUG PriceHistory __str__ (nested product): product_name={product_name_val!r} (type={type(product_name_val)}), product_url={product_url_val!r} (type={type(product_url_val)})")
            
            if product_name_val is not None and product_name_val != "":
                product_info = str(product_name_val)
            elif product_url_val is not None and product_url_val != "":
                product_info = str(product_url_val)

       
        checked_at_str = "N/A Date"
        if checked_at_val:
            try:
                checked_at_str = checked_at_val.strftime('%Y-%m-%d %H:%M')
            except AttributeError:
               
                checked_at_str = "Invalid Date Format"

       
        return f"{product_info} - ${price_val} at {checked_at_str}"

