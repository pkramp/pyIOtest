#!/usr/bin/python
from pyIOtest import PyIOtest
from datetime import datetime, timedelta
import timeit
import sched, time
import argparse
import signal

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

# runs the actual test case
def testCase1(pyIO, scheduler, tries, args):
        # create the work directory test and result directory with a timestamp
        pyIO.initializeRunDirectory(args)
        pyIO.compileBenchTests()
        pyIO.iozoneRecordSize = 4096
        pyIO.iozoneFileSize = 32768
        pyIO.ioZoneTests()
        pyIO.iozoneRecordSize = 4
        pyIO.iozoneFileSize = 32768
        pyIO.iozoneThreads = 10
        pyIO.ioZoneTests()
        pyIO.fioSize = "20M"
        pyIO.fioTests()


def timedExecution(testToRun, pyIO, scheduler, tries, args):
    print("Running")
    signal.alarm(int(args.waitTime))
    try:
        start = timeit.default_timer()
        testToRun(pyIO, scheduler, tries, args)
        stop = timeit.default_timer()
        # reduce waitTime by duration of run tasks
    except TimeoutException:
        print("Timed out current attempt, restarting")
        stop = timeit.default_timer()
    else:
        # Reset the alarm
        signal.alarm(0)
    
    waitTime = float(args.waitTime) - (stop-start)
    if waitTime < 0.0:
        waitTime = 0.0
    tries += 1
    if tries < int(args.tests):
        scheduler.enter(waitTime, 1, timedExecution, (testToRun, pyIO,scheduler, tries, args))

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
    if args.waitTime == "":
        print("No empty string allowed for waitTime")
        return -1
    if args.tests == "":
        print("No empty string allowed for number of tests")
        return -1
    scheduler.enter(0, 1, timedExecution, (testCase1, pyIO,scheduler, tries, args))
    scheduler.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process pyIO arguments.')
    parser.add_argument("workdir", help='Location where IO is done')
    parser.add_argument("resultDir", help='Location of results')
    parser.add_argument("waitTime", help='Time during test starts')
    parser.add_argument("tests", help='Amount of tests')
    args = parser.parse_args()
    default(args)
