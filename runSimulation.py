from util.calc import Statistics, Optimize
from util import Experiment
from models import bishara
import pandas as pd


def main():

    print('\n===============================================================================\n')
    print('                     Wisconsin Card Sorting Task Modelling                       \n')

    # results_path = os.path.join('data', 'output', 'bishara')

    '''
    0. Setup The Experiment
    '''

    experiment_instances = Experiment.setup_experiment(save=False)

    '''
    1. Run The Model and Calculate the statistics
    '''
    model = ''
    while not model:
        model = input('Pick a model to simulate (bishara, outperform): ')

    try:
        parameters = list(map(float, input("Input parameters r, p, f separated by a comma"
                                           " (Enter for default 0.9, 0.9, 2.5): ").split(',')))

    except ValueError:
            # parameters = [0.90, 0.090, 2.5]
            parameters = [0.5, 0.5, 2.5]
            # parameters = [0.0001, 0.0001, 0.0005]
            # parameters = [0.90, 0.020, 2.17]
            # parameters = [0.90197876, 0.09971949, 3.70380517]
    '''
    Parameters that break:

    NANS:: 
    [0.90, 0.020, 2.17]

    '''

    # stats = Statistics()
    # for subject, exp in Experiment.instances.items():
    #     df = bishara.simulate(exp, parameters, save=False)
    #     stats.record(df)
    # start_n, switch_n, start_mean, start_std, switch_mean, switch_std = stats.calculate_results()

    '''
    2. Do so from the exported dataframes
    '''

    # for file in os.listdir(results_path):
    #     df = pd.read_csv(os.path.join(results_path, file))
    #     Statistics.record(df)
    # stt, swt, stMean, stStd, swMean, swStd = Statistics.calculate_results()

    '''
    3. Print Statistics Results
    '''

    # print(f"Number Of Start Trials:\n{start_n}\n \nNumber of Switch Trials: \n{switch_n}\n \n::NUMBER OF TRIES:: "
    #       f"\nStarts Mean: \n{start_mean}\n \nStarts Standard Deviation:\n{start_std}\n \nSwitch Means: "
    #       f"\n{switch_mean}\n\nSwitch Standard Deviations: \n{switch_std}")

    '''
    4.  Find optimized hyperparameters
    '''

    # 4.1. Optuna

    # Optimize.optuna(1000, experiment_instances)

    # 4.2. fmin

    # Optimize.minimize(experiment_instances)

    # 4.3. GridSearch(Brute)

    # Optimize.apply_brute(experiment_instances)

    '''
    5. RMSE the statistics results
    '''

    # rmse = Statistics.RMSE(switch_std, 'switch_std', True)
    # print(rmse)

    '''
    Loop on single parameter!
    '''
    # rmse_list = []
    # for i in range(1, 1000):
    #     stats = Statistics()
    #     for subject, exp in Experiment.instances.items():
    #         df = bishara.simulate(exp, parameters, save=False)
    #         stats.record(df)
    #     start_n, switch_n, start_mean, start_std, switch_mean, switch_std = stats.calculate_results()
    #     rmse = Statistics.RMSE(switch_std, 'switch_std', True)
    #     rmse_list.append(rmse)
    # print(rmse_list)
    # print("===============")
    # print(f"Min: {min(rmse_list)}")
    # print(f"Max: {max(rmse_list)}")


if __name__ == "__main__":
    main()








