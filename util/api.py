import requests
from util.util import logger


host = "https://www.mousehuntgame.com/"


def passiveHorn(token):
    url = "api/action/passiveturn"
    res = requests.post(host + url, data={
        "login_token": token
    })
    if 'error' not in res:
        logger.debug("Camp", "Passive horn initiated")
        return res.json()
    logger.error("Camp", "Passive horn data request failed.")
    return None


def activeHorn(token):
    url = "api/action/turn/me"
    res = requests.post(host + url, data={
        "login_token": token
    })
    if 'error' not in res:
        logger.debug("Camp", "Sounded horn.")
        return res.json()
    logger.error("Camp", "Active horn failed.")
    return None


def convertPotion(token, uh, product, qn, index):
    url = f'api/action/usepotion/{uh}/{product}/{qn}/{index}'
    res = requests.post(host + url, data = {
        "login_token": token
    })
    if 'error' not in res:
        logger.debug("Potion", f"Converted {qn} {product}")
        return res.json()
    logger.error("Potion", "Potion conversion failed.")
    return None


def purchase(token, item_index, quantity):
    url = f'api/action/purchase/{item_index}/{quantity}'
    res = requests.post(host + url, data = {
        "login_token": token
    })
    if 'error' not in res:
        logger.debug("Potion", f"Purchased {quantity} {item_index}")
        return res.json()
    logger.error("Potion", "Purchase failed.")
    return None


def setTrap(token, ids):
    url = "api/action/arm/" + ','.join(ids)
    res = requests.post(host + url, data={
        "login_token": token
    })
    if 'error' not in res:
        logger.debug("Set Trap", "Traps changed")
        return res.json()
    logger.error("Set Trap", "Trap Setting failed.")
    return None


def environmentApiCall(environment, token, body={}, post_url=''):
    url = f"api/action/quest/{environment}{post_url}"
    res = requests.post(host + url, data={**body, **{
        "login_token": token
    }})

    if 'error' not in res:
        logger.debug(environment, "Action triggered successfully")
        return res.json()
    logger.error(environment, res['error'])
    return None
