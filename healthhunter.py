import urllib.parse
import re
from dtos import Item, User
import databaseAccess as db
import smtplib
from email.message import EmailMessage

import requests
from bs4 import BeautifulSoup as BS

# Email configuration
password = 'zbzifkbdbcugjddo'
emailSender = 'HealthHunterAuto@gmail.com'
emailReceivers = ['kristian6710@gmail.com', 'lukas.second.brandt@gmail.com']
port = 587 # TLS port

baseUrl= "https://etilbudsavis.dk"
filter = "?business_ids=bdf5A%2Ca5aaT%2Chg_y5Q%2C71c90%2C0b1e8%2CDWZE1w%2C9ba51%2C11deC%2Cd311fg%2Cc1edq%2C267e1m%2CdcbaNL%2C603dfL%2Cdi314B%2C88ddE%2C93f13"

def getUrl(input: str):
    searchWord = urllib.parse.quote(input)
    return baseUrl + "/soeg/" + searchWord + filter

# Items in the watchlist
searchWords = [("skyr", "pr. liter"), ("æg", "pr. styk"), ("mælk", "pr. liter"), ("ærter", "pr. kg"), ("kylling", "pr. kg"), ("omega-3", "pr. styk"), ("whey", "pr. kg"), ("energidrik", "pr. liter")]

days = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag", "I morgen", "I dag"]

def findDate(spans):
    ret = ""
    # only want the last 4 spans, the 1 span and the 2 span is duplicated once
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
print( "Starting scraping..." )
i = 1
# Scrabing etilbudsavis.dk
for searchWord, measurement in searchWords:
    items[searchWord] = {"topName": searchWord, "items": []}
    response = requests.get(getUrl(searchWord))
    soup = BS(response.content, "html.parser")

    headers = soup.find_all('header', string=lambda text: text is not None and matchOn(text, searchWord))

    for head in headers:
        li = head.findParent('li')

        if li:
            name = head.get_text(strip=True)
            link = li.find('a', href=True)['href'] if li.find('a', href=True) else "No link found"

            # Extract price per word
            spans = li.find_all('span')
            pricePerUnit = (spans[1].get_text(strip=True) if spans else "No price").replace('•', '')
            sanitizedPrice = float(re.search(floatPattern, pricePerUnit).group().replace(',', '.'))
            timeframe = findDate(spans)

            # Store the item
            item = Item(searchWord, name, sanitizedPrice, baseUrl + link, timeframe, measurement)
            # db.insertItem(item) # Uncomment to insert into database

            items[searchWord]["items"].append(item)
    print(f"Finished scraping {searchWord} \n({i}/{len(searchWords)}) \n\n")
    i += 1
print("Finished scraping")

def findCheapestItem(topWord: str):
    min = 10000000
    cheapestItem = None
    for item in items[topWord]["items"]:
        if min > item.pricePerUnit:
            min = item.pricePerUnit
            cheapestItem = item

    return cheapestItem

# Add all cheapest items to a list
cheapestItems = []
for searchWord, _ in searchWords:
    cheapestItem = findCheapestItem(searchWord)
    if cheapestItem:
        cheapestItems.append(cheapestItem)

        
# Send the email to all receivers
print("Sending emails...")
emailErrors = []
for emailReceiver in emailReceivers:
    subject = "Her er de billigste varer på din Watchlist"
    body = ""
    # Add all the cheapest items to the body
    for cheapestItem in cheapestItems:
        body += str(cheapestItem) + "\n\n"
    body += f"Data trukket fra \"{baseUrl}\""

    # Create the email object
    em = EmailMessage()
    em['From'] = emailSender
    em['to'] = emailReceiver
    em['subject'] = subject
    em.set_content(body)


    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', port, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(emailSender, password)
            smtp.sendmail(emailSender, emailReceiver, em.as_string())
            print(f"Email sent to {emailReceiver}")
    except Exception as e:
        print("Error: ", e)
        emailErrors.append(emailReceiver)

print("Finished sending emails")
if len(emailErrors) > 0:
    print("Failed to send emails to: ", emailErrors)
        
