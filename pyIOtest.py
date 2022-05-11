#!/usr/bin/python
import os
import subprocess
from datetime import datetime
import shutil
import argparse

def initializePath(path):
    os.makedirs(path, exist_ok=True)

def cleanUp(path):
    print("Cleaning " + path)
    shutil.rmtree(path)

# get all the outputs in a string and decode it to a string
def decodeOutput(output):
    return (output.stderr.read() + output.stdout.read()).decode("utf-8")

# runs the IO commands in subprocesses, catches all stderr and stdout output and
# writes it into resultPath, automatically appending run to filename
def runIoCommand(runs, command, resultPath):
    for x in range(0,runs):
            # replace <run> tag in command
            command2 = command.replace("<run>", str(x))
            # print commands as progress notifier
            print(command2)
            # start subprocess and capture
            output = subprocess.Popen(command2, stderr=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
            # write output
            f = open(resultPath + str(x) + ".txt", "w")
            f.write(decodeOutput(output))
            f.close()

def compileBenchTests(IOdirectory, resultDir):
    IOdirectory += "/compilebench/"
    initializePath(IOdirectory)
    compileBenchRuns = 1
    # compilebench in makej mode
    runIoCommand(compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' + IOdirectory + '<run> -i 1 --makej ',  resultDir + "/compilebench_makej_")
    # without makej
    runIoCommand(compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' + IOdirectory + '<run> -i 1 -r 1 ',  resultDir + "/compilebench_")
    cleanUp(IOdirectory)
    initializePath(IOdirectory)

def ioZoneTests(resultDir):
    iozoneRuns = 1
    # iozone with all tests
    runIoCommand(iozoneRuns, 'iozone -a -b ' + resultDir + "/result<run>.xls",  resultDir + "/iozone_a")    

def fioTests(IOdirectory, resultDir):
    IOdirectory += "/fio/"
    initializePath(IOdirectory)
    fioRuns = 1
    # set fio parameters
    fiomode = "randrw"
    fionumj = "4"
    fioSize = "20M"
    fioBlockSize = "1M"
    fioExtraArgs =  " --direct=0 --group_reporting --fallocate=none"
    # run fio
    runIoCommand(fioRuns, 'fio --rw=' + fiomode + " --name " + IOdirectory + "/test<run> --bs=" + fioBlockSize + " --numj=" + fionumj + " --size=" + fioSize + fioExtraArgs,
      resultDir + "/fio_" + fiomode + "_s" + fioSize + "_numj" + fionumj + "_") 
    cleanUp(IOdirectory)

def main(args):
    print(args)
    # avoid likely mistakes
    if args.workdir == "" or args.workdir == "/":
        print("No empty string allowed for workdir")
        return -1
    if args.resultDir == "":
        print("No empty string allowed for resultDir")
        return -1
    # create the test result directory with a timestamp
    resultBaseDir = args.resultDir
    initializePath(resultBaseDir)
    resultDir = resultBaseDir+ str(datetime.now())
    initializePath(resultDir)
    IOdirectory = args.workdir+"/pyIOdata"
    initializePath(IOdirectory)

    compileBenchTests(IOdirectory, resultDir)
    ioZoneTests(resultDir)
    fioTests(IOdirectory, resultDir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some values.')
    parser.add_argument("workdir", help='Location where IO is done')
    parser.add_argument("resultDir", help='Location of results')
    args = parser.parse_args()
    main(args)
