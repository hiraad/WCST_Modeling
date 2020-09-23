from scipy.optimize import minimize, brute
from models import bishara
from datetime import datetime
import numpy as np
import optuna
import util


class Statistics:

    def __init__(self):
        self.id = datetime.now()
        self.start_trials = np.zeros(4)
        self.switch_trials = np.zeros((4, 4))
        self.start_tries = {"0": [], "1": [], "2": [], "3": []}
        self.switch_tries = {"0_1": [], "0_3": [], "1_0": [], "1_2": [], "2_1": [], "2_3": [], "3_0": [], "3_2": []}
        self.no_switches = False

    def record(self, df):

        s_trials = np.zeros(4)
        s_tries = np.zeros(4)
        sw_trials = {"0_1": 0, "0_3": 0, "1_0": 0, "1_2": 0, "2_1": 0, "2_3": 0, "3_0": 0, "3_2": 0}
        sw_tries = {"0_1": 0, "0_3": 0, "1_0": 0, "1_2": 0, "2_1": 0, "2_3": 0, "3_0": 0, "3_2": 0}

        criterion_changes = df[df['demanded_criterion'].diff() != 0].demanded_criterion.to_numpy()
        criterion_indexes = df[df['demanded_criterion'].diff() != 0].index.to_numpy()
        streak_indexes = df[df['total_streaks'].notnull()].index.to_numpy()

        # check if the subject achieved any streaks at all...
        if streak_indexes.size == 0:
            sw_trials = [trial for key, trial in sw_trials.items()]
            sw_tries = [trial for key, trial in sw_tries.items()]

            return s_trials, s_tries, sw_trials, sw_tries

        start_criterion = df.demanded_criterion[0]
        self.start_trials[start_criterion] += 1
        s_trials[start_criterion] = 1

        # print(f"Criterion Indices: {criterion_indexes}")
        # print(f"Streak Indices: {streak_indexes}")
        # print(f"Criterion Changes: {criterion_changes}")

        for i in range(0, len(criterion_changes)):
            tries = None

            if len(streak_indexes) > i or i == 0:
                tries = (streak_indexes[i] - 9) - criterion_indexes[i]
                # print(tries)
            if i == 0:
                prior_criterion = criterion_changes[i]
                key = str(prior_criterion)
                self.start_tries[key].append(tries)
                s_tries[prior_criterion] = tries
            else:
                prior_criterion = criterion_changes[i-1]
                post_criterion = criterion_changes[i]
                # print("Switch RECORDED")
                key = f"{prior_criterion}_{post_criterion}"
                if tries is None:
                    continue
                self.switch_tries[key].append(tries)
                self.switch_trials[prior_criterion][post_criterion] += 1
                sw_trials[key] = 1
                sw_tries[key] = tries

        # sw_trials = np.reshape(sw_trials, (1, -1))
        # print(f"switch_trials: {sw_trials}")
        # print(f"switch_tries: {sw_tries}")

        sw_trials = [trial for key, trial in sw_trials.items()]
        sw_tries = [trial for key, trial in sw_tries.items()]

        return s_trials, s_tries, sw_trials, sw_tries

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
    def RMSE(p, t, verbose=False, subject='', gp=False):

        # Base Results:
        base_results = {
            'start_n': [12, 11, 12, 9],
            'start_mean': [20.75, 12.91, 5.58, 27.33],
            'start_std': [22.59, 9.87, 8.83, 30.49],
            'switch_n': [16, 10, 14, 19, 13, 14, 14, 8],
            'switch_mean': [11.13, 16, 15.29, 11.47, 11.69, 38.71, 6.86, 23.25],
            'switch_std': [8.39, 13.13, 22.06, 13.38, 11.41, 28.18, 6.55, 26.44]
        }

        if subject:
            base_r = util.load_obj('base_results')
            base_results = {
                'st_trial': base_r[subject][0],
                'st_try': base_r[subject][1],
                'sw_trial': base_r[subject][2],
                'sw_try': base_r[subject][3],
            }

        prediction = np.array(p)
        target = np.array(base_results[t])
        if gp:
            target = np.array(t)
        if verbose:
            print(f"Model Results: \n{prediction} \nBase Results: \n{target}\n")

        return np.sqrt(np.mean((prediction - target) ** 2))


class Optimize:

    experiment_instances = {}
    rmse_objective = ''
    subject = ''

    @staticmethod
    def simplex(par):
        par0 = [.5, .5, .5]
        b = (0, .99)
        b2 = (0, 99)
        bounds = (b, b, b2)

    @staticmethod
    def general_objective(par):
        stats = Statistics()
        if Optimize.subject:
            exp = Optimize.experiment_instances[Optimize.subject]
            df = bishara.simulate(exp, par)
            st_trial, st_try, sw_trial, sw_try = stats.record(df)
            model_results = {
                'st_trial': st_trial,
                'st_try': st_try,
                'sw_trial': sw_trial,
                'sw_try': sw_try
            }
            obj = Statistics.RMSE(model_results[Optimize.rmse_objective], Optimize.rmse_objective,
                                  subject=Optimize.subject, verbose=False)
        else:

            for subject, exp in Optimize.experiment_instances.items():
                df = bishara.simulate(exp, par)
                stats.record(df)
            start_n, switch_n, start_mean, start_std, switch_mean, switch_std = stats.calculate_results()

            model_results = {
                'start_n': start_n,
                'switch_n': switch_n,
                'start_mean': start_mean,
                'start_std': start_std,
                'switch_mean': switch_mean,
                'switch_std': switch_std
            }

            obj = Statistics.RMSE(model_results[Optimize.rmse_objective], Optimize.rmse_objective, verbose=True)
        return obj

    @staticmethod
    def optuna_objective(trial):
        r = trial.suggest_uniform('r', 0.1, 1)
        p = trial.suggest_uniform('p', 0.1, 1)
        f = trial.suggest_uniform('f', 0.1, 5)
        parameters = [r, p, f]
        print(f"Parameters: {parameters}")

        obj = Optimize.general_objective(parameters)

        return obj

    @staticmethod
    def optuna(n_trials, stages, objective, verbose=False, subject=''):

        Optimize.subject = subject
        Optimize.rmse_objective = objective
        Optimize.experiment_instances = stages

        study = optuna.create_study(study_name='bishara_opt')
        study.optimize(Optimize.optuna_objective, n_trials=n_trials, show_progress_bar=True)

        if verbose:
            print(study)
            print(f'Best trial until now: {study.best_trial.number}')
            print(' Value: ', study.best_trial)

    run = 0

    @staticmethod
    def scipy_objective(par):

        Optimize.run += 1

        # print(f"Run: {Optimize.run}")
        # print('Parameters: ' + str(par))

        obj = Optimize.general_objective(par)

        # print('Objective: ' + str(obj))
        # print('*******')
        return obj

    @staticmethod
    def minimize(stages, objective, subject=''):

        Optimize.subject = subject
        Optimize.rmse_objective = objective
        Optimize.experiment_instances = stages

        r_p_bnd = (0.0001, 0.99)
        f_bnd = (0.00001, 4.95)
        bounds = (r_p_bnd, r_p_bnd, f_bnd)

        minimum = minimize(Optimize.scipy_objective, x0=[.1, .1, .1], method='SLSQP', bounds=bounds)
        print(minimum)

    @staticmethod
    def apply_brute(stages, objective, subject=''):

        Optimize.subject = subject
        Optimize.rmse_objective = objective
        Optimize.experiment_instances = stages

        r_and_p = slice(0.1, 1.0, 0.1)
        f = slice(0.1, 4.9, 0.2)

        # x0, fval, grid, jout = brute(Optimize.scipy_objective, [r_and_p, r_and_p, f], full_output=True)
        # print(f"X0:{x0}\nfval:\n{fval}")
        # print(f"X0:{x0}\nfval:\n{fval}\ngrid:\n{grid}\nJout:\n{jout}")

        brute_results = brute(Optimize.scipy_objective, [r_and_p, r_and_p, f], full_output=True)
        print(f"Value: {brute_results[1]}, Parameters: {brute_results[0]}")
        return [brute_results[1], brute_results[0]]
