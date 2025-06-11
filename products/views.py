from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.core.management import call_command
from .models import Product, PriceHistory
from .forms import ProductURLForm
from .scraper import get_product_info, send_price_alert, save_to_csv
import json
from zoneinfo import ZoneInfo
from django.utils.timezone import localtime


def scrape_view(request):
    if request.method == 'POST':
        form = ProductURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url'].strip()
            target_price = form.cleaned_data['target_price']

            if url:
                title, price_str, price_float = get_product_info(url)
                save_to_csv(title, price_str)

                product, created = Product.objects.update_or_create(
                    url=url,
                    defaults={
                        'name': title,
                        'last_price': price_float,
                        'last_checked': timezone.now(),
                        'target_price': target_price,
                    }
                )

                # Save price to history
                if price_float is not None:
                    PriceHistory.objects.create(product=product, price=price_float)

                # Send alert if below target
                if price_float is not None and target_price and price_float <= target_price:
                    send_price_alert(title, url, price_float)

            return redirect('scrape_view')
    else:
        form = ProductURLForm()

    all_products = Product.objects.all()
    pacific = ZoneInfo("America/Los_Angeles")

    # Prepare history for modal chart
    products_history = [
        {
            'id': product.id,
            'price_dates': [
                localtime(h.checked_at, pacific).strftime('%Y-%m-%d %H:%M')
                for h in product.price_history.order_by('checked_at')
            ],
            'price_values': [
                float(h.price) for h in product.price_history.order_by('checked_at')
            ],
        }
        for product in all_products
    ]

    context = {
        'form': form,
        'products': all_products,
        'products_history': json.dumps(products_history),  # Safe for JS
    }

    return render(request, 'products/scrape.html', context)


def delete_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if product:
        product.delete()
        messages.success(request, "Product deleted successfully.")
    else:
        messages.warning(request, "Product not found.")
    return redirect('scrape_view')


def product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'error': 'Product not found'}, status=404)

    price_history = product.price_history.order_by('checked_at')
    data = {
        'id': product.id,
        'price_values': [float(p.price) for p in price_history],
        'price_dates': [p.checked_at.strftime('%Y-%m-%d %H:%M') for p in price_history]
    }
    return JsonResponse(data)


def run_price_check(request):
    if request.method == 'POST':
        try:
            call_command('check_prices')
            return JsonResponse({'status': 'success', 'message': 'Price check triggered successfully.'})
        except Exception as e:
            print("Error in run_price_check:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
