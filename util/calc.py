
# Base Results:

start_n = [12,11,12,9]
start_mtries = [20.75,12.91,5.58,27.33]
start_sdtries = [22.59, 9.87, 8.83, 30.49]
sw_n = [16,10,14,19,13,14,14,8]
sw_mtries = [11.13,16,15.29,11.47,11.69,38.71,6.86,23.25]
sw_sdtries = [8.39, 13.13, 22.06, 13.38, 11.41, 28.18, 6.55, 26.44]

# Statistics placeholders:
start_trials = np.zeros((4, 1))
start_stat = {"0": [], "1": [], "2": [], "3": []}
switch_trials = np.zeros((4, 4))
switch_stat = {"0_1": [], "0_3": [], "1_0": [], "1_2": [], "2_1": [], "2_3": [], "3_0": [], "3_2": []}
start_means = []
start_std = []


class Statistics:
    """
    Provides functions to calculate the statistics of each trial
    """

    @staticmethod
    def record(tries: int, prior: int, post: int = -1):
        """
        Records the results (ie. Number of times a criterion is asked for and the Number of tries until a criterion is
        found) in A matrix where each row and column corresponds to every criterion respectively (Color, Fill, Topology,
        Position) for two different categories:
        1. Starting with a criterion recorded in a (4x1) Matrix
        2. Switch from criterion to another recorded in a (4x4) Matrix
        :param tries: Number of tries until the criterion was found
        :param prior: The Criterion that was asked for
        :param post: The Next Criterion
        :return: None
        """
        global start_stat
        global start_trials
        global switch_stat
        global switch_trials
        if post == -1:
            key = str(prior)
            start_trials[prior][0] += 1
            start_stat[key].append(tries)
        else:
            key = str(prior) + "_" + str(post)
            switch_trials[prior][post] += 1
            switch_stat[key].append(tries)

    @staticmethod
    def record_means():
        global start_means
        global start_std
        start_means = [np.mean(tries) for key, tries in start_stat.items()]
        start_std = [np.std(tries, ddof=1) for key, tries in start_stat.items()]
        switch_means = [np.mean(tries) for key, tries in switch_stat.items()]
        switch_std = [np.std(tries, ddof=1) for key, tries in switch_stat.items()]
        return start_means, start_std, switch_means, switch_std

    @staticmethod
    def results():
        """
        Prints out the results of the statistics
        :return: None
        """
        global start_trials
        global switch_trials
        stMean, stStd, swMean, swStd  = Statistics.record_means()
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