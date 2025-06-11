import pytest
from django.utils import timezone
from products.models import Product, PriceHistory
from decimal import Decimal

@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(
        name="Test Product",
        url="https://www.example.com/product",
        target_price=Decimal("99.99"),
        last_price=Decimal("120.00"),
        last_checked=timezone.now()
    )
    assert product.pk is not None
    assert str(product) == "Test Product"

@pytest.mark.django_db
def test_create_product_without_name():
    product = Product.objects.create(
        name="",  # explicitly empty string instead of None
        url="https://www.example.com/no-name",
        target_price=Decimal("50.00")
    )
    # The __str__ should fallback to URL if name is empty
    assert str(product) == "https://www.example.com/no-name"

@pytest.mark.django_db
def test_price_history_str():
    product = Product.objects.create(
        name="History Product",
        url="https://www.example.com/history"
    )
    history = PriceHistory.objects.create(
        product=product,
        price=Decimal("79.99"),
        checked_at=timezone.now()  # explicitly set checked_at because __str__ uses it
    )
    str_history = str(history)
    assert "History Product" in str_history
    assert f"{history.price}" in str_history
