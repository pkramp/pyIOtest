#!/usr/bin/python
from pyIOtest import PyIOtest


class FioModule():
    def __init__(self, pyIO):
        self.resultDir = pyIO.resultDir + "/fio/"
        self.IOdir = pyIO.IOdirectory + "/fio/"
        pyIO.initializePath(self.resultDir)

    fioRuns = 1
    # fio args
    fiomode = "randrw"
    fionumj = "4"
    fioSize = "20M"
    fioBlockSize = "1M"
    fioExtraArgs = " --direct=0 --group_reporting --fallocate=none"

    def fioTests(self, pyIO, extraArgs=""):
        pyIO.initializePath(self.IOdir)
        # run fio
        pyIO.runIoCommand(self.fioRuns, 'fio --rw=' + self.fiomode + " --name "
                          + self.IOdir + "/test<run> --bs=" + self.fioBlockSize + " --numj="
                          + self.fionumj + " --size=" + self.fioSize + self.fioExtraArgs,
                          self.resultDir + self.fiomode + "_s" + self.fioSize
                          + "_numj" + self.fionumj + "_")
        pyIO.cleanUp(self.IOdir)
