#!/usr/bin/python
import os
import subprocess
import shutil
from datetime import datetime
class PyIOtest:
    # members
    IOdirectory = "/tmp/pyIOworkdir"
    resultDir = "/tmp/pyIOresults"
    fioRuns = 1
    # fio args
    fiomode = "randrw"
    fionumj = "4"
    fioSize = "20M"
    fioBlockSize = "1M"
    fioExtraArgs =  " --direct=0 --group_reporting --fallocate=none"
    # compilebench args
    compileBenchRuns = 1
    # iozone args
    iozoneRuns = 1
    iozoneRecordSize = 4096
    iozoneFileSize = 32768
    iozoneThreads = 0
    
    def initializeRunDirectory(self, args):
        self.resultBaseDir = args.resultDir
        self.initializePath(self.resultBaseDir)
        self.startTime = datetime.now()
        self.stringTime = str(self.startTime.strftime("%d_%m_%Y-%H_%M_%S"))
        self.resultDir = self.resultBaseDir + "/"
        self.initializePath(self.resultDir)
        self.initializePath(self.resultDir + "/fio/")
        self.initializePath(self.resultDir + "/iozone/xls/")
        self.initializePath(self.resultDir + "/iozone/txt/")
        self.initializePath(self.resultDir + "/compilebench/" )
        self.initializePath(self.resultDir + "/compilebench_makej/")
        self.IOdirectory = args.workdir + "/pyIOdata/" + self.stringTime
        self.initializePath(self.IOdirectory)
    
    def initializePath(self, path):
        os.makedirs(path, exist_ok=True)

    def cleanUp(self, path):
        print("Cleaning " + path)
        shutil.rmtree(path)

    # get all the outputs in a string and decode it to a string
    def decodeOutput(self, output):
        return (output.stderr.read() + output.stdout.read()).decode("utf-8")

    # runs the IO commands in subprocesses, catches all stderr and stdout output and
    # writes it into resultPath, automatically appending run to filename
    def runIoCommand(self, runs, command, resultPath):
        for x in range(0,runs):
                # replace <run> tag in command
                command2 = command.replace("<run>", str(x))
                # print commands as progress notifier
                print(command2)
                # start subprocess and capture
                output = subprocess.Popen(command2, stderr=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
                # write output
                path = resultPath + self.stringTime + "___" + str(x) + ".txt"
                f = open(path, "w")
                print("Writing output to " + path)
                f.write("TIME:" + str(datetime.now().strftime("%d_%m_%Y-%H_%M_%S")) + "\n")
                f.write(self.decodeOutput(output))
                f.close()

    def compileBenchTests(self, extraArgs=""):
        cIOdirectory = self.IOdirectory + "/compilebench/"
        self.initializePath(cIOdirectory)
        # compilebench in makej mode
        self.runIoCommand(self.compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' + cIOdirectory + '<run> -i 1 --makej ' + extraArgs,  self.resultDir + "/compilebench_makej/")
        # without makej
        self.runIoCommand(self.compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' + cIOdirectory + '<run> -i 1 -r 1 ' + extraArgs,  self.resultDir + "/compilebench/")
        self.cleanUp(cIOdirectory)
        self.initializePath(cIOdirectory)

    def ioZoneTests(self, extraArgs=""):
        IOzoneDirectory = self.IOdirectory + "/ioZone/"
        self.initializePath(IOzoneDirectory)
        # iozone with all tests
        self.runIoCommand(self.iozoneRuns, 'cd ' + IOzoneDirectory + '&& iozone -r' + str(self.iozoneRecordSize) + ' -s ' + str(self.iozoneFileSize) + ' ' + extraArgs + " -b " + self.resultDir + "/iozone/xls/" + self.stringTime + "___<run>.xls",  self.resultDir + "/iozone/txt/")
        self.cleanUp(IOzoneDirectory)

    def fioTests(self, extraArgs=""):
        fIOdirectory = self.IOdirectory + "/fio/"
        self.initializePath(fIOdirectory)
        # run fio
        self.runIoCommand(self.fioRuns, 'fio --rw=' + self.fiomode + " --name "
        + fIOdirectory + "/test<run> --bs=" + self.fioBlockSize + " --numj="
        + self.fionumj + " --size=" + self.fioSize + self.fioExtraArgs,
          self.resultDir + "/fio/" + self.fiomode + "_s" + self.fioSize 
          + "_numj" + self.fionumj + "_")
        self.cleanUp(fIOdirectory)
