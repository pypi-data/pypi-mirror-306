import os

class Search():
    def __init__(self, fileTypes=[]) -> None:
        self.__fileTypes = fileTypes
        self.__files = []

    def getFilePaths(self, path):
        for dirPath, dirNames, fileNames in os.walk(path,topdown=True):
                for fileName in fileNames:
                    for fileType in self.__fileTypes:
                        if fileName.endswith("." + fileType):
                            filePath = os.path.join(dirPath, fileName)
                            self.__files.append(filePath)
            
        return self.__files