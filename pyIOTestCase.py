#!/usr/bin/python
from pyIOtest import PyIOtest
from datetime import datetime
import timeit
import sched, time
import argparse
import signal

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException


# runs the actual test case
def runTest(pyIO, scheduler, tries, args):
    print("Running")
    signal.alarm(3595)
    try:
        start = timeit.default_timer()
        pyIO.initializeRunDirectory(args)
        pyIO.compileBenchTests()
        pyIO.iozoneRecordSize = 4096
        pyIO.iozoneFileSize = 32768
        pyIO.ioZoneTests()
        pyIO.iozoneRecordSize = 4
        pyIO.iozoneFileSize = 32768
        pyIO.iozoneThreads = 10
        pyIO.ioZoneTests()
        pyIO.fioSize = "200M"
        pyIO.fioTests()
        stop = timeit.default_timer()
        # reduce waitTime by duration of run tasks
        waitTime = 2.0 - (stop-start)
        if waitTime < 0.0:
            waitTime = 0.0
        tries += 1
        if tries < 10:
            scheduler.enter(waitTime, 1, runTest, (pyIO,scheduler, tries, args))
    except TimeoutException:
        print("Timed out current attempt, restarting")
        stop = timeit.default_timer()
        waitTime = 2.0 - (stop-start)
        if waitTime < 0.0:
            waitTime = 0.0
        tries += 1
        if tries < 10:
            scheduler.enter(waitTime, 1, runTest, (pyIO,scheduler, tries, args))    
    else:
        # Reset the alarm
        signal.alarm(0)
        
def default(args):
    signal.signal(signal.SIGALRM, timeout_handler)
    scheduler = sched.scheduler(time.time, time.sleep)
    pyIO = PyIOtest()
    tries = 0
    print(args)
    # avoid likely mistakes
    if args.workdir == "" or args.workdir == "/":
        print("No empty string allowed for workdir")
        return -1
    if args.resultDir == "":
        print("No empty string allowed for resultDir")
        return -1
    # create the test result directory with a timestamp
    scheduler.enter(0, 1, runTest, (pyIO,scheduler, tries, args))
    scheduler.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process pyIO arguments.')
    parser.add_argument("workdir", help='Location where IO is done')
    parser.add_argument("resultDir", help='Location of results')
    args = parser.parse_args()
    default(args)
