import time
from questLocations.Main import MouseHunt
from util.util import logger
import traceback
import time
import os
from dotenv import load_dotenv



load_dotenv('.env')

def executeScript():
    load_dotenv()

    try:
        while True:
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
    logger.info("Main", "Lauching Application")
    executeScript()