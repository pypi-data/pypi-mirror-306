import os
import time

from datetime import datetime

class Output():
    def __init__(self) -> None:
        self.startTime = time.time()

    def printHeader(self):
        print("################################################################################")
        print("")
        print("npdep-server")
        print("Network Protocol Data Exfiltration Project - A modular approach for data exfiltration")
        print("")
        print("Current working directory: " + os.getcwd())
        print("")
        print("Datetime: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("")
        print("################################################################################")
        print("")

    def printUpRunning(self):
        print("npdep-server up and running...")
        print("")

    def printLoadingFromModulePath(self, name, path):
        print("Load module [Receiver: " + name + "] from options path: " + path)
        print("")

    def printLoadingFromSitePkgs(self, name):
        print("Load module [Receiver: " + name + "] from site packages")
        print("")

    def printExecutionTime(self):
        end = time.time()
        print("")
        print("################################################################################")
        print("")
        print("Execution Time: " + str(end-self.startTime)[0:8] + " sec")
        print("")