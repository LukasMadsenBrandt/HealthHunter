from email.message import EmailMessage
import ssl
import smtplib
import time
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

password = 'lydigtxjnucdxoda'
email_sender = 'auto.python.alerter@gmail.com'
email_receiver = 'lukas.madsen.brandt@gmail.com'

url = "https://www.tilbudsugen.dk/tilbud/æg"

# Configure the Selenium webdriver (make sure you have the appropriate driver executable installed)
driver = webdriver.Chrome()

# Open the URL in the webdriver
driver.get(url)

# Wait until the product elements are located and become visible
wait = WebDriverWait(driver, 30)

# Find the buttons element
button = driver.find_element(By.XPATH, '//*[@id="didomi-notice-disagree-button"]')
# Click the button
button.click()
#Click the filter button after finding it
filterbutton = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="outer-offer-container"]/div[2]/a')))
filterbutton.click()

# Wait until finding element in panels
panels = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mm-1"]')))

# Click the kæder button
kæder = driver.find_element(By.XPATH, '//*[@id="mm-1"]/ul[5]/li/a[2]')
kæder.click()

# Click the dagligvarer button
dagligvarer = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-5"]/ul/li[1]/a[2]')))
dagligvarer.click()

# Click all the places we want to buy eggs from
bilka = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[1]/label')))
bilka.click()

coop = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[2]/label')))
coop.click()

dagli = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[3]/label')))
dagli.click()

føtex = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[4]/label')))
føtex.click()

irma = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[5]/label')))
irma.click()

kvivkly = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[6]/label')))
kvivkly.click()

lidl = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[8]/label')))
lidl.click()

meny = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[10]/label')))
meny.click()

netto = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[12]/label')))
netto.click()

rema = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[13]/label')))
rema.click()

superbrugsen = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mm-6"]/ul/li[15]/label')))
superbrugsen.click()

exitpanel = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filters_mobile"]/div[1]/div/a[3]')))
exitpanel.click()

wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="outer-offer-container"]/div[3]/div[1]/a')))
time.sleep(2)
# Find the product elements again after applying the filter
product_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="outer-offer-container"]/div[3]/div[1]/a')))
listOfEggsOnSale = []
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
