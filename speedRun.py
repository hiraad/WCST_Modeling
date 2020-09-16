from util.calc import Statistics, Optimize
from util import Experiment
from models import bishara
from tqdm import tqdm
import pandas as pd
import os

# parameters = [0.90, 0.090, 2.5]
# parameters = [0.5, 0.5, 2.5]
# parameters = [0.0001, 0.0001, 0.0005]
# parameters = [0.90, 0.020, 2.17] # USED TO BREAK THE BISHARA MODEL
# parameters = [0.90197876, 0.09971949, 3.70380517]


def main():

    print('\n===============================================================================\n')
    print('                     Wisconsin Card Sorting Task Modelling                       \n')

    # results_path = os.path.join('data', 'output', 'bishara')

    experiment_instances = Experiment.setup_experiment(save=False)

    '''
    1. Run The Model and Calculate the statistics
    '''

    # stats = Statistics()
    # for subject, exp in Experiment.instances.items():
    #     df = bishara.simulate(exp, parameters, save=False)
    #     stats.record(df)
    # start_n, switch_n, start_mean, start_std, switch_mean, switch_std = stats.calculate_results()

    '''
    3. Print Statistics Results
    '''

    # print(f"Number Of Start Trials:\n{start_n}\n \nNumber of Switch Trials: \n{switch_n}\n \n::NUMBER OF TRIES:: "
    #       f"\nStarts Mean: \n{start_mean}\n \nStarts Standard Deviation:\n{start_std}\n \nSwitch Means: "
    #       f"\n{switch_mean}\n\nSwitch Standard Deviations: \n{switch_std}")

    '''
    4.  Find optimized Hyperparameters
    '''

    # 4.1. Optuna

    Optimize.optuna(1000, experiment_instances, verbose=True)

    # 4.2. fmin

    # Optimize.minimize(experiment_instances)

    # 4.3. GridSearch(Brute)

    # Optimize.apply_brute(experiment_instances)

    '''
    5. RMSE the statistics results
    '''

    # rmse = Statistics.RMSE(switch_std, 'switch_std', verbose=True)
    # print(rmse)

    '''
    6. Loop on single parameter!
    '''

    # parameter_sets = [[0.9, 0.09, 2.5], [0.5, 0.5, 2.5], [0.0001, 0.0001, 0.0005], [0.9, 0.02, 2.17],
    #                   [0.90197876, 0.09971949, 3.70380517], [0.9, 0.9, 4.9], [0.1, 0.9, 4.9], [0.9, 0.1, 4.9],
    #                   [0.9, 0.9, 0.1], [0.9, 0.9, 0.9], [0.5, 0.5, 4.9], [0.5, 0.5, 0.1], [0.5, 0.5, 0.9],
    #                   [0.5, 0.1, 2.5], [0.5, 0.1, 0.1], [0.1, 0.5, 0.1], [0.5, 0.1, 4.9], [0.1, 0.5, 4.9],
    #                   [0.9, 0.9, 2.5], [0.9, 0.1, 2.5], [0.1, 0.9, 2.5], [0.7, 0.7, 3.1], [0.0001, 0.0001, 4.9],
    #                   [0.0001, 0.0001, 2.5], [0.0001, 0.9, 0.0005], [0.9, 0.0001, 0.0005], [0.0001, 0.9, 4.9],
    #                   [0.9, 0.0001, 4.9], [0.0001, 0.9, 2.5], [0.9, 0.0001, 2.5], [0.0001, 0.9, 4.9]]
    # par_dynamics_path = os.path.join('data', 'output', 'parameter_dynamics.txt')
    # with open(par_dynamics_path, "w") as text_file:
    #
    #     for parameter_set in tqdm(parameter_sets, desc='Calculating results'):
    #
    #         st_trial_rmse = []
    #         st_mean_rmse = []
    #         st_std_rmse = []
    #         sw_std_rmse = []
    #         sw_mean_rmse = []
    #         sw_trial_rmse = []
    #
    #         for i in tqdm(range(1, 1000)):
    #             stats = Statistics()
    #             for subject, exp in Experiment.instances.items():
    #                 df = bishara.simulate(exp, parameter_set, save=False)
    #                 stats.record(df)
    #             start_n, switch_n, start_mean, start_std, switch_mean, switch_std = stats.calculate_results()
    #             rmse = Statistics.RMSE(start_n, 'start_n')
    #             st_trial_rmse.append(rmse)
    #             rmse = Statistics.RMSE(start_mean, 'start_mean')
    #             st_mean_rmse.append(rmse)
    #             rmse = Statistics.RMSE(start_std, 'start_std')
    #             st_std_rmse.append(rmse)
    #             rmse = Statistics.RMSE(switch_n, 'switch_n')
    #             sw_trial_rmse.append(rmse)
    #             rmse = Statistics.RMSE(switch_mean, 'switch_mean')
    #             sw_mean_rmse.append(rmse)
    #             rmse = Statistics.RMSE(switch_std, 'switch_std')
    #             sw_std_rmse.append(rmse)
    #
    #         print("\n===========================\n", file=text_file)
    #         print(f"Parameters: {parameter_set}", file=text_file)
    #         print("\nSTARTS:", file=text_file)
    #         print(f"Start_Trials_Min: {min(st_trial_rmse)}", file=text_file)
    #         print(f"Start_Trials_Max: {max(st_trial_rmse)}", file=text_file)
    #         print(f"Start_Means_Min: {min(st_mean_rmse)}", file=text_file)
    #         print(f"Start_Means_Max: {max(st_mean_rmse)}", file=text_file)
    #         print(f"Start_STD_Min: {min(st_std_rmse)}", file=text_file)
    #         print(f"Start_STD_Max: {max(st_std_rmse)}", file=text_file)
    #         print("\nSWITCHES:", file=text_file)
    #         print(f"Switch_Trials_Min: {min(sw_trial_rmse)}", file=text_file)
    #         print(f"Switch_Trials_Max: {max(sw_trial_rmse)}", file=text_file)
    #         print(f"Switch_Means_Min: {min(sw_mean_rmse)}", file=text_file)
    #         print(f"Switch_Means_Max: {max(sw_mean_rmse)}", file=text_file)
    #         print(f"Switch_STD_Min: {min(sw_std_rmse)}", file=text_file)
    #         print(f"Switch_STD_Max: {max(sw_std_rmse)}", file=text_file)
    #         print("\n===========================\n", file=text_file)


if __name__ == "__main__":
    main()








