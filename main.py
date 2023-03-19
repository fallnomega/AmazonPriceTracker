from bs4 import BeautifulSoup
import requests
import smtplib
import os

PRODUCT_URL = 'https://www.amazon.com/dp/B07S9KKGHQ?tag=camelsearches-20&linkCode=ogi&th=1&psc=1&language=en_US'

HEADERS = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/111.0.0.0 Safari/537.36", "accept-language": "en-US,en;q=0.9"}

amazon_request = requests.get(url=PRODUCT_URL, headers=HEADERS)
amazon_request.raise_for_status()
soup = BeautifulSoup(amazon_request.text, "lxml")
product = soup.find_all("div", {"id": "titleSection"})
price = soup.find_all("div", class_="a-section a-spacing-micro")

price = price[0].getText().split('$')
price = float(price[1])

print(product[0].getText().strip(' '))
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

if price < 1000:
    print(price)
    email = EMAIL
    password = PASSWORD
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.ehlo()
    connection.starttls()
    connection.login(user=email, password=password)
    connection.sendmail(from_addr=email,
                        to_addrs=f"{EMAIL}",
                        msg=f"Subject:AMAZON PRICE ALERT!\n\n{product[0].getText().strip(' ')} is now {price}")
    connection.close()
