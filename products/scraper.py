import os
import time
import csv
import datetime
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Load env variables
load_dotenv()
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')
APP_PASSWORD = os.getenv('APP_PASSWORD')  # Gmail App Password
CHROME_DRIVER_PATH = '/path/to/chromedriver'  # Update this if needed
CSV_FILE = '/Users/younki/Downloads/AmazonWebScraperDataSet.csv'

# Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def get_product_info(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.visibility_of_element_located((By.ID, 'productTitle')))
    time.sleep(2)
    
    try:
        title = driver.find_element(By.ID, 'productTitle').text.strip()
        price_symbol = driver.find_element(By.CLASS_NAME, 'a-price-symbol').text.strip()
        price_whole = driver.find_element(By.CLASS_NAME, 'a-price-whole').text.strip()
        price_fraction = driver.find_element(By.CLASS_NAME, 'a-price-fraction').text.strip()
        price_str = f'{price_symbol}{price_whole}.{price_fraction}'
        price_float = float(price_whole.replace(',', '') + '.' + price_fraction)
    except Exception as e:
        print("❌ Could not get product data:", e)
        title, price_str, price_float = "N/A", "N/A", None

    driver.quit()
    return title, price_str, price_float

def save_to_csv(title, price_str):
    today = datetime.date.today()
    header = ['Title', 'Price', 'Date']
    data = [title, price_str, today]

    file_exists = os.path.isfile(CSV_FILE)
    write_header = not file_exists or os.path.getsize(CSV_FILE) == 0

    try:
        with open(CSV_FILE, 'a+', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(header)
            writer.writerow(data)
    except Exception as e:
        print("CSV Error:", e)

def send_mail(subject, body):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(EMAIL_SENDER, APP_PASSWORD)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg)
        server.quit()
        print("📧 Email sent!")
    except Exception as e:
        print("❌ Email failed:", e)

def send_price_alert(title, url, price_float):
    subject = f"Price Alert! '{title}' is now ${price_float}!"
    body = f"The item you wanted is below your target price.\nCheck it out here: {url}"
    send_mail(subject, body)
