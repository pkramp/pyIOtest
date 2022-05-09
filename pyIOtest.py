import os
import subprocess
from datetime import datetime

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
            # get all the outputs in a string
            outString = b""
            outString += output.stderr.read()        
            outString += output.stdout.read()
            outString = outString.decode("utf-8") 
            # write output
            f = open(resultPath + str(x) + ".txt", "w")
            f.write(outString)
            f.close()

#"main"
# create the test result directory with a timestamp
testBaseDir = "/tmp/pyIOResults"
if not os.path.exists(testBaseDir):
    os.mkdir(testBaseDir)
resultDir = testBaseDir+ str(datetime.now())
os.mkdir(resultDir)
compileBenchRuns = 1
iozoneRuns = 1
IOdirectory = "/tmp/pyIOworkDir"
if not os.path.exists(IOdirectory):
    os.mkdir(IOdirectory)
# compilebench in makej mode
runIoCommand(compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' + IOdirectory + 'compilebench_working_dir_<run> -i 1 --makej ',  resultDir + "/compilebench_makej_")
# without makej
runIoCommand(compileBenchRuns, 'cd compilebench-0.6 && ./compilebench -D' + IOdirectory + 'compilebench_working_dir_<run> -i 1 -r 1 ',  resultDir + "/compilebench_")
# iozone with all tests
runIoCommand(iozoneRuns, 'iozone -a -b ' + resultDir + ,  resultDir + "/iozone_a")
# set fio parameters
fiomode = "randrw"
fionumj = "4"
fioSize = "20M"
fioBlockSize = "1M"
fioExtraArgs =  " --direct=0 --group_reporting --fallocate=none"
# run fio
runIoCommand(2, 'fio --rw=' + fiomode + " --name test<run> --bs=" + fioBlockSize + " --numj=" + fionumj + " --size=" + fioSize + fioExtraArgs,
  resultDir + "/fio_" + fiomode + "_s" + fioSize + "_numj" + fionumj + "_")
 
#subprocess.Popen("rm -rf test*", stderr=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
