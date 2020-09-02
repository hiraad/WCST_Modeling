import json
from models import outperform, bishara
from util import Experiment
import numpy as np
from scipy.optimize import fmin, minimize, Bounds
import optuna

with open('data/input/conditions.txt', "r") as file:
    conditions_json = json.load(file)
criterion_order = conditions_json[0]["Criterion_Order"]
pile_order = conditions_json[1]["Target_Order"]
deck_order = conditions_json[2]["Card_Order"]

run = 0

start_n = [12,11,12,9]
start_mtries = [20.75,12.91,5.58,27.33]
start_sdtries = [22.59, 9.87, 8.83, 30.49]
sw_n = [16,10,14,19,13,14,14,8]
sw_mtries = [11.13,16,15.29,11.47,11.69,38.71,6.86,23.25]
sw_sdtries = [8.39, 13.13, 22.06, 13.38, 11.41, 28.18, 6.55, 26.44]

def objective(trial):
    global run
    run += 1
    r = trial.suggest_uniform('r', 0, 1)
    p = trial.suggest_uniform('p', 0, 1)
    f = trial.suggest_uniform('f', 0, 5)
    par = [r,p,f]
    print('*******')
    print(run)
    print('Parameters: ' + str(par))
    for i in range(len(deck_order)):
        # print("SUBJECT: " + str(i + 1))
        # outperform.simulate(deck_order[i], criterion_order[i], pile_order[i])
        bishara.simulate(deck_order[i], criterion_order[i], pile_order[i], par)

    stNum, swNum, stMean, stDev, swMean, swDev = Statistics.results()

    # obj = np.absolute(stNum[3]-9)
    # obj = np.linalg.norm(sum(swMean)-sum(sw_mtries))
    obj = np.linalg.norm(swMean-sw_mtries)
    print(f'Start No. of Tries: {swMean}')
    # print(stNum,swNum,stMean,stDev,swMean,swDev)
    print('Objective: ' + str(obj))
    print('*******')
    return obj
    # print(len(deck_order))

study = optuna.create_study(study_name='bishara_opt')
study.optimize(objective, n_trials=500)
print(study)
print(f'Best trial until now: {study.best_trial.number}')
print(' Value: ', study.best_trial)