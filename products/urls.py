from django.urls import path
from django.http import HttpResponse
from .views import scrape_view, delete_product, product_detail, run_price_check  

def home_view(request):
    return HttpResponse("Welcome! Visit /scrape/ to see the product info.")

urlpatterns = [
    path('', home_view, name='home'),
    path('scrape/', scrape_view, name='scrape_view'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'), 
    path('run-price-check/', run_price_check, name='run_price_check'),
]
