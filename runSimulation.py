from util.calc import Statistics, Optimize
from util import Experiment
from models import bishara
import pandas as pd
import os

model = 'bishara'
parameters = [0.53, 0.50, 4.47]
results_path = os.path.join('data', 'output', 'bishara')

'''
0. Setup The Experiment
'''
experiment_stages = Experiment.setup_experiment(save=False)

'''
1. Run The Model and Calculate the statistics
'''
# for subject, exp in Experiment.instances.items():
#     df = bishara.simulate(exp, parameters)
#     Statistics.record(df)
# stt, swt, stMean, stStd, swMean, swStd = Statistics.calculate_results()

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
# print(f"Number Of Start Trials:\n{stt}\n \nNumber of Switch Trials: \n{swt}\n \n::NUMBER OF TRIES:: \nStarts Mean: "
#       f"\n{stMean}\n \nStarts Standard Deviation:\n{stStd}\n \nSwitch Means: \n{swMean}\n "
#       f"\nSwitch Standard Deviations: \n{swStd}")

'''
4.  Find optimized hyperparameters
'''
Optimize.optuna(100, experiment_stages)



















