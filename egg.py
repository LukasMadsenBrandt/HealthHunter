from dataclasses import dataclass
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
import urllib.parse

password = 'lydigtxjnucdxoda'
email_sender = 'auto.python.alerter@gmail.com'
email_receiver = 'lukas.madsen.brandt@gmail.com'

baseUrl= "https://etilbudsavis.dk/soeg/"
query = "?price_range.per_unit=piece&price_range.max=40&business_ids=bdf5A%2C0b1e8%2C71c90%2CDWZE1w%2Cc1edq%2Cd311fg%2C11deC%2C9ba51%2C93f13%2C88ddE%2C603dfL%2Cdi314B"

def getUrl(input: str):
    searchWord = urllib.parse.quote(input)
    return baseUrl + searchWord + query

searchWords = ["skyr", "æg", "mælk"]
days = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag", "I morgen", "I dag"]
def findDate(spans):
    ret = ""
    # i only want the last 4 spans
    spans = spans[-4:]
    if spans[0].text in days:
        ret += spans[0].text + " til " + spans[3].text
    else:
        ret = "I dag til " + spans[3].text
    return ret

def matchOn(text: str, match: str):
    input = text.lower()
    if match in input:
        return True
    else:
        return False

@dataclass
class Item:
    topName: str
    name: str
    price: str
    link: str
    timeframe: str


items = {}
cheapestItems = []
for word in searchWords:
    items[word] = {"topName": word, "items": []}
    response = requests.get(getUrl(word))
    soup = BS(response.content, "html.parser")

    headers = soup.find_all('header', string=lambda text: text is not None and matchOn(text, word))

    for head in headers:
        li = head.findParent('li')
        if li:
            name = head.get_text(strip=True)
            link = li.find('a', href=True)['href'] if li.find('a', href=True) else "No link found"

            # Extract price per egg
            spans = li.find_all('span')
            price_per_unit = (spans[1].get_text(strip=True) if spans else "No price").replace(',', '.')

            timeframe = findDate(spans)

            # Store the item
            item = Item(word, name, price_per_unit, link, timeframe)

            items[word]["items"].append(item)
            # Cheapest Item
            cheapestItem = min(items[word]["items"], key=lambda x: float(x.price.split()[0].replace(',', '.')), default=None)
            cheapestItems.append(cheapestItem)
  

for cheapestItem in cheapestItems:
    print(cheapestItem)

# subject = f"Æg på tilbud!"
# body = "Her er ugens tilbud på æg: \n \n"
# for item in items:
#     # print the keys with the value in a new line
#     body += "\n".join(f"{key}: {value}" for key, value in item.items())
#     body += "\n \n"
#
# url = getUrl("æg")
# body += f"Data trukket fra \"{url}\""
# #print(subject)
# print(body)
# print(f"Mail sent to \"{email_receiver}\"")

'''
em = EmailMessage()
em['From'] = email_sender
em['to'] = email_receiver
em['subject'] = subject
em.set_content(body)


context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
    smtp.login(email_sender, password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())


print("SENT")'''