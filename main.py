from Solver import Solver
from Parser import Parser

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

parser = Parser(connection, config)

parser.make()
parser.save()