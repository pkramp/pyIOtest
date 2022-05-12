#!/usr/bin/python
from pyIOtest import PyIOtest
from datetime import datetime
import argparse
def default(args):
    pyIO = PyIOtest()
    print(args)
    # avoid likely mistakes
    if args.workdir == "" or args.workdir == "/":
        print("No empty string allowed for workdir")
        return -1
    if args.resultDir == "":
        print("No empty string allowed for resultDir")
        return -1
    # create the test result directory with a timestamp
    pyIO.resultBaseDir = args.resultDir
    pyIO.initializePath(pyIO.resultBaseDir)
    pyIO.resultDir = pyIO.resultBaseDir + "/" + str(datetime.now())
    pyIO.initializePath(pyIO.resultDir)
    pyIO.IOdirectory = args.workdir+"/pyIOdata"
    pyIO.initializePath(pyIO.IOdirectory)

    pyIO.compileBenchTests()
    pyIO.iozoneRecordSize = 4096
    pyIO.iozoneFileSize = 32768
    pyIO.ioZoneTests()
    pyIO.iozoneRecordSize = 4
    pyIO.iozoneFileSize = 32768
    pyIO.iozoneThreads = 10
    pyIO.ioZoneTests()
    pyIO.fioTests()
    pyIO.fioSize = "200M"
    pyIO.fioSize = "2G"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some values.')
    parser.add_argument("workdir", help='Location where IO is done')
    parser.add_argument("resultDir", help='Location of results')
    args = parser.parse_args()
    default(args)
