import os
import subprocess
from datetime import datetime
import shutil

class fioResultClass:
    fiomode = ""
    fionumj = ""
    fioSize = ""
    fioBlockSize = ""
    fioExtraArgs =  ""

class PyIOPlot:
    test_results = []
    # point this method to a result directory. 
    # It will iterate over all sub directories
    # and gather all data in a format to be plotted
    def resultIteration(self, resultDir):
        print("Iterating through all times")
        results = []
        for subdir, dirs, files in os.walk(resultDir):
            for file in files:
                if(os.path.isfile(os.path.join(subdir, file))):
                    filename, file_extension = os.path.splitext(file)
                    if file_extension == ".txt":
                        print (file)
                        print (os.path.join(subdir, file))
                        f = open(os.path.join(subdir, file))
                        results.append(f.read())
        return results
        
    # parsing method for compileBench raw text
    def parseCompileBench(outString):
        pos1 = outString.find("avg")
        pos2 = outString.find("B/s", pos1)#
        pos3 = outString.find("avg", pos2)
        pos4 = outString.find("B/s", pos3)#
        print(outString[pos1+4:pos2-2])
        print(outString[pos3+4:pos4-2])
        test_results.append(outString[pos1+4:pos2-2])
        test_results.append(outString[pos3+4:pos4-2])

    def getIoZoneResults(self, path):
        results = self.resultIteration(path)
        
    def getFioResults(self, path):
        results = self.resultIteration(path)
        for x in results:
            print(x)
