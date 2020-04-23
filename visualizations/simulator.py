from collections import Counter
import matplotlib
import imageio
from random import randrange, choices, choice
from uuid import uuid4 as uuid
from pathlib import Path
from matplotlib import pyplot as plt
from statistics import median
from scipy.stats import norm
import numpy as np

options = list(range(0, 101))
N_VOTERS = 100000
voter_mean = choice(options)
distribution = norm(loc=voter_mean, scale=45)
voters = np.array(choices(options, weights=[1000 * distribution.pdf(o) for o in options], k=N_VOTERS))
median_voter = median(voters)

start_strategy = (randrange(0, 101), randrange(0, 101))

def num_votes(strategy, idx):
    my_strategy = strategy[idx]
    other_strategy = strategy[1 - idx]
    distance_from_them = abs(voters - other_strategy)
    distance_from_me = abs(voters - my_strategy)
    return np.sum(distance_from_me < distance_from_them)

def next_strategy(strategy, who):
    if who == 1:
        return next_strategy(strategy[::-1], 0)[::-1]
    other_strategy = strategy[1]
    my_new_strategy = max(options, key=lambda x: num_votes((x, other_strategy), 0))
    return (my_new_strategy, other_strategy)

all_strategies = [start_strategy]
who = 0
while True:
    current_strategy = all_strategies[-1]
    new_strategy = next_strategy(current_strategy, who)
    if new_strategy != current_strategy:
        all_strategies.append(new_strategy)
        who = 1 - who
    else:
        break

uuid_string = str(uuid())
directory = Path("figures", uuid_string)
print(uuid_string)
directory.mkdir(parents=True)
filenames = []

for (idx, (a, b)) in enumerate(all_strategies):
    matplotlib.rc('axes', edgecolor='w')
    matplotlib.rc('xtick', color='w')
    matplotlib.rc('ytick', color='w')
    fig, axes = plt.subplots()
    axes.set_xlim(-2, 102)
    axes.hist(voters, 101)
    axes.plot([median_voter, median_voter], [100, -100], linewidth=1, color="k")
    axes.plot([a], [[0]], "ro")
    axes.plot([b], [[0]], "bo")
    filename = str(directory / f"{idx}.png")
    filenames.append(filename)
    fig.savefig(filename)

images = []
for filename in filenames:
    images.append(imageio.imread(str(filename)))

movie_directory = Path("movies")
movie_directory.mkdir(exist_ok=True)
imageio.mimsave(movie_directory / f"{uuid_string}.gif", images, duration=0.3)
