#!/usr/bin/python
from pyIOtest import PyIOtest
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class fioResult:
    fiomode = ""
    fionumj = ""
    fioSize = ""
    fioBlockSize = ""
    fioExtraArgs = ""
    readResult = ""
    writeResult = ""
    IOPs = ""
    timestamp = ""


class FioPlotModule():
    def __init__(self):
        return

    def parseFioResult(self, inString, pyIOplot):
        results = []
        substr = pyIOplot.substrSearch(inString, "READ: bw=", "iB/s")
        results.append(pyIOplot.removeUnitAndMultiply(substr, True))

        substr = pyIOplot.substrSearch(inString, "WRITE: bw=", "iB/s")
        results.append(pyIOplot.removeUnitAndMultiply(substr, True))
        timestamp = pyIOplot.substrSearch(inString, "TIME:", "\n")
        results.append(timestamp)
        return results

    def plot(self, path, pyIOplot):
        results = pyIOplot.resultIteration(path)
        fioResults = []
        times = []
        readResults = []
        writeResults = []
        for result in results:
            fResult = self.parseFioResult(result, pyIOplot)
            # only plot from start time
            testTime = datetime.strptime(fResult[2], "%d_%m_%Y-%H_%M_%S")
            if(pyIOplot.startTime <= testTime):
                # get timedelta and save it
                timeD = (testTime - pyIOplot.startTime).total_seconds()
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
        ax.set_title("Fio Results on " + pyIOplot.workDir)
        plt.show()
