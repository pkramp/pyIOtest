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
                        f = open(os.path.join(subdir, file))
                        results.append(f.read())
        return results
    
    # search for two keys in a string and return the substring
    def substrSearch(self, inString, key1, key2):
        pos1 = inString.find(key1)
        pos1 += len(key1)
        pos2 = inString.find(key2, pos1)
        return inString[pos1:pos2]
            
    def removeUnitAndMultiply(self, str, ibi):
        multiplier = 1.0
        unit = str[-1]
        str = str.replace(unit, '')
        # convert all units to MiB
        if unit == "K":
            multiplier = multiplier / (1024.0 if ibi else 1000.0)
        elif unit == "G":
            multiplier = multiplier * (1024.0 if ibi else 1000.0)
        num = float(str)
        num *= multiplier
        return num
                
    # parsing method for compileBench raw text
    def parseCompileBench(self, inString):
        searchStrings = ["intial create total runs", ")\ncreate total runs", 
        "patch total runs", "compile total runs ", "clean total runs", 
        "read tree total runs", "read compiled tree total runs " ]
        results = []
        for searchString in searchStrings:
            subs = self.substrSearch(inString, searchString, "MB/s")
            subs = self.substrSearch(subs, "avg ", "\n")
            results.append(subs)
        # also get timestamp
        timestamp = self.substrSearch(inString, "TIME:", "\n")
        results.append(timestamp)
        return results

    def parseFioResult(self, inString):
        results = []
        substr = self.substrSearch(inString, "READ: bw=", "iB/s")
        results.append(self.removeUnitAndMultiply(substr, True))
        
        substr = self.substrSearch(inString, "WRITE: bw=", "iB/s")
        results.append(self.removeUnitAndMultiply(substr, True))
        timestamp = self.substrSearch(inString, "TIME:", "\n")
        results.append(timestamp)
        return results

    def getCompileBenchResults(self, path):
        initCreate = []
        create = []
        patch = []
        compile = []
        clean = []
        readTree = []
        readCompiled = []
        times = []
        # gather all result texts from given path
        results = self.resultIteration(path)
        for result in results:
            cbResult = self.parseCompileBench(result)
            testTime = datetime.strptime(cbResult[7], "%d_%m_%Y-%H_%M_%S")
            if(self.startTime <= testTime):
                print(cbResult)
                initCreate.append(float(cbResult[0]))
                create.append(float(cbResult[1]))
                patch.append(float(cbResult[2]))
                compile.append(float(cbResult[3]))
                clean.append(float(cbResult[4]))
                readTree.append(float(cbResult[5]))
                readCompiled.append(float(cbResult[6]))
                timeD =  (testTime - self.startTime).total_seconds()
                times.append(timeD)

        # get the order in which the results should be plotted
        order = np.argsort(times)
        # order times, readResults and writeResults
        times = np.array(times)[order]
        initCreate = np.array(initCreate)[order]
        create = np.array(create)[order]
        patch = np.array(patch)[order]
        compile = np.array(compile)[order]
        clean = np.array(clean)[order]
        readTree = np.array(readTree)[order]
        readCompiled = np.array(readCompiled)[order]
        # now do the plotting
        fig, ax = plt.subplots()
        initCreateHandle, = ax.plot(times, initCreate, label='Initial create performance')
        createHandle, = ax.plot(times, create, label='Create performance')
        patchHandle, = ax.plot(times, patch, label='Patch performance')
        compileHandle, = ax.plot(times, compile, label='Compile performance')
        #cleanHandle, = ax.plot(times, clean, label='Clean performance')
        readTreeHandle, = ax.plot(times, readTree, label='readTree performance')
        #readCompiledHandle, = ax.plot(times, readCompiled, label='readCompiled performance')
        
        ax.set_xlabel("Time since start in seconds")
        ax.set_ylabel("Throughput in MB/s")
        ax.legend(handles=[initCreateHandle, createHandle, patchHandle, compileHandle, readTreeHandle])
        ax.set_title("Compilebench results on " + self.workDir)
        plt.show()
        
        

    def getIoZoneResults(self, path):
        results = self.resultIteration(path)
        
    def getFioResults(self, path):
        results = self.resultIteration(path)
        fioResults = []
        times = []
        readResults = []
        writeResults = []
        for result in results:
            fResult = self.parseFioResult(result)
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

        # get the order in which the results should be plotted
        order = np.argsort(times)
        # order times, readResults and writeResults
        times = np.array(times)[order]
        readResults = np.array(readResults)[order]
        writeResults = np.array(writeResults)[order]
        print(readResults)
        # now do the plotting
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
        #pyIOplot.getFioResults(args.resultDir + "/fio/")
        pyIOplot.getCompileBenchResults(args.resultDir + "/compilebench/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process pyIO arguments.')
    parser.add_argument("workdir", help='Location where IO is done')
    parser.add_argument("resultDir", help='Location of results')
    parser.add_argument("timeStamp", help='Timestamp, from which one results will be considered for plotting')
    args = parser.parse_args()
    pyIOplot = PyIOPlot()
    pyIOplot.plot(args)
