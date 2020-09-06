from util import create_path
import pandas as pd
import numpy as np
import os
# Base Results:

start_n = [12, 11, 12, 9]
start_mtries = [20.75, 12.91, 5.58, 27.33]
start_sdtries = [22.59, 9.87, 8.83, 30.49]
sw_n = [16, 10, 14, 19, 13, 14, 14, 8]
sw_mtries = [11.13, 16, 15.29, 11.47, 11.69, 38.71, 6.86, 23.25]
sw_sdtries = [8.39, 13.13, 22.06, 13.38, 11.41, 28.18, 6.55, 26.44]

# Statistics placeholders:
start_trials = np.zeros((4))
start_tries = {"0": [], "1": [], "2": [], "3": []}
switch_trials = np.zeros((4, 4))
switch_tries = {"0_1": [], "0_3": [], "1_0": [], "1_2": [], "2_1": [], "2_3": [], "3_0": [], "3_2": []}
start_means = []
start_std = []


class Statistics:
    """
    Provides functions to calculate the statistics of each trial
    """

    @staticmethod
    def calculate(df):
        start_criterion = df.demanded_criterion[0]
        start_trials[start_criterion] += 1
        criterion_changes = df[df['demanded_criterion'].diff() != 0].demanded_criterion.to_numpy()
        criterion_indexes = df[df['demanded_criterion'].diff() != 0].index.to_numpy()
        streak_indexes = df[df['total_streaks'].notnull()].index.to_numpy()
        for i in range(0, len(criterion_changes)):
            prior_criterion = criterion_changes[i]
            if i < len(criterion_changes)-1:
                post_criterion = criterion_changes[i+1]
                switch_trials[prior_criterion][post_criterion] += 1
                tries = (streak_indexes[i] - 9) - criterion_indexes[i]
                if i == 0:
                    key = str(prior_criterion)
                    start_tries[key].append(tries)
                else:
                    key = f"{prior_criterion}_{post_criterion}"
                    switch_tries[key].append(tries)
        # print(f"Start Criterion is {start_criterion}\n{start_trials}")
        # print(streak_indexes)

    @staticmethod
    def record_means():
        global start_means
        global start_std
        start_means = [np.mean(tries) for key, tries in start_tries.items()]
        start_std = [np.std(tries, ddof=1) for key, tries in start_tries.items()]
        switch_means = [np.mean(tries) for key, tries in switch_tries.items()]
        switch_std = [np.std(tries, ddof=1) for key, tries in switch_tries.items()]
        return start_means, start_std, switch_means, switch_std

    @staticmethod
    def results():
        """
        Prints out the results of the statistics
        :return: None
        """
        global start_trials
        global switch_trials
        stMean, stStd, swMean, swStd = Statistics.record_means()
        stt = start_trials
        swt = switch_trials
        # start_trials = np.zeros((4, 1))
        # switch_trials = np.zeros((4, 4))
        # print("Start Trials: \n" + str(start_trials))
        # print("Start Means: " + str(stMean))
        # print("Start Deviations:\n" + str(stStd))
        # print("\nSwitch Trials: \n" + str(switch_trials))
        # print("Switch Mean: " + str(swMean))
        # print("Switch Deviations:\n" + str(swStd))
        return stt, swt, stMean, stStd, swMean, swStd


class Fit:

    @staticmethod
    def simplex(par):
        par0 = [.5, .5, .5]
        b = (0, .99)
        b2 = (0, 99)
        bounds = (b, b, b2)