#!/usr/bin/python
from pyIOtest import PyIOtest
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class CompileBenchPlotModule():
    def __init__(self):
        return

    # parsing method for compileBench raw text
    def parseCompileBench(self, inString, pyIOplot):
        searchStrings = ["intial create total runs", ")\ncreate total runs",
                         "patch total runs", "compile total runs ", "clean total runs",
                         "read tree total runs", "read compiled tree total runs "]
        results = []
        for searchString in searchStrings:
            subs = pyIOplot.substrSearch(inString, searchString, "MB/s")
            subs = pyIOplot.substrSearch(subs, "avg ", "\n")
            results.append(subs)
        # also get timestamp
        timestamp = pyIOplot.substrSearch(inString, "TIME:", "\n")
        results.append(timestamp)
        return results

    def plot(self, path, pyIOplot):
        initCreate = []
        create = []
        patch = []
        compile = []
        clean = []
        readTree = []
        readCompiled = []
        times = []
        # gather all result texts from given path
        results = pyIOplot.resultIteration(path)
        for result in results:
            cbResult = self.parseCompileBench(result)
            testTime = datetime.strptime(cbResult[7], "%d_%m_%Y-%H_%M_%S")
            if(pyIOplot.startTime <= testTime):
                print(cbResult)
                initCreate.append(float(cbResult[0]))
                create.append(float(cbResult[1]))
                patch.append(float(cbResult[2]))
                compile.append(float(cbResult[3]))
                clean.append(float(cbResult[4]))
                readTree.append(float(cbResult[5]))
                readCompiled.append(float(cbResult[6]))
                timeD = (testTime - pyIOplot.startTime).total_seconds()
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
        initCreateHandle, = ax.plot(
            times, initCreate, label='Initial create performance')
        createHandle, = ax.plot(times, create, label='Create performance')
        patchHandle, = ax.plot(times, patch, label='Patch performance')
        compileHandle, = ax.plot(times, compile, label='Compile performance')
        #cleanHandle, = ax.plot(times, clean, label='Clean performance')
        readTreeHandle, = ax.plot(
            times, readTree, label='readTree performance')
        #readCompiledHandle, = ax.plot(times, readCompiled, label='readCompiled performance')

        ax.set_xlabel("Time since start in seconds")
        ax.set_ylabel("Throughput in MB/s")
        ax.legend(handles=[initCreateHandle, createHandle,
                  patchHandle, compileHandle, readTreeHandle])
        ax.set_title("Compilebench results on " + pyIOplot.workDir)
        plt.show()
