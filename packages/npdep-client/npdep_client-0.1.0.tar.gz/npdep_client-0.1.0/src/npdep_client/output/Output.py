import os
import time

from datetime import datetime

class Output():
    def __init__(self) -> None:
        self.startTime = time.time()

    def printHeader(self):
        print("################################################################################")
        print("")
        print("npdep-client")
        print("Network Protocol Data Exfiltration Project - A modular approach for data exfiltration")
        print("")
        print("Current working directory: " + os.getcwd())
        print("")
        print("Datetime: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("")
        print("################################################################################")
        print("")

    def printLoadingFromModulePath(self, path, src, trans):
        print("Load modules [Sourcing: " + src + ", Transfer: " + trans + "] from options path: " + path)
        print("")

    def printLoadingFromSitePkgs(self, src, trans):
        print("Load modules [Sourcing: " + src + ", Transfer: " + trans + "] from site packages")
        print("")

    def printExecutionTime(self):
        end = time.time()
        print("")
        print("################################################################################")
        print("")
        print("Execution Time: " + str(end-self.startTime)[0:8] + " sec")
        print("")