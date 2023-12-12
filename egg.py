import urllib.parse
import re
from dtos import Item
import databaseAccess as db
import smtplib
from email.message import EmailMessage

import requests
from bs4 import BeautifulSoup as BS

password = 'zbzifkbdbcugjddo'
email_sender = 'HealthHunterAuto@gmail.com'
email_receivers = ['lukas.madsen.brandt@gmail.com','krelledegn@gmail.com','lukas.second.brandt@gmail.com']
port = 587

baseUrl= "https://etilbudsavis.dk"
filter = "?business_ids=bdf5A%2Ca5aaT%2Chg_y5Q%2C71c90%2C0b1e8%2CDWZE1w%2C9ba51%2C11deC%2Cd311fg%2Cc1edq%2C267e1m%2CdcbaNL%2C603dfL%2Cdi314B%2C88ddE%2C93f13"

def getUrl(input: str):
    searchWord = urllib.parse.quote(input)
    return baseUrl + "/soeg/" + searchWord + filter

searchWords = [("skyr", "pr. liter"), ("æg", "pr. styk"), ("mælk", "pr. liter"), ("ærter", "pr. kg"), ("kylling", "pr. kg"), ("omega-3", "pr. styk"), ("whey", "pr. kg")]

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

floatPattern = r"\d+,?\d*"
items = {}
for searchWord, measurement in searchWords:
    items[searchWord] = {"topName": searchWord, "items": []}
    response = requests.get(getUrl(searchWord))
    print(getUrl(searchWord))
    soup = BS(response.content, "html.parser")

    headers = soup.find_all('header', string=lambda text: text is not None and matchOn(text, searchWord))

    for head in headers:
        li = head.findParent('li')

        if li:
            name = head.get_text(strip=True)
            link = li.find('a', href=True)['href'] if li.find('a', href=True) else "No link found"

            # Extract price per word
            spans = li.find_all('span')
            price_per_unit = (spans[1].get_text(strip=True) if spans else "No price").replace('•','')
            sanitizedPrice = float(re.search(floatPattern, price_per_unit).group().replace(',', '.'))
            timeframe = findDate(spans)

            # Store the item
            item = Item(searchWord, name, sanitizedPrice, baseUrl + link, timeframe, measurement)
            # db.insertItem(item) # Uncomment to insert into database

            items[searchWord]["items"].append(item)
  
def findCheapestItem(topWord: str):
    min = 10000000
    cheapestItem = None
    for item in items[topWord]["items"]:
        if min > item.price_per_unit:
            min = item.price_per_unit
            cheapestItem = item

    return cheapestItem

cheapestItems = []
for searchWord, _ in searchWords:
    cheapestItem = findCheapestItem(searchWord)
    if cheapestItem:
        cheapestItems.append(cheapestItem)

for cheapestItem in cheapestItems:
    print(cheapestItem)



for email_receiver in email_receivers:
    subject = "Her er de billigste varer på din Watchlist"
    body = ""
    for cheapestItem in cheapestItems:
        body += str(cheapestItem) + "\n\n"

    body += f"Data trukket fra \"{baseUrl}\""

    print("PREPARING")
    em = EmailMessage()
    em['From'] = email_sender
    em['to'] = email_receiver
    em['subject'] = subject
    em.set_content(body)


    print(em)


    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', port, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            print("Email sent successfully")
    except Exception as e:
        print("Error:", e)