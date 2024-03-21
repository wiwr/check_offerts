import requests
import time
import errno
import json
from datetime import datetime
from bs4 import BeautifulSoup


def pageRequest(url, cookies = {}):
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'}
    page = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def printDetails(storeName, price, currency, title):
    print(f'{storeName:15} {price:>10} {currency:3} {title:80.80}')


def textTillDash(text) -> str:
    dash_position = text.find('-')
    return text[:dash_position].strip()


def extractDetailsForAmazon(soup):
    title = soup.find(id="productTitle")
    if title is None:
       title = "Amazone without title"
    else:
        title = title.get_text().strip()
    try:
        input_price = soup.find(id="twister-plus-price-data-price")
        price = input_price['value']
        price = "{:.2f}".format(float(price))
    except:
        price = '---.--'
    
    try:
        input_curre = soup.find(id="twister-plus-price-data-price-unit")
        curre = input_curre['value']
    except:
        curre = '---'
    return price, curre, title


def extractDetailsForOleOle(soup):
    title_tag = soup.find('title')
    title = textTillDash(title_tag.text) if title_tag else "-"*20
    script_tags = soup.findAll('script', type='application/ld+json')
    script_tag = script_tags[1]
    script_json = script_tag.string.strip()
    script = json.loads(script_json)
    price = script['offers']['price'] 
    if price == None:
        price = "---.--"
    else:
        price = "{:.2f}".format(float(price))
    curre = script['offers']['priceCurrency']
    if curre == None:
        curre = "---"
    return price, curre, title


def extractDetailsForXKom(soup):
    title_tag = soup.find('title')
    title = textTillDash(title_tag.text) if title_tag else "-"*20
    price_tag = soup.find(attrs={"property": "product:price:amount"})
    price = "{:.2f}".format(float(price_tag['content'])) if price_tag else "---.--"
    curre = "---"
    return price, curre, title


def checkPrice(url, storeName):
    if storeName == "amazon.de" or storeName == "amazon.co.uk":
        cookies = {'i18n-prefs':'PLN'} 
    else: cookies = {} 
    soup = pageRequest(url, cookies)

    match storeName:
        case "amazon.de" | "amazon.pl" | "amazon.co.uk":
            returned = extractDetailsForAmazon(soup)
        case "x-kom.pl" | "al.to":
            returned = extractDetailsForXKom(soup)
        case "oleole.pl" | "euro.com.pl":
            returned = extractDetailsForOleOle(soup)
        case _:
            print(storeName)

    price, currency, title = returned    
    printDetails(storeName, price, currency, title)


def checkAmazon(prodID):
    checkPrice(f'https://www.amazon.de/-/pl/dp/{prodID}', 'amazon.de')
    checkPrice(f'https://www.amazon.pl/dp/{prodID}','amazon.pl')
    checkPrice(f'https://www.amazon.co.uk/dp/{prodID}','amazon.co.uk')


def checkXKom(prodID):
    checkPrice(f'https://www.x-kom.pl/p/{prodID}','x-kom.pl')
    checkPrice(f'https://www.al.to/p/{prodID}','al.to')


def checkOleOle(prodID):
    checkPrice(f'https://www.oleole.pl/{prodID}','oleole.pl')
    checkPrice(f'https://www.euro.com.pl/{prodID}','euro.com.pl')


if __name__ == "__main__":
    with open("list.json", 'r') as file:
        data = json.load(file)
        print("-"*80)
        for item in data['items']:
            print("Name:", item['name'])
            print("Description:", item['description'])

            for store in item['stores']:
                if store['store_name'] == 'Amazon':
                    checkAmazon(store['prod_id'].strip())
                elif store['store_name'] == 'OleOle':
                    checkOleOle(store['prod_id'].strip())
                elif store['store_name'] == 'x-kom':
                    checkXKom(store['prod_id'].strip())

            print("-"*80)
    #try:
        #file_name = "AmazonProdID.txt"
        #with open(file_name,"r") as file:
            #lines = file.readlines()
            #for line in lines:
                #checkAmazone(line.strip())
    #except IOError as e:
        #print(f'File name: {file_name}')
        #if e.errno == errno.ENOENT:
            #print("File not found!")
        #else:
            #print("An error occurred:", e)
#
    #try:
        #file_name = "OleOleProdID.txt"
        #with open(file_name,"r") as file:
            #lines = file.readlines()
            #for line in lines:
                #checkOleOle(line.strip())
    #except IOError as e:
        #print(f'File name: {file_name}')
        #if e.errno == errno.ENOENT:
            #print("File not found!")
        #else:
            #print("An error occurred:", e)
#
    #try:
        #file_name = "XKomProdID.txt"
        #with open(file_name,"r") as file:
            #lines = file.readlines()
            #for line in lines:
                #checkXKom(line.strip())
    #except IOError as e:
        #print(f'File name: {file_name}')
        #if e.errno == errno.ENOENT:
            #print("File not found!")
        #else:
            #print("An error occurred:", e)
