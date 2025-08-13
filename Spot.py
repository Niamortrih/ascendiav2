import subprocess
import os
import pathlib
import math
from functions import *
import time
from Tree import Tree

class Spot(object):
    def __init__(self, filename, parser):
        self.filename = filename
        self.parser = parser
        self.connection = parser.connection
        self.lines = 0


    def make(self):
        r = self.connection.command(line='load_tree "' + self.filename + '"')
        board = os.path.basename(self.filename).split(self.parser.config["separator"])[0]
        board = board.split(".")[0]
        # print(board)
        r = self.connection.command(line="set_board " + board)
        self.stroop = get_range(self.connection, "OOP", "r:0")
        self.taboop = str_to_tab(self.stroop)
        self.eqs = get_eqs(self.connection,self.taboop, board)

        r = self.connection.command(line="show_effective_stack")
        self.startstack = float(r[0])
        r = self.connection.command(line="show_tree_params")
        self.startpot = float(r[1].split()[-1])

        self.make_recur("r:0",1,0)


    def make_recur(self,node, pos, n):
        tree = Tree(self.parser, self, node, pos, n)
        tree.make()
        children = get_children(self.connection,node)
        if len(children) < 30:
            for child in children:
                if child[-1] != "f":
                    self.make_recur(child,1-pos, n+1)






