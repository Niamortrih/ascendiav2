from Solver import Solver
from funcsolver import *
import joblib
import numpy as np

MODEL_FILE = "model.pkl"
SCALER_FILE = "scaler.pkl"

# charge comme dans ton script
model = joblib.load(MODEL_FILE)
scaler = joblib.load(SCALER_FILE)

def load_config(path):
    config = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#') and line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


config = load_config("config.txt")
connection = Solver(solver=config["solver"])
r = connection.command(line="set_isomorphism 0 0")

r = connection.command(line="show_hand_order")
list_hands = r[0].split()

filename = "D:/Jesolver/QJ7_6.cfr"
board = "QsJh7d"
alpha = 0.1

r = connection.command(line="load_tree " + filename)
print(r[0])
# r = connection.command(line="set_board " + board)

stroop = get_range(connection, "OOP", "r:0")
taboop = str_to_tab(stroop)
strip = get_range(connection, "IP", "r:0")
tabip = str_to_tab(strip)


eqs = get_eqs(connection,taboop)
print("EQUITIES LOADED, SOLVING START")


node = "r:0"
children = get_children(connection,node)
print(children)

nbplays = len(children)
startfreq = 1 / nbplays

tabstrat = np.full((1326, 3), startfreq, dtype=float)

def boost_index(x, n, step=0.1):
    mask = np.ones(x.shape, dtype=bool); mask[n] = False
    take = np.minimum(step, x[mask])     # ne descend jamais sous 0
    x[mask] -= take
    x[n] += take.sum()

for i in range(100):
    evs = []
    for j in range(nbplays):
        roop = tabstrat[:, j].copy()
        roop *= taboop
        print(children[j])
        res = make_result(connection, children[j], roop, tabip, eqs, list_hands, scaler, model)
        evs.append(res)
    evs = np.array(evs)
    for j in range(1326):
        if taboop[j] > 0.01:
            res = evs[:, j]
            res[0] -= 4.5
            res[1] -= 0.5
            imax = np.argmax(res)
            # print("OLD", list_hands[j], tabstrat[j])
            boost_index(tabstrat[j],imax,0.1)
            print("-------")
            print(list_hands[j], tabstrat[j])
            print(res)


