#!/usr/bin/python
from pyIOtest import PyIOtest
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class IoZonePlotModule():
    def __init__(self):
        return

    def plot(self, path, pyIOplot):
        results = pyIOplot.resultIteration(path)
