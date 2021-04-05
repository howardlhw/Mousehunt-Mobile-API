from questLocations.FloatingIslands import FloatingIslands
from questLocations.BristleWoodsRift import BristleWoodsRift
from util.api import passiveHorn, activeHorn
from util.util import logger

class MouseHunt():
    """ This is the main mousehunt class that houses the quest locations """
    def __init__(self, config):
        self.config = config
        self.userdata = passiveHorn(config['login_token'])

    def checkActiveTurnAvailability(self):
        return self.userdata['user']['next_activeturn_seconds'] == 0

    def getEnvIds(self):
        """ Return the location of the user """
        return self.userdata['user']['environment_id']

    def getLocationObject(self, token, userdata, *args):
        """ resolve environment id and location objects """

        locations = {
            63: FloatingIslands(token, userdata, "floating_islands", *args),
            55: BristleWoodsRift(token, userdata, "rift_bristle_woods", *args)
        }

        if locations.get(self.getEnvIds()) == None:
            logger.debug("Main", "Location not available for automating.")
            return None
        return locations.get(self.getEnvIds())


    def automateHunt(self, *args):
        """ Main automation code """
        if self.checkActiveTurnAvailability():
            activeHorn(self.config['login_token'])

        questObj = self.getLocationObject(self.config['login_token'], self.userdata, *args)

        # Exit condition
        if questObj == None:
            return

        # Sound the horn if it's available.
        questObj.execute()