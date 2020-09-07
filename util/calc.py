from util import create_path, Experiment
from scipy.optimize import fmin, minimize, Bounds
import pandas as pd
from models import bishara
import numpy as np
import optuna
import os


class Statistics:

    start_trials = np.zeros(4)
    switch_trials = np.zeros((4, 4))
    start_tries = {"0": [], "1": [], "2": [], "3": []}
    switch_tries = {"0_1": [], "0_3": [], "1_0": [], "1_2": [], "2_1": [], "2_3": [], "3_0": [], "3_2": []}

    stages = {}

    @staticmethod
    def record(df):
        start_criterion = df.demanded_criterion[0]
        Statistics.start_trials[start_criterion] += 1

        criterion_changes = df[df['demanded_criterion'].diff() != 0].demanded_criterion.to_numpy()
        criterion_indexes = df[df['demanded_criterion'].diff() != 0].index.to_numpy()
        streak_indexes = df[df['total_streaks'].notnull()].index.to_numpy()

        for i in range(0, len(criterion_changes)):
            prior_criterion = criterion_changes[i]
            if i < len(criterion_changes)-1:
                post_criterion = criterion_changes[i+1]
                Statistics.switch_trials[prior_criterion][post_criterion] += 1
                tries = (streak_indexes[i] - 9) - criterion_indexes[i]
                if i == 0:
                    key = str(prior_criterion)
                    Statistics.start_tries[key].append(tries)
                else:
                    key = f"{prior_criterion}_{post_criterion}"
                    Statistics.switch_tries[key].append(tries)

    @staticmethod
    def calculate_results():
        start_means = [np.mean(tries) for key, tries in Statistics.start_tries.items()]
        start_std = [np.std(tries, ddof=1) for key, tries in Statistics.start_tries.items()]
        switch_means = [np.mean(tries) for key, tries in Statistics.switch_tries.items()]
        switch_std = [np.std(tries, ddof=1) for key, tries in Statistics.switch_tries.items()]
        return Statistics.start_trials, Statistics.switch_trials, start_means, start_std, switch_means, switch_std

    @staticmethod
    def RMSE(p, t):
        prediction = np.array(p)
        target = np.array(t)
        return np.sqrt(np.mean((prediction - target) ** 2))


# Base Results:
base_start_n = [12, 11, 12, 9]
base_start_mean_tries = [20.75, 12.91, 5.58, 27.33]
base_start_std_tries = [22.59, 9.87, 8.83, 30.49]
base_switch_n = [16, 10, 14, 19, 13, 14, 14, 8]
base_switch_mean_tries = [11.13, 16, 15.29, 11.47, 11.69, 38.71, 6.86, 23.25]
base_switch_std_tries = [8.39, 13.13, 22.06, 13.38, 11.41, 28.18, 6.55, 26.44]


class Optimize:

    @staticmethod
    def simplex(par):
        par0 = [.5, .5, .5]
        b = (0, .99)
        b2 = (0, 99)
        bounds = (b, b, b2)

    @staticmethod
    def objective(trial):
        r = trial.suggest_uniform('r', 0.1, 1)
        p = trial.suggest_uniform('p', 0.1, 1)
        f = trial.suggest_uniform('f', 0.1, 5)
        parameters = [r, p, f]
        for subject, exp in Statistics.stages.items():
            df = bishara.simulate(exp, parameters)
            Statistics.record(df)
        start_n, switch_n, start_mean, start_dev, switch_mean, switch_dev = Statistics.calculate_results()
        obj = Statistics.RMSE(switch_mean, base_switch_mean_tries)
        return obj

    @staticmethod
    def optuna(n_trials, stages):
        Statistics.stages = stages
        study = optuna.create_study(study_name='bishara_opt')
        study.optimize(Optimize.objective, n_trials=n_trials)
        print(study)
        print(f'Best trial until now: {study.best_trial.number}')
        print(' Value: ', study.best_trial)












    # run = 0
    # def run_bishara(par):
    #     global run
    #     run += 1
    #     print('*******')
    #     print(run)
    #     print('Parameters: ' + str(par))
    #
    #     for i in range(len(deck_order)):
    #         # print("SUBJECT: " + str(i + 1))
    #         # outperform.simulate(deck_order[i], criterion_order[i], pile_order[i])
    #         bishara.simulate(deck_order[i], criterion_order[i], pile_order[i], par)
    #
    #     stNum, swNum, stMean, stDev, swMean, swDev = Statistics.results()
    #     # obj = np.absolute(stNum[3]-9)
    #     obj = np.linalg.norm(sum(swMean)-sum(sw_mtries))
    #     print(f'Start No. of Tries: {swMean}')
    #     # print(stNum,swNum,stMean,stDev,swMean,swDev)
    #     print('Objective: ' + str(obj))
    #     print('*******')
    #     return obj
    #     # print(len(deck_order))
    #
    #
    # rp_bnd = (0, 0.99)
    # d_bnd = (0, 4.95)
    # f_bnd = (0, 4.95)
    # bnds = (rp_bnd,rp_bnd,f_bnd)
    # # minimum = fmin(run_bishara, [0.5, 0.5, 0.5], xtol=0.0000000000001)
    # minimum = minimize(run_bishara, [.5, .5, 2.5], method='SLSQP', bounds=bnds, tol=0.1)
    # print(minimum)