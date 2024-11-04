import os
import time

from datetime import datetime

class Output():
    def __init__(self) -> None:
        self.startTime = time.time()

    def printHeader(self):
        print("################################################################################")
        print("")
        print("NPDEP - Network Protocol Data Exfiltration Project")
        print("foi - files of interest")
        print("Identifies files based on their file type")
        print("")
        print("Current working directory: " + os.getcwd())
        print("")
        print("Datetime: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("")
        print("################################################################################")
        print("")

    def printFileTypes(self, types):
        print("Files to be searched: " + str(types))
        print("")

    def printPath(self, path):
        print("Path: " + path)
        print("")

    def printResult(self, paths):
        print("Files found:")
        print("---")
        for path in paths:
            print(path)

    def printExecutionTime(self):
        end = time.time()
        print("")
        print("################################################################################")
        print("")
        print("Execution Time: " + str(end-self.startTime)[0:8] + " sec")
        print("")