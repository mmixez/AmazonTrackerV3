from django.core.management.base import BaseCommand
from products.models import Product
from products.scraper import get_product_info, send_price_alert
from django.utils import timezone
from products.models import Product, PriceHistory


class Command(BaseCommand):
    help = 'Checks prices for all tracked products and sends alerts if below target price.'

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            title, price_str, price_float = get_product_info(product.url)
            if price_float is None:
                self.stdout.write(f"Skipping {product.name} due to invalid price.")
                continue

            product.last_price = price_float
            product.last_checked = timezone.now()
            product.save()

            # Add this block to save price history:
            PriceHistory.objects.create(product=product, price=price_float)

            self.stdout.write(f"Checked {title}: {price_str}")

            if price_float <= product.target_price:
                send_price_alert(title, product.url, price_float)
                self.stdout.write(f"Price alert sent for {title}!")

        self.stdout.write("Price check completed.")