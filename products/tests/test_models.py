import pytest
from django.utils import timezone
from products.models import Product, PriceHistory

@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(
        name="Test Product",
        url="https://www.example.com/product",
        target_price=99.99,
        last_price=120.00,
        last_checked=timezone.now()
    )
    assert product.pk is not None
    assert str(product) == "Test Product"

@pytest.mark.django_db
def test_create_product_without_name():
    product = Product.objects.create(
        url="https://www.example.com/no-name",
        target_price=50.00
    )
    assert str(product) == "https://www.example.com/no-name"

@pytest.mark.django_db
def test_price_history_str():
    product = Product.objects.create(
        name="History Product",
        url="https://www.example.com/history"
    )
    history = PriceHistory.objects.create(
        product=product,
        price=79.99
    )
    assert "History Product" in str(history)
    assert f"{history.price}" in str(history)
