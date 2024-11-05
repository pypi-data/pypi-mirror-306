#!/usr/bin/env python

import os
import yaml
import subprocess
import argparse
import json
from importlib import resources
from itertools import product

parser = argparse.ArgumentParser(
    prog='taguchi',
    description='performs taguchi based experiments',
    epilog='see https://github.com/jcranney/taguchi for more info.',
)

parser.add_argument(
    'config', nargs='?', default="./taguchi.yaml",
    help="specify a yaml file instead of looking for taguchi.yaml"
)
parser.add_argument(
    '-v', '--verbose', action='count', default=0,
    help="verbosity level (e.g., use -vvv for level 3 verbosity)"
)
parser.add_argument(
    '-d', '--dense', action='count', default=0,
    help="force use of 'dense' experiment array, performing all experiments"
)

args = parser.parse_args()
verbose = args.verbose
dense = args.dense
config = args.config


def printout(*args, level: int = 1):
    if verbose >= level:
        print(*args, flush=True)


with open(config, "r") as f:
    a: dict = yaml.full_load(f)

command = a.pop("command")

params = []
static_params = []
for param in list(a.keys()):
    if len(a[param]) == 0:
        printout(f"empty param: {param}, skipping it.")
        continue
    if len(a[param]) == 1:
        os.environ[param] = str(a[param][0])
        printout(
            f"param {param} has only one value, setting to {str(a[param][0])}"
        )
        static_params.append(param)
        continue
    params.append(param)

n_params = len(params)
if n_params > 0:
    n_states = len(a[params[0]])
else:
    # to get here, we must have static parameters only (if anything)
    # I realise that n_states makes more sense as "1" but let's have
    # n_states = 0 => all static params
    n_states = 0

for param in params:
    if len(a[param]) != n_states:
        raise ValueError(
            "All parameters must have the same number of states (for now)"
        )

filename = str(resources.files("taguchi")/"database.json")

with open(filename, "r") as f:
    orthogonal_arrays = json.load(f)

if dense:
    array = list(product(range(n_states), repeat=n_params))
else:
    try:
        array = orthogonal_arrays[f"{n_params:d},{n_states:d}"]
    except KeyError:
        raise NotImplementedError(
            f"{n_params:d} params with {n_states:d} states"
            " not supported, try --dense"
        )

printout(f"Doing {len(array)} experiments in total!\n")
printout("Experiments:\n", array, level=2)

results: list = []
for experiment in array:
    for param, state in zip(params, experiment):
        os.environ[param] = str(a[param][state])
        printout(param, a[param][state])
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if err is not None:
        printout(err.decode(), level=0)
        exit(1)
    printout(out.decode(), level=2)

    out = out.decode().split("\n")
    result = None
    for o in out:
        try:
            result = float(o)
        except ValueError:
            pass
    printout(f"{result=}\n")
    if result is None:
        raise ValueError("No number found in output of command")

    results.append(result)

if len(params) > 0:
    printout("\n`````` VARIABLE PARAMS ``````", level=0)
for j, param in enumerate(params):
    printout(f"{param:12s}", level=0)
    for i, state in enumerate(a[param]):
        res = 0.0
        n_experiment = 0
        for k, experiment in enumerate(array):
            if experiment[j] == i:
                res += results[k]
                n_experiment += 1
        printout(f"{state:12} : {res/n_experiment:12f}", level=0)

if len(static_params) > 0:
    printout("\n``````  STATIC PARAMS  ``````")
for j, param in enumerate(static_params):
    printout(f"{param:12s}")
    for i, state in enumerate(a[param]):
        printout(f"{state:12} : {sum(results)/len(results):12f}")
