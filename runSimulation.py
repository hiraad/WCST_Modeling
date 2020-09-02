# import json
from util import run_experiment
from models import bishara
# import numpy as np
# from scipy.optimize import fmin, minimize, Bounds

parameters = [0.5,0.5,0.5]
exp = run_experiment(7)
bishara.simulate(exp, parameters)





















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
