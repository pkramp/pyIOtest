import os
import subprocess
from datetime import datetime
import shutil

test_results = []
# parsing method for compileBench raw text
def parseCompileBench(outString):
    pos1 = outString.find("avg")
    pos2 = outString.find("B/s", pos1)#
    pos3 = outString.find("avg", pos2)
    pos4 = outString.find("B/s", pos3)#
    print(outString[pos1+4:pos2-2])
    print(outString[pos3+4:pos4-2])
    test_results.append(outString[pos1+4:pos2-2])
    test_results.append(outString[pos3+4:pos4-2])

def initializePath(path):
    if not os.path.exists(path):
        os.mkdir(path)

def cleanUp(path):
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

def compileBenchTests():
    compileBenchRuns = 1
    # compilebench in makej mode
    runIoCommand(compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' + IOdirectory + 'compilebench_working_dir_<run> -i 1 --makej ',  resultDir + "/compilebench_makej_")
    # without makej
    runIoCommand(compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' + IOdirectory + 'compilebench_working_dir_<run> -i 1 -r 1 ',  resultDir + "/compilebench_")
    cleanUp(IOdirectory)
    initializePath(IOdirectory)

def ioZoneTests():
    iozoneRuns = 1
    # iozone with all tests
    runIoCommand(iozoneRuns, 'iozone -a -b ' + resultDir + "/result<run>.xls",  resultDir + "/iozone_a")    

def fioTests():
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

#"main"
# create the test result directory with a timestamp
testBaseDir = "/tmp/pyIOResults/"
initializePath(testBaseDir)
resultDir = testBaseDir+ str(datetime.now())
initializePath(resultDir)
IOdirectory = "/tmp/pyIOworkDir/"
initializePath(IOdirectory)

compileBenchTests()
#ioZoneTests()
fioTests()
