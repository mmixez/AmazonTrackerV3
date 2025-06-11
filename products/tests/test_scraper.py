import pytest
import os
import csv
from unittest import mock
from products.scraper import get_product_info, save_to_csv, send_price_alert


# --- Mocks for Selenium WebDriver ---

class MockWebElement:
    def __init__(self, text):
        self.text = text

class MockDriver:
    def __init__(self):
        self.calls = []

    def get(self, url):
        self.calls.append(('get', url))

    def find_element(self, by, value):
        # Return mocked elements based on selector name
        if value == 'productTitle':
            return MockWebElement("Test Product Title")
        elif value == 'a-price-symbol':
            return MockWebElement("$")
        elif value == 'a-price-whole':
            return MockWebElement("123")
        elif value == 'a-price-fraction':
            return MockWebElement("45")
        else:
            raise Exception("Element not found")

    def quit(self):
        self.calls.append(('quit',))

# Patch webdriver.Chrome to return the MockDriver instance
@pytest.fixture
def mock_chrome(monkeypatch):
    monkeypatch.setattr("products.scraper.webdriver.Chrome", lambda **kwargs: MockDriver())

def test_get_product_info_success(mock_chrome):
    title, price_str, price_float = get_product_info("https://fake-url.com/product")
    assert title == "Test Product Title"
    assert price_str == "$123.45"
    assert price_float == 123.45

def test_get_product_info_fail(monkeypatch):
    # Simulate element not found exception
    class FailDriver:
        def get(self, url):
            pass
        def find_element(self, by, value):
            raise Exception("Element not found")
        def quit(self):
            pass

    monkeypatch.setattr("products.scraper.webdriver.Chrome", lambda **kwargs: FailDriver())


    title, price_str, price_float = get_product_info("https://fake-url.com/fail")
    assert title == "N/A"
    assert price_str == "N/A"
    assert price_float is None

def test_save_to_csv(tmp_path):
    test_file = tmp_path / "test.csv"
    with mock.patch("products.scraper.CSV_FILE", str(test_file)):
        save_to_csv("Test Product", "$99.99")
        # File should have header + 1 data row
        with open(test_file, newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert rows[0] == ['Title', 'Price', 'Date']
            assert rows[1][0] == "Test Product"
            assert rows[1][1] == "$99.99"

@mock.patch("products.scraper.smtplib.SMTP_SSL")
def test_send_price_alert(mock_smtp):
    mock_server = mock.Mock()
    mock_smtp.return_value = mock_server

    send_price_alert("Test Product", "http://example.com", 50.0)

    mock_smtp.assert_called_once_with('smtp.gmail.com', 465)
    mock_server.login.assert_called_once()
    mock_server.sendmail.assert_called_once()
    mock_server.quit.assert_called_once()
