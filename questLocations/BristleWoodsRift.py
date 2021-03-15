from questLocations.questAbstraction import QuestAbstractions
from loadouts.bristleWoodsRiftLoadout import loadouts
from loadouts.library import library
from random import randint
from util.api import convertPotion, purchase
from util.util import logger


class BristleWoodsRift(QuestAbstractions):
    def getCurrentPortals(self):
        return [
            portal['type']
            for portal in self.userdata['user']['location_stats']['portals']
        ]

    def isPortalsOpened(self):
        currentPortals = self.getCurrentPortals()
        if 'closed' in currentPortals and len(list(set(currentPortals))) == 1:
            return False
        return True

    def getItemsCount(self, itemName):
        return int(self.userdata['user']['location_stats']['items'][itemName]['quantity'])

    def isStatusEffectsActive(self, effect):
        return self.userdata['user']['location_stats']['status_effects'][effect] == 'active'

    def isItemActive(self, itemName):
        status = ['selected']
        return self.userdata['user']['location_stats']['items'][itemName]['status'] in status

    def getObeliskCharge(self):
        return self.userdata['user']['location_stats']['obelisk_percent']

    def toggleQuantumQuarts(self):
        res = self.action({'action': 'toggle_loot_boost'})
        return res

    def scramblePortal(self):
        res = self.action({'action': 'scramble_portals'})
        return res

    def convertPotionToCheese(self, potion, quantity):
        res = convertPotion(self.login_token, self.userdata['user']['uh'], potion, quantity, 0)
        return res

    # Common Actions
    def chamberTrapSetup(self, loadout):
        # Quantum Quarts Setup
        if loadout['quantumQuarts'] and not self.isItemActive('rift_quantum_quartz_stat_item'):
            self.toggleQuantumQuarts()
        if not loadout['quantumQuarts'] and self.isItemActive('rift_quantum_quartz_stat_item'):
            self.toggleQuantumQuarts()

        # Then trap setup
        self.changeTrap([
            library[loadout['bait']],
            library[loadout['trinket']]
        ])

    def selectChamber(self, portalName):
        # NOT TESTED AND CHECKED
        """
        Chamber Options
        acolyte_chamber: Acolyte Chamber
        magic_chamber: Runic Laboratory
        potion_chamber : Ancient Laboratory
        timewarp_chamber: Timewarp Chamber
        guard_chamber : Guard barracks
        silence_chamber : Silent Chamber
        hidden_treasury : Hidden Treasury
        lucky_chamber : Lucky Tower

        Useless Chambers
        icy_chamber: Frozen Alcove
        ingress_chamber: Ingress Chamber
        basic_chamber: Gearworks
        
        """
        res = self.action({
            'action': 'enter_portal',
            'chamber_type': portalName
        })
        # logger.info(self.environment, f'Entering {portalName}')
        return res

    # Chamber condition setters
    def determineChamberToEnter(self, mode):
        """
        This method determines the chamber to enter, the priorities are:
        1. Enter Security Chamber to disable alarm
        2. Enter Guard Barracks if the alarm was triggered
        3. Hidden Treasury for gold
        4. Then Lucky tower for loot
        5. Acolyte Chamber if conditions are met
        6. Timewarp chamber if conditions are met
        7. runic chamber if all else fails
        8. ancient chamber if oh well....
        9. Gear works, seriously?
        10. Enter the tower
        11. Never bother to enter ingress chamber

        returns the name of the chamber
        """

        portals = self.getCurrentPortals()
        portals = list(set(portals))
        logger.info(self.environment, portals)

        aa_sand_threshold = 38  # For entering acolyate chamber
        runic_threshold = aa_sand_threshold  # For entering acolyate chamber
        runic_upper_threshold = 400 # For stop entering runic chambers
        timewramp_runicRqd_thresdhold = 40 # Required amount of runic cheese before enteiring timewarp

        # Banished chambers
        if 'ingress_chamber' in portals:
            portals.remove('ingress_chamber')

        if 'basic_chamber' in portals:
            portals.remove('basic_chamber')

        # Loop begin
        if 'entrance_chamber' in portals:
            logger.info(self.environment, "Starting the loop again....")
            return 'basic_chamber'

        # Go straight to the AA under speedy and can afford to scramble
        if mode == 'speedy':
            if 'magic_chamber' in portals and self.getItemsCount('rift_scramble_portals_stat_item')>3:
                portals.remove('magic_chamber')

            if 'potion_chamber' in portals and self.getItemsCount('rift_scramble_portals_stat_item')>3:
                portals.remove('potion_chamber')

        # Condition 1s - Always enter
        if 'guard_chamber' in portals:
            # logger.info(self.environment, "Entering Guard Barracks")
            return 'guard_chamber'

        # Actively remove the status effect, if inflicted.
        if self.isStatusEffectsActive('un') and 'silence_chamber' not in portals:
            logger.info(self.environment, "Scrambling for security chamber")
            return None

        # Condition 1s - Always enter
        if 'silence_chamber' in portals:
            # logger.info(self.environment, "Entering Silence Chamber")
            return 'silence_chamber'

        # Condition 1s - Always enter
        if 'security_chamber' in portals:
            # logger.info(self.environment, "Entering Security Chamber")
            return 'security_chamber'

        # Condition - Enter Acolyte chamber if all conditions are met
        if self.getItemsCount('rift_hourglass_sand_stat_item') > aa_sand_threshold and \
            self.getItemsCount('runic_string_cheese') > runic_threshold and \
                self.isStatusEffectsActive('ng') and \
                    'acolyte_chamber' in portals:
            logger.info(self.environment, "Acolyte Condiiton met, entering chamber")
            return 'acolyte_chamber'

        # Condition - Money is money
        if 'lucky_chamber' in portals:
            # logger.info(self.environment, "Entering Lucky Chamber.")
            return 'lucky_chamber'

        # Condition - Money is money
        if 'treasury_chamber' in portals:
            # logger.info(self.environment, "Entering Treasury Chamber.")
            return 'treasury_chamber'

        # Condition - Don't get into timewarp if not enough runic cheese
        if 'timewarp_chamber' in portals and \
            self.getItemsCount('rift_hourglass_sand_stat_item') <= aa_sand_threshold and \
                self.getItemsCount('runic_string_cheese') > timewramp_runicRqd_thresdhold:
            logger.info(self.environment, "Gathering hourglass sand.")
            return 'timewarp_chamber'

        # Condition - Don't get into timewarp if have enough time sand
        if 'timewarp_chamber' in portals and \
            self.getItemsCount('rift_hourglass_sand_stat_item') > aa_sand_threshold:
            logger.info(self.environment, "Removing timewarp due to sufficient time sand.")
            portals.remove('timewarp_chamber')

        # Condition - Get runic string cheese, but not too much
        if 'magic_chamber' in portals and self.getItemsCount('runic_string_cheese') <= runic_upper_threshold:
            logger.info(self.environment, "Gathering Runic cheese.")
            return 'magic_chamber'

        if 'potion_chamber' in portals:
            logger.info(self.environment, "Gathering Ancient String cheese.")
            return 'potion_chamber'

        if self.getItemsCount('rift_scramble_portals_stat_item') < 2:
            logger.info(self.environment, "Critically low portal scramblers.")
            initialPortals = list(set(self.getCurrentPortals()))
            if 'potion_charmber' in initialPortals:
                return 'potion_chamber'

            if 'magic_chamber' in initialPortals:
                return 'magic_chamber'

            return initialPortals[0]

        logger.info(self.environment, "No suitable portal, scrambling.")
        return None


    # Main Automation
    def execute(self, mode=None):
        sandCount = ''

        # Brew the potions, if any
        if self.getItemsCount('ancient_string_cheese_potion') > randint(6, 10):
            self.convertPotionToCheese('ancient_string_cheese_potion', self.getItemsCount('ancient_string_cheese_potion'))
        if self.getItemsCount('runic_string_cheese_potion') > randint(4, 10):
            self.convertPotionToCheese('runic_string_cheese_potion', self.getItemsCount('runic_string_cheese_potion'))

        # Toggle for the case at acolyte chamber
        if self.getObeliskCharge() == 100 and self.isItemActive('rift_quantum_quartz_stat_item'):
            self.toggleQuantumQuarts()
            self.changeTrap(2322)
            logger.info(self.environment, "Obelisk fully charged, disable Quantum Quarts.")


        # Refil brie string cheese if running low
        if self.getItemsCount('brie_string_cheese') < 200:
            purchase(self.login_token, 1424, 30)
            logger.info(self.environment, "Purchased 30 brie string cheese.")

        # End loop if portals are closed
        if not self.isPortalsOpened():
            return

        # # Select the portal and enter the chamber, then change trap setup
        determinedPortal = self.determineChamberToEnter(mode)
        if determinedPortal == None:
            self.scramblePortal()
            return

        sandCount += 'with sandCount ' + str(self.getItemsCount("rift_hourglass_sand_stat_item"))
        logger.info(self.environment, f'Entering {determinedPortal} {sandCount}')
        self.selectChamber(determinedPortal)
        self.chamberTrapSetup(loadouts[determinedPortal])
        return