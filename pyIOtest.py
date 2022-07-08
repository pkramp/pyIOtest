#!/usr/bin/python
import os
import subprocess
import shutil
from datetime import datetime


class PyIOtest:
    # default values
    IOdirectory = "/tmp/pyIOworkdir"
    resultDir = "/tmp/pyIOresults"

    def initializeRunDirectory(self, args):
        self.resultBaseDir = args.resultDir
        self.initializePath(self.resultBaseDir)
        self.startTime = datetime.now()
        self.stringTime = str(self.startTime.strftime("%d_%m_%Y-%H_%M_%S"))
        self.resultDir = self.resultBaseDir + "/"
        self.initializePath(self.resultDir)
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
    def runIoCommand(self, runs, command, resultPath, pathArgs=""):
        for x in range(0, runs):
            # replace <run> tag in command
            command2 = command.replace("<run>", str(x))
            # print commands as progress notifier
            print(command2)
            # start subprocess and capture
            output = subprocess.Popen(
                command2, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            # write output
            path = resultPath + self.stringTime + \
                "_" + pathArgs + "__" + str(x) + ".txt"
            f = open(path, "w")
            print("Writing output to " + path)
            f.write(
                "TIME:" + str(datetime.now().strftime("%d_%m_%Y-%H_%M_%S")) + "\n")
            f.write(self.decodeOutput(output))
            f.close()
