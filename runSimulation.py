from util.calc import Statistics
from util import Experiment
from models import bishara
import pandas as pd
import os
# from scipy.optimize import fmin, minimize, Bounds

model = 'bishara'
parameters = [0.5, 0.5, 0.5]
# Experiment.reset_experiment()

# Run on all subjects

# for n in range(1, len(Experiment.base_decks)):
#     exp = Experiment.setup_experiment(n)
#     result_df = bishara.simulate(exp, parameters)


# Calculate the statistics

results_path = os.path.join('data', 'output', 'bishara')
for file in os.listdir(results_path):
    print('-----------------------')
    print(f'\nResults for {file}\n')
    df = pd.read_csv(os.path.join(results_path, file))
    Statistics.calculate(df)
    stt, swt, stMean, stStd, swMean, swStd = Statistics.results()
print(f"Number Of Start Trials:\n{stt}\n \nNumber of Switch Trials: \n{swt}\n \n::NUMBER OF TRIES:: \nStarts Mean: \n{stMean}\n"
      f"\nStarts Standard Deviation:\n{stStd}\n \nSwitch Means: \n{swMean}\n \nSwitch Standard Deviations: \n{swStd}")
















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
