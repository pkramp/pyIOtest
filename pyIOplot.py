import os
import subprocess
from datetime import datetime, timedelta
import shutil
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

class fioResult:
    fiomode = ""
    fionumj = ""
    fioSize = ""
    fioBlockSize = ""
    fioExtraArgs =  ""
    readResult = ""
    writeResult = ""
    IOPs = ""
    timestamp = ""

class PyIOPlot:
    test_results = []
    startTime = 0
    workDir = ""
    
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
    def parseCompileBench(self, outString):
        pos1 = outString.find("avg")
        pos2 = outString.find("B/s", pos1)#
        pos3 = outString.find("avg", pos2)
        pos4 = outString.find("B/s", pos3)#
        print(outString[pos1+4:pos2-2])
        print(outString[pos3+4:pos4-2])
        test_results.append(outString[pos1+4:pos2-2])
        test_results.append(outString[pos3+4:pos4-2])
        
        
    def substrSearch(self, inString, key1, key2):
        pos1 = inString.find(key1)
        pos1 += len(key1)
        pos2 = inString.find(key2, pos1)
        return inString[pos1:pos2]
            
        
    def removeUnitAndMultiply(self, str):
        multiplier = 1.0
        unit = str[-1]
        str = str.replace(unit, '')
        # convert all units to MiB
        if unit == "K":
            multiplier = multiplier / 1024.0
        elif unit == "G":
            multiplier = multiplier * 1024.0
        num = float(str)
        num *= multiplier
        return num
        
    def parseFioResult(self, inString):
        results = []
        substr = self.substrSearch(inString, "READ: bw=", "iB/s")
        results.append(self.removeUnitAndMultiply(substr))
        
        substr = self.substrSearch(inString, "WRITE: bw=", "iB/s")
        results.append(self.removeUnitAndMultiply(substr))
        timestamp = self.substrSearch(inString, "TIME:", "\n")
        results.append(timestamp)
        return results
        

    def getIoZoneResults(self, path):
        results = self.resultIteration(path)
        
    def getFioResults(self, path):
        results = self.resultIteration(path)
        fioResults = []
        times = []
        readResults = []
        writeResults = []
        for x in results:
            fResult = self.parseFioResult(x)
            # only plot from start time
            testTime = datetime.strptime(fResult[2], "%d_%m_%Y-%H_%M_%S")
            if(self.startTime <= testTime):
                # get timedelta and save it
                timeD =  (testTime - self.startTime).total_seconds()
                fR = fioResult()
                fR.readResult = fResult[0]
                fR.writeResult = fResult[1]
                readResults.append(fResult[0])
                writeResults.append(fResult[1])
                times.append(timeD)
                fioResults.append(fR)

        readResults.sort()
        writeResults.sort()
        fig, ax = plt.subplots()
        readHandle, = ax.plot(times, readResults, label='Read performance')
        writeHandle, = ax.plot(times, writeResults, label='Write performance')
        ax.set_xlabel("Time since start in seconds")
        ax.set_ylabel("Throughput in MiB/s")
        ax.legend(handles=[readHandle, writeHandle])
        ax.set_title("Fio Results on " + self.workDir)
        plt.show()

    def plot(self, args):
        pyIOplot.startTime = datetime.strptime(args.timeStamp, "%d_%m_%Y-%H_%M_%S")
        pyIOplot.workDir = args.workdir
        pyIOplot.getFioResults(args.resultDir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process pyIO arguments.')
    parser.add_argument("workdir", help='Location where IO is done')
    parser.add_argument("resultDir", help='Location of results')
    parser.add_argument("timeStamp", help='Timestamp, from which one results will be considered for plotting')
    args = parser.parse_args()
    pyIOplot = PyIOPlot()
    pyIOplot.plot(args)
