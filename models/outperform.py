"""
    The "OUTPERFORM" Model:
        As the name suggests it is used to outperform the experiment without any cheating ofcourse. Just going through
        the whole thing in a very efficient way and without any mistakes.
"""
from util import Experiment, Subject, Statistics


record: {}
card_codes_txt = open('data/cards_codes.txt', "r")
card_stack = [[int(i) for i in line.strip().split(',')] for line in card_codes_txt]
criteria_list = [0, 1, 2, 3]


def rec(card, criteria, pile, match):
    """
    Records the Subjects card and choices in each step of the experiment (Not to be confused with record in statistics)
    :param card: Card in hand
    :param criteria: Criterion chosen in this step
    :param pile: Pile that the subject lands the card
    :param match: Response from the experiment (Match, No-Match)
    :return: None
    """
    global record
    record["Card"] = card
    record["Criterion"] = criteria
    record["Pile"] = pile
    record["Match"] = match


def simulate(card_order: [], crit_order: [], pile_order: []):
    """
    Simulates the outperform model
    :param card_order: The order of the deck in current trial
    :param crit_order: The order of expected criteria by the experiment in current trial
    :param pile_order: The order of Piles on the table in current trial
    :return: None
    """
    global record
    global card_stack
    global criteria_list
    strike = 0
    crit_found = False
    crit_confusion = False
    crit = 0  # Used by util
    results = [0, 0, 0]         # {0: possibleMatch, 1: correctMatch, 2:wrongMatch}
    record = {}                 # {0: selectedCriteria, 1:selectedPile, selectedCard}
    exp_results = []            # List of records for each card
    response = False
    old_crit: int
    streaks = 0
    prior_streak = 0
    crit_focus = 0
    alter_crit = 0

    if crit_order:
        criteria_list = crit_order
    if card_order:
        card_stack = card_order

    Experiment.start(crit_order, pile_order)

    for i, card in enumerate(card_stack):
        if strike == 10:
            # print("TOTAL STREAKS: " + str(streaks+1))
            prior = criteria_list[crit]
            crit = Experiment.change_criteria()
            if not streaks:
                post = -1
                tries = i - 10
                start = prior
            elif streaks == 1:
                post = prior
                prior = start
                tries = (i - 10) - prior_streak
            else:
                prior = post
                post = criteria_list[crit-1]
                tries = (i - 10) - prior_streak

            Statistics.record(tries, prior, post)
            streaks += 1
            # print("Prior: " + str(prior) + ", Post: " + str(post) + ", NumberOfTries: " + str(tries) + "\n")
            if crit == len(crit_order):
                print("ALL CRITERIA SORTED, TASK IS DONE!")
                break  # break if all the criteria to check have been sorted to
            prior_streak = i

        cur_card = Experiment.deal_card(card)
        if not cur_card:
            break
        if crit_found:
            # Case: sure of selected the correct criteria --> Continue on criterion until streak
            strike += 1
            selected_pile = Subject.pick_suitable_pile(cur_card, crit_focus)[0]
            response = Experiment.check_criteria(cur_card, selected_pile)
            rec(cur_card, crit_focus, selected_pile, response)
            cur_crit = criteria_list[crit]
            # print("Run " + str(i) + ": [Case: 'CritFound', Response: '" + str(response) + "', DemandedCriterion: '" +
            #       str(cur_crit) + "']")
            if not response:
                # Possible add remove the criteria that ended in the strike from the list!
                strike = 0
                crit_found = False
        elif crit_confusion:
            # Case where the second criterion was not True so you know the criteria is the possibleCrit
            crit_focus = alter_crit[0]
            selected_pile = Subject.pick_suitable_pile(cur_card, crit_focus)[0]
            response = Experiment.check_criteria(cur_card, selected_pile)
            rec(cur_card, crit_focus, selected_pile, response)
            cur_crit = criteria_list[crit]
            # print("Run " + str(i) + ": [Case: 'AlternateCheck', Response: '" + str(response) +
            # "', DemandedCriterion: '" + str(cur_crit) + "']")
            if response:
                strike += 1
            # else:
                # print("This is so wrong now!")
            crit_confusion = False
        else:
            if response:
                # Case: criteria was True on first run and needs to be doubleChecked
                results[0] += 1
                selected_pile = Subject.pick_suitable_pile(cur_card, crit_focus)[0]
                second_response = Experiment.check_criteria(cur_card, selected_pile)
                rec(cur_card, crit_focus, selected_pile, second_response)
                cur_crit = criteria_list[crit]
                # print("Run " + str(i) + ": [Case: 'SecondCheck', Response: '" + str(second_response) +
                #       "', DemandedCriterion: '" + str(cur_crit) + "']")
                if second_response:
                    # Case: Criteria was correct twice --> You've found the criteria
                    strike += 1
                    crit_found = True
                else:
                    # Case: criteria wrong on second run --> it must be the possibleCrit from the last run!
                    crit_confusion = True
                    strike = 0
            else:
                # Case: last picked criteria was False on first run --> Pick a new one and move on:
                if i == 0:
                    crit_focus = Subject.pick_criteria()
                else:
                    old_crit = crit_focus
                    crit_focus = Subject.pick_criteria(old_crit)
                selected_pile, alter_crit = Subject.pick_suitable_pile(cur_card, crit_focus)
                response = Experiment.check_criteria(cur_card, selected_pile)
                rec(cur_card, crit_focus, selected_pile, response)
                cur_crit = criteria_list[crit]
                # print("Run " + str(i) + ": [Case: 'Guess Criterion', Response: '" + str(response) +
                # "', 'DemandedCrit: " + str(cur_crit) + "']")
                if response:
                    strike += 1
                else:
                    strike = 0

        exp_results.append(record)
        i += 1
        # print(" SUBJECT:" + str(record) + "\n [CurStreak:" + str(strike) + "]\n")
    print("Total Streaks = " + str(streaks) +" \n" )
