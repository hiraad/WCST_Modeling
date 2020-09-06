import numpy as np
import random
import json
import os
import pickle
# from models import bishara


with open('data/input/conditions.txt', "r") as file:
    conditions_json = json.load(file)

card_codes_text = open('data/input/cards_codes.txt', "r")
card_codes = [[int(i) for i in line.strip().split(',')] for line in card_codes_text]
pile_codes = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
criteria_list = [0, 1, 2, 3, 0]
crit = 0
curCrit = 6


def create_path(p):
    if not os.path.exists(p):
        os.makedirs(p)


class Experiment:

    # Experiment setup data from the original study:
    base_criteria = conditions_json[0]["Criterion_Order"]
    base_piles = conditions_json[1]["Target_Order"]
    base_decks = conditions_json[2]["Card_Order"]

    def __init__(self, subject, card_order, criterion_order, pile_order):
        self.id = subject
        self.card_order = card_order
        self.criterion_order = criterion_order
        self.pile_order = pile_order
        self.trial = 0
        self.current_card = None
        self.criterion_index = 0
        self.demanded_criterion = criterion_order[self.criterion_index]

    def deal_card(self):
        """
        Deals a card given a number revealing the information on card (ie. color, fill, topology, position respectively)
        :param n: Card number (see cards_codes.txt in root/data)
        :return: The information on card
        """
        self.trial += 1
        try:
            self.current_card = self.card_order[self.trial - 1]
            card_dimensions = card_codes[self.current_card]
            return card_dimensions
        except:
            print("No More CARDS, Task is done!!")
            return None

    def check_criterion(self, cur_card: [], selected_pile: [], c: int):
        m_ind = [i for i, dim in enumerate(cur_card) if cur_card[i] == selected_pile[i]]
        if selected_pile[self.demanded_criterion] == cur_card[self.demanded_criterion]:
            response = True
            ambiguity = True if len(m_ind) > 1 else False
        else:
            response = False
            ambiguity = True if len(m_ind) < 3 else False
        return response, ambiguity, m_ind

    def change_criterion(self):
        if self.criterion_index < len(criteria_list)-1:
            self.criterion_index += 1
            self.demanded_criterion = self.criterion_order[self.criterion_index]
            return self.demanded_criterion
        else:
            return None

    @staticmethod
    def reset_experiment():
        df_path = os.path.join('data', 'output', 'bishara')
        for df in os.listdir(df_path):
            os.remove(os.path.join(df_path, df))

    @staticmethod
    def setup_experiment(subject):
        card_order = Experiment.base_decks[subject - 1]
        criterion_order = Experiment.base_criteria[subject - 1]
        pile_order = Experiment.base_piles[subject - 1]
        experiment_path = os.path.join('data', 'experiment_instances')
        instance = os.path.join(experiment_path, f'{subject}.pickle')
        if os.path.exists(instance):
            with open(instance, 'rb') as pickle_file:
                exp = pickle.load(pickle_file)
                print("--------------------------")
                print(f"\nSubject {exp.id}, loaded.")
        else:
            exp = Experiment(subject, card_order, criterion_order, pile_order)
            print("--------------------------")
            print(f"\nSubject {exp.id}, Initialized.")
            with open(os.path.join(experiment_path, f'{subject}.pickle'), 'wb') as pickle_dump:
                pickle.dump(exp, pickle_dump)
        return exp


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
    def select_pile(cur_card: [], criteria_focus: int):
        """
        Searches for a suitable pile based on the card in hand and the chosen criterion. NOTE: multiple returns
        1. the selected pile as a list (of card codes eg. [1111]) 2. The possible criterion mismatch (ie. if the
        current criterion gives a fault-correct feedback.) this can happen since in each pile selection two criterions
        can match.
        :param cur_card: Card in hand
        :param criteria_focus: Selected Criterion
        :return: SelectedPile and Possible Alternative Criterion
        """
        for pile in pile_codes:
            if cur_card[criteria_focus] == pile[criteria_focus]:
                selected_pile = pile
                break
        a = np.array(cur_card)
        possible_crit = np.array(np.where(a == selected_pile[0]))
        possible_crit = possible_crit.tolist()[0]
        possible_crit.remove(criteria_focus)
        return selected_pile, possible_crit
