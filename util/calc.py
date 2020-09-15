from scipy.optimize import minimize, brute
from models import bishara
from datetime import datetime
import numpy as np
import optuna


class Statistics:

    def __init__(self):
        self.id = datetime.now()
        self.start_trials = np.zeros(4)
        self.switch_trials = np.zeros((4, 4))
        self.start_tries = {"0": [], "1": [], "2": [], "3": []}
        self.switch_tries = {"0_1": [], "0_3": [], "1_0": [], "1_2": [], "2_1": [], "2_3": [], "3_0": [], "3_2": []}
        self.no_switches = False

    def record(self, df):
        start_criterion = df.demanded_criterion[0]
        self.start_trials[start_criterion] += 1
        criterion_changes = df[df['demanded_criterion'].diff() != 0].demanded_criterion.to_numpy()
        criterion_indexes = df[df['demanded_criterion'].diff() != 0].index.to_numpy()
        streak_indexes = df[df['total_streaks'].notnull()].index.to_numpy()

        # print(criterion_changes)
        # print(criterion_indexes)
        # print(streak_indexes)

        for i in range(0, len(criterion_changes)):
            tries = None

            if len(streak_indexes) > i or i == 0:
                # this if ensures that the start tries doesnt get recorded again as the first switch
                tries = (streak_indexes[i] - 9) - criterion_indexes[i]
                # print(tries)
            if i == 0:
                prior_criterion = criterion_changes[i]
                key = str(prior_criterion)
                self.start_tries[key].append(tries)
            else:
                prior_criterion = criterion_changes[i-1]
                post_criterion = criterion_changes[i]
                # print("Switch RECORDED")
                key = f"{prior_criterion}_{post_criterion}"
                if tries is None:
                    continue
                self.switch_tries[key].append(tries)
                self.switch_trials[prior_criterion][post_criterion] += 1

    def calculate_results(self):
        start_means = [np.mean(tries) for key, tries in self.start_tries.items()]
        start_std = [np.std(tries, ddof=1) for key, tries in self.start_tries.items()]
        if [switch for switch in self.switch_tries.values() if switch]:
            switch_means = [np.mean(tries) for key, tries in self.switch_tries.items()]
            switch_std = [np.std(tries, ddof=1) for key, tries in self.switch_tries.items()]
            switch_trials = self.switch_trials[self.switch_trials != 0]
            switch_trials = np.reshape(switch_trials, (1, -1))
        else:
            switch_trials = [0, 0, 0, 0, 0, 0, 0, 0]
            switch_means = [0, 0, 0, 0, 0, 0, 0, 0]
            switch_std = [0, 0, 0, 0, 0, 0, 0, 0]

        return self.start_trials, switch_trials, start_means, start_std, switch_means, switch_std

    @staticmethod
    def RMSE(p, t, print_result=False):

        # Base Results:
        base_results = {
            'start_n': [12, 11, 12, 9],
            'start_mean': [20.75, 12.91, 5.58, 27.33],
            'start_std': [22.59, 9.87, 8.83, 30.49],
            'switch_n': [16, 10, 14, 19, 13, 14, 14, 8],
            'switch_mean': [11.13, 16, 15.29, 11.47, 11.69, 38.71, 6.86, 23.25],
            'switch_std': [8.39, 13.13, 22.06, 13.38, 11.41, 28.18, 6.55, 26.44]
        }
        prediction = np.array(p)
        target = np.array(base_results[t])
        if print_result:
            print(f"Model Results: \n{prediction} \nBase Results: \n{target}\n")

        return np.sqrt(np.mean((prediction - target) ** 2))


class Optimize:

    experiment_instances = {}

    @staticmethod
    def simplex(par):
        par0 = [.5, .5, .5]
        b = (0, .99)
        b2 = (0, 99)
        bounds = (b, b, b2)

    @staticmethod
    def optuna_objective(trial):
        r = trial.suggest_uniform('r', 0.1, 1)
        p = trial.suggest_uniform('p', 0.1, 1)
        f = trial.suggest_uniform('f', 0.1, 5)
        parameters = [r, p, f]
        stats = Statistics()
        for subject, exp in Optimize.experiment_instances.items():
            df = bishara.simulate(exp, parameters)
            stats.record(df)
        start_n, switch_n, start_mean, start_std, switch_mean, switch_std = stats.calculate_results()

        # obj = Statistics.RMSE(switch_mean, 'switch_mean')
        obj = Statistics.RMSE(switch_std, 'switch_std')
        # obj = Statistics.RMSE(switch_n, 'switch_n', True)

        return obj

    @staticmethod
    def optuna(n_trials, stages):
        Optimize.experiment_instances = stages
        study = optuna.create_study(study_name='bishara_opt')
        study.optimize(Optimize.optuna_objective, n_trials=n_trials)
        print(study)
        print(f'Best trial until now: {study.best_trial.number}')
        print(' Value: ', study.best_trial)

    run = 0

    @staticmethod
    def scipy_objective(par):
        Optimize.run += 1
        print(f"Run: {Optimize.run}")
        print('Parameters: ' + str(par))
        stats = Statistics()
        for subject, exp in Optimize.experiment_instances.items():
            df = bishara.simulate(exp, par)
            stats.record(df)

        start_n, switch_n, start_mean, start_std, switch_mean, switch_std = stats.calculate_results()

        # obj = Statistics.RMSE(switch_mean, 'switch_mean_tries', True)
        obj = Statistics.RMSE(switch_std, 'switch_std', True)
        # obj = Statistics.RMSE(switch_n, 'switch_n', True)

        print('Objective: ' + str(obj))
        print('*******')
        return obj

    @staticmethod
    def minimize(stages):
        Optimize.experiment_instances = stages
        r_p_bnd = (0.0001, 0.99)
        f_bnd = (0.00001, 4.95)
        bnds = (r_p_bnd, r_p_bnd, f_bnd)
        minimum = minimize(Optimize.scipy_objective, x0=[.1, .1, .1], method='SLSQP', bounds=bnds)
        print(minimum)

    @staticmethod
    def apply_brute(stages):
        Optimize.experiment_instances = stages
        # r_and_p = slice(0.1, 1.0, 0.001)
        # f = slice(0.1, 4.9, 0.001)
        r_and_p = slice(0.1, 1.0, 0.1)
        f = slice(0.1, 4.9, 0.2)
        x0, fval, grid, jout = brute(Optimize.scipy_objective, [r_and_p, r_and_p, f], full_output=True)
        print(f"X0:{x0}\nfval:\n{fval}\ngrid:\n{grid}\nJout:\n{jout}")
        brute_results = brute(Optimize.scipy_objective, [r_and_p, r_and_p, f], full_output=True)
        print(brute_results)