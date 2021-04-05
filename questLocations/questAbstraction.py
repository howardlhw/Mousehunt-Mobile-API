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