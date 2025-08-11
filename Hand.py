import subprocess
import os
import pathlib
import random
import math
import numpy as np
from scipy.stats import skew, kurtosis
from functions import *

def print_lines(lines):
    for line in lines:
        print(line)

class Hand(object):
    def __init__(self, parser, spot, tree, num):
        self.parser = parser
        self.spot = spot
        self.tree = tree
        self.num = num
        self.strhand = self.parser.list_hands[num]
        self.data = []

    def make(self):
        self.make_vs_ranges()
        self.make_rivers()
        # if random.randint(0,90) == 87:
        #     print(self.strhand, self.data)
        self.make_data()


    def make_vs_ranges(self):
        for i in range(len(self.tree.sepvln)):
            res = hand_vs_range(self.tree.eqs, self.num, self.tree.sepvln[i], self.parser.inter)
            self.data.append(res)
            block = blocker(self.num,self.tree.sepvln[i],self.parser.inter)
            self.data.append(block)

    def make_rivers(self):
        rivers = self.tree.rivers[:, self.num]
        self.data.append(np.nanmean(rivers))
        self.data.append(np.nanstd(rivers))
        for i in range(5,100,5):
            self.data.append(np.nanpercentile(rivers, i))
        self.data.append(skew(rivers, nan_policy='omit'))
        self.data.append(kurtosis(rivers, nan_policy='omit'))

    def make_data(self):
        action = self.tree.node
        target = self.tree.evs[self.num] / self.tree.pot + self.tree.addev / self.tree.pot
        name = self.spot.filename + " " + action + " " + self.strhand
        inputs = self.tree.data + self.data

        self.parser.names.append(name)
        self.parser.X.append(inputs)
        self.parser.y.append(target)
        self.spot.lines += 1
        if random.randint(0,20000) == 17:
            print("------" + name + "------")
            print("SPR : ", inputs[0:5])
            print("Range VS Range : ", inputs[5:30])
            print("Range Drawyness : ", inputs[30:34])
            print("Hand VS Range : ", inputs[34:58])
            print("River Stats : ", inputs[58:])
            print("Target : ", target)
            print("EV : ", self.tree.evs[self.num])
            print("POT : ", self.tree.pot)
            print("ADD EV : ", self.tree.addev)
            print("EV TOTAL : ", self.tree.addev + self.tree.evs[self.num])




