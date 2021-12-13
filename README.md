# morphBot
Code via 2bitcoder and CodetheThings

## Purpose
* To webscrape for popular products
* Check for inventory and pricing
* Add to Cart
* Checkout Purchase




# Usage

## Install
1. Python > 3.6
2. Packages
    1. time
    2. requests
    3. bs4
    4. pprint
    5. os
    6. json
    7. random
    8. multiprocessing
    9. termcolor

## Execution
1. Modify profiles.json and add any profiles per template
```
{
    "name": "",
    "firstName": "",
    "lastName": ""
}
```
2. Modify watchlist.json and add links to monitor per template
```
    {
        "site": "",
        "profile": "",
        "proxy": "",
        "quantity": 0,
        "desired": 1,
        "maxPrice": 0,
        "running": 1,
        "status": "Idle",
        "lastinstock": "",
        "taskId": ""
    }
```
3. Modify proxies.json and add proxies profiles per template
```
"myproxies":[
        "user:pass@ip:port",
        "user:pass@ip:port",
        "user:pass@ip:port"
    ]
```
4. Modify settings.json and modify thresholds
5. Run morphBot.py




# Current Functionality

## Amazon
    * Get Product Title
    * Get Pricing
    * Get Availability

## Best Buy
    * Get Product Title
    * Get Availability 

## Newegg 
    * Get Product Title
    * Get Availability