import subprocess
import os
import pathlib
import traceback
from Spot import Spot
import random
import numpy as np
from functions import *

def print_lines(lines):
    for line in lines:
        print(line)

class Parser(object):
    def __init__(self, connection, config):
        self.config = config
        r = connection.command(line="set_isomorphism 1 0")
        self.connection = connection
        self.folder = config["folder"]
        print("dataset_" + self.folder.replace("/", "_").replace("\\", "_") + ".npz" + " WILL BE CREATED")
        r = connection.command(line="show_hand_order")
        self.list_hands = r[0].split()
        self.inter = get_intersection_matrix(self.list_hands)
        self.X = []
        self.y = []
        self.names = []
        self.aff = True
        self.bb = 20

    def make(self):
        print("START PARSING", self.folder)
        counter = 1
        file_paths = []

        # Collecte tous les chemins de fichiers récursivement
        for dirpath, _, filenames in os.walk(self.folder):
            for filename in filenames:
                file_paths.append(os.path.join(dirpath, filename))

        random.shuffle(file_paths)
        nbfile = len(file_paths)

        for file_path in file_paths:
            try:
                print("----- SPOT", counter, "/", nbfile, ":", file_path, "-----")
                spot = Spot(file_path, self)
                spot.make()
                print("LINES DONE :", spot.lines)
                counter += 1
                if counter % 100 == 0:
                    self.save_temp()
            except Exception as e:
                print("Erreur :", e)
                traceback.print_exc()


    def save(self):
        X = np.array(self.X)
        y = np.array(self.y)
        names = np.array(self.names)
        name = "dataset_" + self.folder.replace("/", "_").replace("\\", "_") + ".npz"
        np.savez_compressed(name, X=X, y=y, names=names)

    def save_temp(self):
        X = np.array(self.X)
        y = np.array(self.y)
        names = np.array(self.names)
        name = "dataset_save_" + self.folder.replace("/", "_").replace("\\", "_") + ".npz"
        np.savez_compressed(name, X=X, y=y, names=names)