from email.message import EmailMessage
import ssl
import smtplib
import time
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

password = 'lydigtxjnucdxoda'
email_sender = 'auto.python.alerter@gmail.com'
email_receiver = 'lukas.madsen.brandt@gmail.com'

url = "https://etilbudsavis.dk/soeg/%C3%A6g?price_range.per_unit=piece&price_range.max=40&business_ids=bdf5A%2C0b1e8%2C71c90%2CDWZE1w%2Cc1edq%2Cd311fg%2C11deC%2C9ba51%2C93f13%2C88ddE%2C603dfL%2Cdi314B"

response = requests.get(url)
soup = BS(response.content, "html.parser")

print(soup)
#cleanup = BS.find_all('//*[@id="main"]/div/div/div/div[2]/div/ul')

'''
# Find the product elements again after applying the filter
product_elements = 
listOfEggsOnSale = []
keywords = ["økologiske æg", "skrabeæg", "frilandsæg"]

for element in product_elements:
    
    product_name = element.text
    if product_name in keywords:
        
'''
'''
# Iterate over each product element and extract the information
for product_element in product_elements:
    
    # Check if the product element contains the desired certificate div and img tags
    certificate_div = product_element.find_elements(By.XPATH, './/div[contains(@class, "certificates-imgs")]//img[@alt="Økologisk"]')
    if certificate_div:
        
        # Extract the product name
        product_name = product_element.text

        # Find the corresponding price element for the product
        price_element = product_element.find_element(By.XPATH, './/div[@class="product_price_pcs"]/div[@class="price"]')

        # Extract the price text
        price_text = price_element.text

        # Remove any non-digit characters from the price text
        price_text = ''.join(filter(str.isdigit, price_text))

        # Convert the price to a float
        price_text = price_text.replace(",",".")
        price = float(price_text) /100

        # Check if the price per egg is below 2.5 kr
        if price < 2.5:
            # Print the product, price, and price per egg
            #print(f"Product: {product_name}")
            #print(f"Price: {price} kr")
            #print("-------------------------")
            listOfEggsOnSale.append(product_name)

# Close the webdriver
driver.quit()
subject = f"Økologiske æg på tilbud!"
body = "Her er ugens tilbud på økologiske æg: \n \n"
for i in range (len(listOfEggsOnSale)):
    body += listOfEggsOnSale[i] + "\n\n"

body += f"Data trukket fra \"{url}\""
print(subject)
print(body)
print(f"Mail sent to \"{email_receiver}\"")


em = EmailMessage()
em['From'] = email_sender
em['to'] = email_receiver
em['subject'] = subject
em.set_content(body)


context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
    smtp.login(email_sender, password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
'''