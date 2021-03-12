import time
from questLocations.Main import MouseHunt
from util.util import logger
import traceback
import time
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env')

def executeScript():
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
            mh = MouseHunt(user1)
            mh.automateHunt()

            user2 = {
                "login_token": os.getenv('USER2')
            }
            mh2 = MouseHunt(user2)
            mh2.automateHunt()
            time.sleep(120)

        except Exception as e:
            print(str(e))
            traceback.print_exc()

if __name__ == "__main__":
    logger.info("Main", "Launching Application")
    executeScript()