import pytest
from products.forms import ProductURLForm

def test_valid_form():
    form_data = {
        'url': 'https://www.amazon.com/dp/B08N5WRWNW',
        'target_price': 99.99,
    }
    form = ProductURLForm(data=form_data)
    assert form.is_valid()

def test_invalid_url():
    form_data = {
        'url': 'invalid-url',
        'target_price': 50.00,
    }
    form = ProductURLForm(data=form_data)
    assert not form.is_valid()
    assert 'url' in form.errors

def test_empty_url():
    form_data = {
        'url': '',
        'target_price': 50.00,
    }
    form = ProductURLForm(data=form_data)
    assert not form.is_valid()
    assert 'url' in form.errors

def test_empty_target_price():
    form_data = {
        'url': 'https://www.amazon.com/dp/B08N5WRWNW',
        'target_price': '',
    }
    form = ProductURLForm(data=form_data)
    assert not form.is_valid()
    assert 'target_price' in form.errors

def test_invalid_target_price():
    form_data = {
        'url': 'https://www.amazon.com/dp/B08N5WRWNW',
        'target_price': 'not-a-number',
    }
    form = ProductURLForm(data=form_data)
    assert not form.is_valid()
    assert 'target_price' in form.errors
