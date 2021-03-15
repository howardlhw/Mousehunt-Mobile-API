""" This is the main python execution loop """

import time
import traceback
import os
from datetime import datetime
from dotenv import load_dotenv
from questLocations.Main import MouseHunt
from util.util import logger

load_dotenv('.env')

def execute_script():
    """ This is the main execution script """
    load_dotenv()

    while True:
        try:
            current_hour = datetime.now().hour
            if 1<=current_hour<=6:
                logger.info("Snooze", "Sleeping Time")
                time.sleep(3600)
                continue

            user1 = {
                "login_token": os.getenv('USER1')
            }
            mh_main = MouseHunt(user1)
            mh_main.automateHunt()

            user2 = {
                "login_token": os.getenv('USER2')
            }
            mh_sashimi = MouseHunt(user2)
            mh_sashimi.automateHunt()
            time.sleep(120)

        except ValueError as value_error:
            print(str(value_error))
            traceback.print_exc()

if __name__ == "__main__":
    logger.info("Main", "Launching Application")
    execute_script()
