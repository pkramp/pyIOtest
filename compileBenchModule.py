#!/usr/bin/python
from pyIOtest import PyIOtest


class CompileBenchModule():
    compileBenchRuns = 1

    def __init__(self, pyIO):
        self.resultDir = pyIO.resultDir + "/compilebench/"
        self.makeJResultDir = pyIO.resultDir + "/compilebench_makej/"
        self.IOdir = pyIO.IOdirectory + "/compilebench/"
        pyIO.initializePath(self.resultDir)
        pyIO.initializePath(self.makeJResultDir)

    def compileBenchTests(self, pyIO, extraArgs=""):
        #cIOdirectory = self.IOdirectory + "/compilebench/"
        pyIO.initializePath(self.IOdir)
        # compilebench in makej mode
        pyIO.runIoCommand(self.compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' +
                          self.IOdir + '<run> -i 10 --makej ' + extraArgs,  self.makeJResultDir)
        # without makej
        pyIO.runIoCommand(self.compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' +
                          self.IOdir + '<run> -i 10 -r 20 ' + extraArgs,  self.resultDir)
        pyIO.cleanUp(self.IOdir)
