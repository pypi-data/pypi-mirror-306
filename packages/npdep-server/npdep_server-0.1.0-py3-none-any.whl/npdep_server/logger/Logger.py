import os
import logging

class Logger():
    def __init__(self, logfilePath) -> None:
        logging.basicConfig(
            filename= os.path.join(logfilePath, "npdep-server.log"),
            format= "%(asctime)s | %(message)s",
            level=logging.INFO
        )

    def log(self, message):
        logging.info(message)
