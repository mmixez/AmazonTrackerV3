import pytest
from django.urls import reverse
from django.utils import timezone
from products.models import Product, PriceHistory
from decimal import Decimal

@pytest.mark.django_db
def test_scrape_view_get(client):
    url = reverse('scrape_view')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'products' in response.context

@pytest.mark.django_db
def test_scrape_view_post_valid(client, mocker):
    # Mock get_product_info to avoid real scraping
    mocker.patch('products.views.get_product_info', return_value=("Test Product", "$99.99", 99.99))
    # Mock send_price_alert to avoid sending emails
    mocker.patch('products.views.send_price_alert')

    url = reverse('scrape_view')
    data = {
        'url': 'https://www.example.com/product',
        'target_price': '100.00',
    }
    response = client.post(url, data)
    assert response.status_code == 302  # redirect after post

    product = Product.objects.get(url=data['url'])
    assert product.name == "Test Product"
    assert product.target_price == 100.00
    assert product.last_price == Decimal('99.99')
    assert PriceHistory.objects.filter(product=product).exists()

@pytest.mark.django_db
def test_scrape_view_post_invalid(client):
    url = reverse('scrape_view')
    data = {
        'url': '',  # empty URL invalid
        'target_price': '',
    }
    response = client.post(url, data)
    # Should re-render form with errors (status 200)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors

@pytest.mark.django_db
def test_delete_product_existing(client):
    product = Product.objects.create(
        name="Delete Me",
        url="https://www.example.com/delete",
        target_price=50.00
    )
    url = reverse('delete_product', args=[product.id])
    response = client.get(url)
    assert response.status_code == 302
    with pytest.raises(Product.DoesNotExist):
        Product.objects.get(id=product.id)

@pytest.mark.django_db
def test_delete_product_nonexistent(client):
    url = reverse('delete_product', args=[9999])  # Nonexistent id
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_product_detail_existing(client):
    product = Product.objects.create(
        name="Detail Product",
        url="https://www.example.com/detail"
    )
    PriceHistory.objects.create(product=product, price=75.00, checked_at=timezone.now())

    url = reverse('product_detail', args=[product.id])
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == product.id
    assert 75.00 in data['price_values']

@pytest.mark.django_db
def test_product_detail_nonexistent(client):
    url = reverse('product_detail', args=[9999])
    response = client.get(url)
    assert response.status_code == 404
    assert 'error' in response.json()

@pytest.mark.django_db
def test_run_price_check_post(client, mocker):
    mocker.patch('products.views.call_command')
    url = reverse('run_price_check')
    response = client.post(url)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'

@pytest.mark.django_db
def test_run_price_check_wrong_method(client):
    url = reverse('run_price_check')
    response = client.get(url)
    assert response.status_code == 400
    data = response.json()
    assert data['status'] == 'error'
