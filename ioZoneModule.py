#!/usr/bin/python
from pyIOtest import PyIOtest


class IoZoneModule():
    # iozone args
    iozoneRuns = 1
    iozoneRecordSize = 4096
    iozoneFileSize = 32768
    iozoneThreads = 0

    def __init__(self, pyIO):
        self.xlsDir = pyIO.resultDir + "/iozone/xls/"
        self.txtDir = pyIO.resultDir + "/iozone/txt/"
        self.IOdir = pyIO.IOdirectory + "/iozone/"
        pyIO.initializePath(self.xlsDir)
        pyIO.initializePath(self.txtDir)

    def ioZoneTests(self, pyIO, extraArgs=""):
        pyIO.initializePath(self.IOdir)
        # iozone with all tests
        pyIO.runIoCommand(self.iozoneRuns, 'cd ' + self.IOdir + '&& iozone -r ' + str(self.iozoneRecordSize) + ' -s ' + str(self.iozoneFileSize) + ' ' + extraArgs + " -b " + self.xlsDir +
                          pyIO.stringTime + "_r" + str(self.iozoneRecordSize) + "_s" + str(self.iozoneFileSize) + "_<run>.xls",  self.txtDir, "r" + str(self.iozoneRecordSize) + "_s" + str(self.iozoneFileSize))
        pyIO.cleanUp(self.IOdir)
