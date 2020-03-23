"""
This package contains 3 classes that provide methods for simulating the experiment. and calculating the stats of
each trial.
"""

import numpy as np
import random

cardCodesTxt = open('data/cards_codes.txt', "r")
cardStack = [[int(i) for i in line.strip().split(',')] for line in cardCodesTxt]
pileCodes = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
criteriaList = [0, 1, 2, 3, 0]
crit = 0
curCrit = 6

global curCard
start_trials = np.zeros((4, 1))
start_stat = np.zeros((4, 1))
switch_trials = np.zeros((4, 4))
switch_stat = np.zeros((4, 4))


class Experiment:
    """
    Provides functions to simulate the experiment
    Methods:  1. deal_card 2. check_criteria 3.change criteria
    """
    @staticmethod
    def start(crit_order=[], pile_order=[]):
        """
        Sets-up the Experiment by setting up the criterion order, pile order...
        :param crit_order: By default goes through the list of criterions respectively (ie. Color, Fill, Topology,
        Position) repeating the first one (Color) in the end. Pass a list to change order (eg. [3,2,1,0,3])
        :param pile_order: Defaults to the piles in order (ie. [1111],[2222],[3333]) pass a list to change order
        (eg. [3,2,1])
        :return: None
        """
        global crit
        global curCrit
        global criteriaList
        global pileCodes
        crit = 0
        curCrit = 6
        if crit_order:
            criteriaList = crit_order
        if pile_order:
            pileCodes = [pileCodes[i-1] for i in pile_order]

    @staticmethod
    def deal_card(n: int):
        """
        Deals a card given a number revealing the information on card (ie. color, fill, topology, position respectively)
        :param n: Card number (see cards_codes.txt in root/data)
        :return: The information on card
        """
        global curCard
        try:
            curCard = cardStack[n]
            return curCard
        except:
            print("No More CARDS, Task is done!!")

    @staticmethod
    def check_criteria(cur_card: [], selected_pile: []):
        """
        Checks if the Criterion matches given a card and the selected pile
        :param cur_card: Card at hand
        :param selected_pile: The chosen pile by the subject
        :return: True/False
        """
        global crit
        global curCrit
        curCrit = criteriaList[crit]
        if selected_pile[curCrit] == cur_card[curCrit]:
            return True
        else:
            return False

    @staticmethod
    def change_criteria():
        """
        Goes to the next criterion. NOTE: The returned value is not the CRITERION itself but simply an index to be used
        to return the real criterion from the criterionList
        :return: The new criterion (:int)
        """
        global crit
        if crit < len(criteriaList):
            crit += 1
            print("Criterion changed! Currently: " + str(crit))
            return crit
        else:
            crit += 1
            return crit


criterions = [0, 1, 2, 3]


class Subject:
    """
    Provides functions to simulate tasks done on a subjects side.
    Methods:    1. pick_criteria(lastCrit): arbitrarily selects a criterion and spits it out as criteria_focus
                2. pick_suitable_pile(curCard, criteriaFocus): simulates searching for and placing your current
                card on a suitable pile based on the current criterion focus, and returns:
                    A. The selected pile.
                    B. The alternative possible criterion(in cases where current picked criterion is only
                        giving a false-correct feedback.
    """
    @staticmethod
    def pick_criteria(lastCrit: int = 4):
        """
        Selects an arbitrary criterion by default. unless the lastCriterion is passed to the function. In which case
        it selects a new one until the right criterion is found.
        :param lastCrit: The last picked criterion
        :return: The chosen criterion
        """
        global criterions
        try:
            criterions.remove(lastCrit)
        except:
            criterions = [0, 1, 2, 3]
        if not criterions:
            criterions = [0, 1, 2, 3]
        ran = random.randrange(len(criterions))
        criteria_focus = criterions[ran]
        return criteria_focus

    @staticmethod
    def pick_suitable_pile(cur_card: [], criteria_focus: int):
        """
        Searches for a suitable pile based on the card in hand and the chosen criterion. NOTE: multiple returns
        1. the selected pile as a list (of card codes eg. [1111]) 2. The possible criterion mismatch (ie. if the
        current criterion gives a fault-correct feedback.) this can happen since in each pile selection two criterions
        can match.
        :param cur_card: Card in hand
        :param criteria_focus: Selected Criterion
        :return: SelectedPile and Possible Alternative Criterion
        """
        for pile in pileCodes:
            if cur_card[criteria_focus] == pile[criteria_focus]:
                selected_pile = pile
                break
        a = np.array(cur_card)
        possible_crit = np.array(np.where(a == selected_pile[0]))
        possible_crit = possible_crit.tolist()[0]
        possible_crit.remove(criteria_focus)
        return selected_pile, possible_crit


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
        if post != -1:
            print("SWIIIITCH!")
            switch_trials[prior][post] += 1
            switch_stat[prior][post] = tries
        else:
            print("STAAAART!")
            start_trials[prior][0] += 1
            start_stat[prior][0] = tries

    @staticmethod
    def results():
        """
        Prints out the results of the statistics
        :return: None
        """
        print("Start Trials: ")
        print(start_trials)
        print("\nStart Stats: ")
        print(start_stat)
        print("\nSwitch Trials: ")
        print(switch_trials)
        print("\nSwitch Stats: ")
        print(switch_stat)











