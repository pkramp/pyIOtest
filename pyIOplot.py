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
