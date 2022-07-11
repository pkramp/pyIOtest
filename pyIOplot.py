import os
from datetime import datetime, timedelta
import shutil
import argparse
from fioPlotModule import FioPlotModule
from compileBenchPlotModule import CompileBenchPlotModule
from ioZonePlotModule import IoZonePlotModule


class PyIOPlot:
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

    def plot(self, args):
        pyIOplot.startTime = datetime.strptime(
            args.timeStamp, "%d_%m_%Y-%H_%M_%S")
        pyIOplot.workDir = args.workdir
        fioPlotter = FioPlotModule()
        fioPlotter.plot(args.resultDir + "/fio/", self)
        compileBenchPlotter = CompileBenchPlotModule()
        compileBenchPlotter.plot(
            args.resultDir + "/compilebench/", self)
        ioZonePlotter = IoZonePlotModule()
        ioZonePlotter.plot(args.resultDir + "/iozone/", self)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process pyIO arguments.')
    parser.add_argument("workdir", help='Location where IO is done')
    parser.add_argument("resultDir", help='Location of results')
    parser.add_argument(
        "timeStamp", help='Timestamp, from which one results will be considered for plotting')
    args = parser.parse_args()
    pyIOplot = PyIOPlot()
    pyIOplot.plot(args)
