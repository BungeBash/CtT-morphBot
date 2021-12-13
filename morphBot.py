import time
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import os
import json
import random
from multiprocessing import Pool
from termcolor import colored
import smtplib
import pandas as pd

# Config files
configfiles = {
    'profiles': "config/profiles.json",
    'proxies': "config/proxies.json",
    'settings': "config/settings.json",
    'watchlist': "config/watchlist.json",
    'user': "config/user.json"
}


# Initialize config
profiles = None
proxies = None
settings = None
watchlist = None
user = None

# Functions
def get_session(proxylist):
    # construct an HTTP session
    session = requests.Session()
    # choose one random proxy
    proxy = random.choice(proxylist)
    session.proxylist = {"http": "http://"+proxy, "https": "http://"+proxy}
    return session


def scrape_amazon(listing):
    headers = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}) 
    if listing['proxy'] == 'None':
        s = requests.Session()
    else:
        s = get_session(proxies[listing['proxy']])
    instock = False
    page = s.get(listing['site'], headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    try:
        title = soup.find("span",attrs={"id": 'productTitle'}).string.strip().replace(',', '')
    except:
        title = "NA"
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')
    except:
        price = "NA"
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip().replace(',', '')
        if "In Stock" in available:
            listing['lastinstock'] = time.asctime(time.localtime(time.time()))
            print(colored("[IN STOCK] --- %s" % title,'green'))
            print(colored("%s - %s" % (price, listing['url']), 'cyan'))
            e.sendmail(u['username'],u['sendTo'])
            return listing
        else:
            print("[OOS] --- %s" % title)
            return None
    except:
        print("[OOS] --- %s" % title)
        return None


def scrape_bestbuy(listing):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
    }
    if listing['proxy'] == 'None':
        s = requests.Session()
    else:
        s = get_session(proxies[listing['proxy']])
    instock = False
    page = s.get(listing['site'], headers=headers)
    target_class = "fulfillment-add-to-cart-button"
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        results = soup.find(class_=target_class).find()
        add_to_cart_elements = results.find_all(type='button',class_='btn-primary')
        if len(add_to_cart_elements) > 0:
            instock = True
            listing['lastinstock'] = time.asctime(time.localtime(time.time()))
        title = soup.title.string
        if instock:
            print(colored("[IN STOCK] --- %s" % title, 'green'))
            print(colored("%s" % listing['url'], 'cyan'))
            e.sendmail(u['username'],u['sendTo'])
            return listing
        else:
            print("[OOS] --- %s" % title)
            return None
    except:
        print("error getting %s" % listing)


def scrape_newegg(listing):
    if listing['proxy'] == 'None':
        s = requests.Session()
    else:
        s = get_session(proxies[listing['proxy']])
    goodscrape = False
    instock = False
    page = s.get(listing['site'])
    target_class = "ProductBuy"
    soup = BeautifulSoup(page.content, 'html.parser')
    check = soup.find_all('div', class_='product-seller')
    if "Newegg" in str(check):
        goodscrape = True
    try:
        results = soup.find(id=target_class).find()
        add_to_cart_elements = results.find_all('button', class_='btn-primary')
        if len(add_to_cart_elements) > 0:
            instock = True
            listing['lastinstock'] = time.asctime(time.localtime(time.time()))
        title = soup.title.string
        if instock:
            print(colored("[IN STOCK] --- %s" % title,'green'))
            print(colored("%s" % listing['url'], 'cyan'))
            e.sendmail(u['username'],u['sendTo'])
            return listing
        else:
            if not goodscrape:
                print("POSSIBLE BAD SCRAPE")
            print("[OOS] --- %s" % title)
            return None
    except:
        print("error getting %s" % listing)

def scrape_target(listing):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
    }
    if listing['proxy'] == 'None':
        s = requests.Session()
    else:
        s = get_session(proxies[listing['proxy']])
    instock = False
    page = s.get(listing['site'])
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        results = soup.find('shipItButton')
        print(results)
        price = soup.find("span", {'data-test': 'product-price'})
        title = soup.find("span", {'data-test': 'product-title'})
        example = soup.findAll('div', attrs={'data-test':'shipItButton'})
        print(title)
        print(price)
        print(example)
    except:
        print("error getting %s" % listing)


def load_settings_from_file(targetfile):
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, targetfile)) as jsonfile:
        try:
            output = json.load(jsonfile)
            return output
        except json.JSONDecodeError as jsonerror:
            print("bad json in %s: \n%s" % (targetfile, jsonerror))
            return None


def update_config(config, configfile):
    # if config is not None:
    # import pdb; pdb.set_trace()
    new = load_settings_from_file(configfile)
    if new is not None:
        return new
    else:
        print("Cannot load %s" % configfile)
        if config is None:
            print("Exiting...")
            quit(1)
        else:
            print("Proceeding with previous values")
            return config


def update_files(config, configfile):
    if config is not None:
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, configfile), 'w') as f:
            json.dump(config, f, indent=4)


def main():
    # Amazon
    for i in watchlist['Amazon']:
        if i['running'] == 1:
            scrape_amazon(i)

    # Best Buy
    for i in watchlist['BestBuy']:
        if i['running'] == 1:
            scrape_bestbuy(i)

    # Newegg
    for i in watchlist['Newegg']:
        if i['running'] == 1:
            scrape_newegg(i)

# SMTP
u = load_settings_from_file(configfiles['user'])
e = smtplib.SMTP(u['smtp'], u['port'])
e.starttls()
e.login(u['username'], u['password'])

# Loop Checks
if __name__ == '__main__':
    while True:
        print(time.asctime(time.localtime(time.time())))
        print("Reloaded Configs")
        profiles = update_config(profiles, configfiles['profiles'])
        proxies = update_config(proxies, configfiles['proxies'])
        settings = update_config(settings, configfiles['settings'])
        watchlist = update_config(watchlist, configfiles['watchlist'])
        main()
        for i in watchlist:
            for s in watchlist[i]:
                if s['running'] == 0:
                    s['status'] = 'Idle'
                else:
                    s['status'] = 'Running'
        print(colored('Updating Configs...', 'yellow'))
        update_files(watchlist, configfiles['watchlist'])
        print(colored('Pausing...', 'yellow'))
        time.sleep(settings['Global']['retry'])