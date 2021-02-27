import datetime
import logging
from config import MousehuntConfig



logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=MousehuntConfig.loggingLevel)

# def eprint(location, message):
        # self.t = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
#     print(f"[{t}] {location}: {message}")

class logger():
    
    @staticmethod
    def info(context, message):
        """ test class """
        logging.info(f'{context}: {message}')

    @staticmethod
    def debug(context, message):
        logging.debug(f'{context}: {message}')

    @staticmethod
    def error(context, message):
        logging.error(f'{context}: {message}')

        

def debug(message, debug=False):
    if debug:
        t = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        print(f"[{t}] DEBUG: {message}")

