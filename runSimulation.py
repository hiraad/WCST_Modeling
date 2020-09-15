from util.calc import Statistics, Optimize
from util import Experiment
from models import bishara
from tqdm import tqdm
import pandas as pd
import cmd

# parameters = [0.90, 0.090, 2.5]
# parameters = [0.5, 0.5, 2.5]
# parameters = [0.0001, 0.0001, 0.0005]
# parameters = [0.90, 0.020, 2.17] # The parameter that Used to break
# parameters = [0.90197876, 0.09971949, 3.70380517]


class Main(cmd.Cmd):

    """
    Wisconsin Card Sorting Task Models
    """
    undoc_header = None

    experiment_instances = {}
    stat_results = {
        'start_n': [],
        'switch_n': [],
        'start_mean': [],
        'start_std': [],
        'switch_mean': [],
        'switch_std': []
    }

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if header is not None:
            cmd.Cmd.print_topics(self, header, cmds, cmdlen, maxcol)

    def do_setup(self, save=False):
        """
        Sets up the experiment employing the setup from the original experiment.
        Parameters:
            save(bool,default=False): If True saves the experiment class instances to the drive.
        """
        print()
        self.experiment_instances = Experiment.setup_experiment(save=save)
        print("======================================================\n")
        print("You can now run the model using the <bishara> command.\n")

    def do_bishara(self, p, save=False):
        """
        Runs the bishara model on all the setup experiments.
        Parameters:
            p(list,default=[0.5,0.5,2.5]): Takes the model's three parameters r,p,f respectively as a list.
            save(bool,default=False): If True saves the experiment trials as a csv file.
        """
        if not p:
            parameters = [0.5, 0.5, 2.5]
            print(parameters)
        else:
            parameters = [float(par) for par in p]

        stats = Statistics()
        for subject, exp in tqdm(Experiment.instances.items(), desc='Running the bishara model'):
            df = bishara.simulate(exp, parameters, save=save)
            stats.record(df)
        print("Model finished successfully, calculating results:")
        self.stat_results['start_n'], self.stat_results['switch_n'], self.stat_results['start_mean'], \
            self.stat_results['start_std'], self.stat_results['switch_mean'], self.stat_results['switch_std'] = \
            stats.calculate_results()
        print("\nResults are stored successfully.\n")

        print("======================================================\n")
        print("You can now print results using the <results> command. "
              "\nOr compare RMSE to target results using <RMSE>\n")

    def do_results(self, x):
        """
        Prints out the statistics results of the model
        """
        print(f"Number Of Start Trials:\n{self.stat_results['start_n']}\n \nNumber of Switch Trials: \n"
              f"{self.stat_results['switch_n']}\n\n::NUMBER OF TRIES:: \nStarts Mean: "
              f"\n{self.stat_results['start_mean']}\n \nStarts Standard Deviation:\n{self.stat_results['start_std']}"
              f"\n\nSwitch Means: \n{self.stat_results['switch_mean']}\n\nSwitch Standard Deviations: "
              f"\n{self.stat_results['switch_std']}\n")

    def do_optuna(self, iterations):
        """
        Finds optimum hyper parameters for the model employing the optuna library
        Parameters:
            iterations(int): Number of iterations
        """
        if not iterations:
            iterations = 100
        if not self.experiment_instances:
            print("Setup experiment using the 'setup' command first.")
        else:
            Optimize.optuna(iterations, self.experiment_instances)

    def do_minimize(self):
        """
        Finds optimum hyper-parameters for the model employing scipy.optimize, minimize library
        """
        Optimize.minimize(self.experiment_instances)

    def do_brute(self, rp_step, f_step):
        """
        Finds optimum hyper-parameters for the model employing scipy.optimize, brute library
        Parameters:
            rp_step(float): step_size for the r and p parameters (ranging 0-1)
            f_step(float): step-size for the f parameter (ranging 0-5)
        """
        if not self.experiment_instances:
            print("Setup experiment using the 'setup' command first.")
        else:
            Optimize.apply_brute(self.experiment_instances)

    def do_RMSE(self, target, verbose=True):
        """
        Calculates RMSE between the calculated model results and the base results from the original experiment.
        Parameters:
            target(String): Pass a keyword from ['start_n','switch_n','start_mean','start_std','switch_mean',
                                                 'switch_std'] to calculate RMSE.
            verbose(bool,default=True): If True prints out the target and predicted results array.
        """
        try:
            pred = self.stat_results[target]
        except KeyError:
            print("\nWrong argument passed, try <help RMSE> to see the correct syntax and"
                  " make sure you have successfully setup and run the experiment.\n")
            return False
        rmse = Statistics.RMSE(pred, target, verbose)
        print(f'{rmse}\n')

    def do_loop(self, args):
        """
        Loops the bishara model on a parameter set and prints out the min and max RMSE results.
        Parameters:
            args: inputs following arguments separated by a column ':'
                iterations(int): Number Of iterations
                p(list,default=[0.5,0.5,2.5]): List of parameters to run the model
        """

        if not self.experiment_instances:
            print("Setup experiment using the 'setup' command first.")
            return False

        args = args.split(':')
        p = args[1].replace(']', '').replace('[', '').split(',')
        iterations = int(args[0])
        print(f'ITERATIONS: {iterations}')

        if not p:
            parameters = [0.5, 0.5, 2.5]
            print(parameters)
        else:
            parameters = [float(par) for par in p]
            print(f'PARAMETERS:  {parameters}')



        rmse_list = []

        for i in range(1, iterations):
            stats = Statistics()
            for subject, exp in Experiment.instances.items():
                df = bishara.simulate(exp, parameters, save=False)
                stats.record(df)
            start_n, switch_n, start_mean, start_std, switch_mean, switch_std = stats.calculate_results()
            rmse = Statistics.RMSE(switch_std, 'switch_std')
            rmse_list.append(rmse)
        # print(rmse_list)
        print("===============")
        print(f"Min: {min(rmse_list)}, Max: {max(rmse_list)}\n")

    def default(self, arg):
        print("\n Command not found. \n")

    def do_EOF(self, line):
        return True

    def do_exit(self,*args):
        return True


if __name__ == "__main__":

    c = Main()
    c.intro = "\n==========================================\n" \
              "MODELLING THE WISCONSIN CARD SORTING TASK\n" \
              "==========================================\n\n" \
              "Try setting up the experiment using the <setup> command.\n\n" \
              "OR:\n" \
              "Type help to view list of commands.\n" \
              "Type help <command-name> for an extended doc on each command.\n" \
              "Arguments can be passed after the command using a whitespace and separated with a column.\n" \
              "Press <Ctrl+D> to quit.\n\n" \
              "==========================================\n"
    c.prompt = ">>>"
    c.doc_header = 'WCSTM Commands:'
    c.cmdloop()







