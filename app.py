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
    stop_hour = 10
    start_hour = 10

    while True:
        try:
            current_hour = datetime.now().hour
            if stop_hour != start_hour:
                if stop_hour<=current_hour<=start_hour:
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
            mh_acc2 = MouseHunt(user2)
            mh_acc2.automateHunt('speedy')

        except Exception as general_error:
            print(str(general_error))
            traceback.print_exc()
            
        time.sleep(120)

if __name__ == "__main__":
    logger.info("Main", "Launching Application")
    execute_script()
