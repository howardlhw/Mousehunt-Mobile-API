from abc import ABC
from util.api import setTrap, environmentApiCall, passiveHorn
import requests
from util.util import logger

class QuestAbstractions(ABC):
    def __init__(self, login_token, userdata, environment, *args):
        self.login_token = login_token
        self.userdata = userdata
        self.environment = environment
        self.args = args

    def refreshUserData(self):
        self.userdata = passiveHorn(self.login_token)
        return self.userdata

    def getUserData(self):
        return self.userdata

    def action(self, body):
        if self.environment == None:
            logger.error("Environment", "Environment is missing from api call.")
        return environmentApiCall(self.environment, self.login_token, body)

    def changeTrap(self, ids):
        if ids.__class__ == int:
            ids = [str(ids)]
        else:
            ids = [str(id) for id in ids]
        res = setTrap(self.login_token, ids)
        return res

    def debug(self):
        print(self.userdata['user']['location_stats'])

    def printCurrentTrapID(self):
        print(f"Bait: {self.userdata['user']['trap']['bait_id']}")
        print(f"Weapon: {self.userdata['user']['trap']['weapon_id']}")
        print(f"Base: {self.userdata['user']['trap']['base_id']}")
        print(f"Trinket: {self.userdata['user']['trap']['trinket_id']}")

    def getCurrentID(self, item):
        # Item can be trinket_id ,bait_id, base_id
        return self.userdata['user']['trap'][item]