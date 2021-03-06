import argparse
import game_loop
from colors import Colors
from tqdm import tqdm
import time
import random

parser = argparse.ArgumentParser(description='A game based on the Game of Life')
parser.add_argument('--night-mode', dest='night_mode', action='store_true', help="Changes the colors to accomodate the eyes")
parser.add_argument('--no-ui', dest='ui', action='store_false', help="Makes the game run without a ui. Use it with --synchronous to speed up the game by a lot")
parser.add_argument('--synchronous', dest='synchronous', action='store_true', help="Does not wait the set amount of time to run next step, only wait for the players")
parser.add_argument('--nb-moves', dest='nb_moves', help="The max number of move for each player", default=250)
parser.add_argument('--density', dest='density', help="The proportion of alive cells at the start of the game, between 0 and 1", default=0.2)
parser.add_argument('--nb-games', dest='nb_games', help="Runs several games and returns stats for both players", default=1)
parser.add_argument('--p1', dest="p1", help="The location of your player 1", default="AIs/player.py")
parser.add_argument('--p2', dest="p2", help="The location of your player 2", default="AIs/player.py")
parser.add_argument('--width', dest='width', help="The number of cells horizontally", default=15)
parser.add_argument('--height', dest='height', help="The number of cells vertically", default=15)
parser.add_argument('--test', dest='test', action='store_true', help="Runs the game in a test state, allowing to start with a given configuration specified in the AI file")
parser.add_argument('--seed', dest='seed', help="Starts the game with a given seed", default=None)
parser.add_argument('--fps', dest='fps', help="Sets the speed of the game", default=4)

args = parser.parse_args()

col = Colors()
if args.night_mode:
    col.night_mode()

if args.test:
    args.p2 = "AIs/dummy.py"

if (args.seed == None):
    args.seed = int(1000000000 * time.time())
else:
    args.seed = int(args.seed)
rng = random.Random(args.seed)

res = []
seed_list = []

nb_wins = {'p1': 0, 'p2': 0, 'tie': 0}

for game in tqdm(range(int(args.nb_games))):
    res.append(game_loop.game(args.p1.replace('/', '.')[:-3], args.p2.replace('/', '.')[:-3], int(args.width),\
     int(args.height), col, args.ui, args.synchronous, int(args.nb_moves), float(args.density), args.test, int(args.fps), rng))
    seed_list.append(args.seed)
    args.seed = int(1000000000 * time.time())
    rng = random.Random(args.seed)


for game in res:
    if game['p1'] > game['p2']:
        nb_wins['p1'] += 1
    if game['p2'] > game['p1']:
        nb_wins['p2'] += 1
    if game['p1'] == game['p2']:
        nb_wins['tie'] += 1

print(nb_wins)

print(seed_list)
