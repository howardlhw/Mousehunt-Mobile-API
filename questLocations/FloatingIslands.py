from questLocations.questAbstraction import QuestAbstractions
from util.util import logger
from loadouts.library import library
import time

class FloatingIslands(QuestAbstractions):
    def isIslandFullyExplored(self):
        return self.userdata['user']['location_stats']['hunting_site_atts']['island_progress'] == 40

    def isAtLastPanel(self):
        return self.userdata['user']['location_stats']['hunting_site_atts']['island_progress'] > 29

    def distanceFromWarden(self):
        return self.userdata['user']['location_stats']['hunting_site_atts']['enemy_encounter_hunts_remaining']

    def has_defeated_enemy(self):
        return self.userdata['user']['location_stats']['hunting_site_atts']['has_defeated_enemy']

    def hasDefeatedWarden(self):
        return self.userdata['user']['location_stats']['hunting_site_atts']['has_defeated_enemy']

    def getIslandType(self):
        return self.userdata['user']['location_stats']['hunting_site_atts']['island_type']

    def isOnHighAltitudeIsland(self):
        return self.userdata['user']['location_stats']['hunting_site_atts']['is_high_tier_island'] == True

    def getBottledWindStatus(self):  # None if false
        return self.userdata['user']['location_stats']['hunting_site_atts']['is_fuel_enabled'] == True

    def getCorsairCheeseCount(self):
        for item in self.userdata['user']['inventory']:
            if item['item_id'] == 3090:
                return item['quantity']
        return 0

    def isAtHAI(self):
        return self.userdata['user']['location_stats']['hunting_site_atts']['sky_wardens_caught'] == 4

    def isArmingSavedSetup(self):
        # Added a bypass due to lack of charms
        if self.userdata['user']['trap']['trinket_id'] == None:
            return True

        return self.userdata['user']['location_stats']['saved_trap_setup']['is_active'] == True

    # Derived Methods
    def isAtLaunchPad(self):
        return self.getIslandType() == 'launch_pad_island'

    def isBattlingWarden(self):
        return self.distanceFromWarden() == 0 and \
            not self.has_defeated_enemy() and \
                not self.isOnHighAltitudeIsland()

    def isBattlingParagon(self):
        return self.distanceFromWarden() == 0 and \
            not self.has_defeated_enemy() and \
                self.isOnHighAltitudeIsland()

    def enableBottledWind(self):
        if self.getBottledWindStatus() == False:
            logger.info(self.environment, 'Enabled bottled wind.')
            self.toggleBottledWind()

    def disableBottledWind(self):
        if self.getBottledWindStatus() == True:
            logger.info(self.environment, 'Disabled bottled wind.')
            self.toggleBottledWind()

    # Actions
    def leaveTheIsland(self):
        res = self.action({'action': 'retreat'})
        logger.info(self.environment, f'Leaving the island')
        return res

    def toggleBottledWind(self):
        res = self.action({'action': 'toggle_fuel'})
        return res
    
    def useCyclone(self):
        res = self.action({'action': 'reroll'})
        logger.info(self.environment, f'Randomize Adventure Board')
        return res

    def launch(self, powertype):
        logger.info(self.environment, f'Launching to {powertype} island')
        res = self.action({
            'action': 'launch',
            'power_type': powertype,
            'use_saved_trap_setup': 0
        })
        return res

    def armSavedSetup(self):
        res = self.action({
            'action': 'arm_saved_setup'
        })
        logger.info(self.environment, f'Arming saved setup')
        return res

    # Computations
    def getSkyMapGrid(self):
        self.refreshUserData()
        squareArray = self.userdata['user']['location_stats']['board_grid_data']
        mainArray = []
        for array in squareArray:
            mainArray += array
        return [grid['type'] for grid in mainArray]

    def sortSkyMapGrid(self):
        grid = self.getSkyMapGrid()
        weaponMap = {
            'arcn': grid[0:4],
            'frgttn': grid[4:8],
            'hdr': grid[8:12],
            'shdw': grid[12:16],
            'drcnc': grid[12::-4],
            'law': grid[13::-4],  # verified
            'phscl': grid[14::-4],  # verified
            'tctcl': grid[15::-4],
        }
        return weaponMap

    def determineIslandTarget(self, mode='normal'):
        weaponMap = self.sortSkyMapGrid()

        # Debugging
        for power in weaponMap:
            logger.info(self.environment, f'{power} : {weaponMap[power]}')

        def assignScore(map):
            if map == 'ore_bonus':
                return 2
            if map == 'gem_bonus':
                return 2
            if map == 'sky_cheese':
                return 1
            if map == 'loot_cache':
                return 3
            if map == "sky_pirates":
                return 4
            if map[0:13] == 'paragon_cache':
                return 5
            if map[-6:] == 'shrine':
                return 5
            return 0

        # key is to make everything 3,2,1,0
        scoring = []
        logger.info(self.environment, f'{mode} mode grid search')

        for power in weaponMap:
            # Power skipping, if applicable
            # if power == "drcnc":
            #     eprint("Floating Islands", "Skipping Draconic")
            #     continue

            # Pirate Mode
            if mode == 'pirate':
                # Prioritize pirate hunting
                if weaponMap[power].count('sky_pirates') != 2:
                    continue
                if weaponMap[power][0] != 'sky_pirates':
                    continue

                skipping = True
                for slot in weaponMap[power]:
                    if slot[-6:] == 'shrine':
                        skipping = False
                if skipping:
                    continue
            
            # Pirate mode on high altitude island, prioritize pirate on high altitude
            elif mode == 'high_pirate':
                if not ('loot_cache' in weaponMap[power] and weaponMap[power].count('sky_pirates') == 2):
                    continue

            # Loot mode on high altitude island, prioritize pirate on loot
            elif mode == 'high_loot':
                if 'loot_cache' in weaponMap[power]:
                    print(f'{power}: {weaponMap[power]}')
                    print(f'gem bonus: {weaponMap[power].count("gem_bonus")}, ore bonus: {weaponMap[power].count("ore_bonus")}')

                    if not (weaponMap[power].count("gem_bonus") == 2 or weaponMap[power].count("ore_bonus") == 2):
                        print(f"{power}: not consideered")
                        continue

                elif not (weaponMap[power].count("gem_bonus") == 3 or weaponMap[power].count("ore_bonus") == 3):
                    print(f"{power}: not consideered")
                    continue

            # The first tile must be paragon or shrine
            else:
                if not (weaponMap[power][0][0:13] == 'paragon_cache'
                        or weaponMap[power][0][-6:] == 'shrine'):
                    continue

                # Count the number of empty skies
                noEmptySky = [
                    item for item in weaponMap[power] if item != 'empty_sky'
                ]
                if weaponMap[power][0][0:13] == 'paragon_cache':
                    if len(noEmptySky) < 4:
                        continue
                if weaponMap[power][0][-6:] == 'shrine':
                    if len(noEmptySky) < 2:
                        continue
            score = assignScore(weaponMap[power][0]) * 1000 + assignScore(
                weaponMap[power][1]) * 100 + assignScore(
                    weaponMap[power][2]) * 10 + assignScore(
                        weaponMap[power][3]) * 1
            scoring.append({"power": power, "score": score})

        newlist = sorted(scoring, key=lambda k: k['score'], reverse=True)

        for item in newlist:
            logger.info(self.environment, f'{item["power"]} : {weaponMap[item["power"]]}')
            return item['power']

    def armWardenSetup(self):
        status = False
        if self.getTrapSetup('weapon_id') != 2844:
            self.changeTrap(2844)
            logger.info(self.environment, 'Arming Smoldering Stone sentinel')
            status = True

        if self.getTrapSetup('bait_id') != 1967:
            self.changeTrap(1967)
            logger.info(self.environment, 'Arming empowered SB+')
            status = True

        if self.getTrapSetup('trinket_id') != 1651:
            self.changeTrap(1651)
            logger.info(self.environment, 'Arming Rift ultimate power charm')
            status = True

        if status:
            logger.info(self.environment, 'Armed warden setup, ready to battle.')


    def armParagonSetup(self):
        status = False
        if self.getTrapSetup('bait_id') != 1967:
            self.changeTrap(1967)
            logger.info(self.environment, 'Arming empowered SB+')
            status = True

        if self.getTrapSetup('trinket_id') != 1651:
            self.changeTrap(1651)
            logger.info(self.environment, 'Arming Rift ultimate power charm')
            status = True

        if status:
            logger.info(self.environment, 'Armed paragon setup, ready to battle.')


    def armPirateSetup(self):
        status = False
        if self.getTrapSetup('weapon_id') != 3152:
            self.changeTrap(3152)
            logger.info(self.environment, 'Arming S.S.S.S. Trap')  
            status = True

        if self.getTrapSetup('bait_id') != 3090:
            self.changeTrap(3090)
            logger.info(self.environment, 'Arming Pirate Cheese')
            status = True

        # if self.getTrapSetup('trinket_id') != 2121:
        #     self.changeTrap(2121)
        #     logger.info(self.environment, 'Arming Rift Ultimate Lucky Power charm')
        #     status = True

        if self.getTrapSetup('trinket_id') != 1651:
            self.changeTrap(1651)
            logger.info(self.environment, 'Arming Rift ultimate power charm')
            status = True

        if status:
            logger.info(self.environment, 'Armed pirate setup, ready to battle.')

    def execute(self):
        # Commence loop to scramble door until the preferred door is available
        while (True):
            # Determining the threshold to start hunting pirates.
            pirate_threshold = 123
            # Case 1 - at launch pad ready to go
            if self.isAtLaunchPad():
                while True:
                    power = None
                    # Determine the mode of moving to the islands
                    # if self.isAtHAI():
                    #     power = self.determineIslandTarget('high_pirate')
                    if self.isAtHAI():
                        # return # don't select island first
                        # power = self.determineIslandTarget() # Normal high speed hunting
                        # power = self.determineIslandTarget('high_pirate') # Double pirate icon mode
                        power = self.determineIslandTarget('high_loot')
                    elif self.getCorsairCheeseCount() >= pirate_threshold:
                        power = self.determineIslandTarget('pirate')
                    elif self.getCorsairCheeseCount() < pirate_threshold:
                        power = self.determineIslandTarget()

                    if power != None: break
                    if power == None:
                        logger.info(self.environment, f'No suitable island found, triggering cyclone.')
                        self.useCyclone()  # Troubleshoot first
                        time.sleep(5)

                self.launch(power)

                # If launching to pirate, equip pirate setup
                if self.getCorsairCheeseCount() >= pirate_threshold:
                    self.armPirateSetup()
                else:
                    self.armSavedSetup()
                return

            # Case 2, on the island
            else:
                # Case 2-1, leave the LAI if fully explored
                if self.isIslandFullyExplored() and not self.isOnHighAltitudeIsland() and not self.isBattlingWarden():
                    logger.info(self.environment, f'Low Altitude Island is fully explored.')
                    self.leaveTheIsland()
                    return

                # Case 2-2 determine trap setup for specific requirements
                if self.isBattlingWarden():
                    self.armWardenSetup()
                elif self.isBattlingParagon():
                    self.armParagonSetup()
                elif self.isOnHighAltitudeIsland():
                    if not self.isArmingSavedSetup():
                        logger.info(self.environment, f'On high altitude island, arm saved setup.')
                        self.armSavedSetup()

                # Actions here are for low altittude islands, hunt pirate if has enough cheese
                # Else hunt normally.
                elif self.getCorsairCheeseCount() >= pirate_threshold: 
                    self.armPirateSetup()
                elif self.getCorsairCheeseCount() < pirate_threshold:
                    if not self.isArmingSavedSetup():
                        logger.info(self.environment, f'Low on corsair cheese, arming saved setup.')
                        self.armSavedSetup()

                # Ensure the bottled wind is on
                if self.isIslandFullyExplored():
                    self.disableBottledWind()
                else:
                    self.enableBottledWind()

            return

