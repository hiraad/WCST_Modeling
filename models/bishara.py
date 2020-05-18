from util import Experiment, Subject, Statistics
from random import randrange, choice
import numpy as np
"""
CardsKeys:

    0) Color	1) Fill	    2) Topology		    3) Position    
    1: Blue		1: Empty	1: Contain  		1: Top
    2: Red		2: Full	    2: Partial overlap	2: Middle
    3: Yellow	3: Semi	    3: Disconnected		3: Bottom

Free Parameters: 

    r = Rapidness of Attention Shifts toward feedback signals in reward trials
    [ranges from "0" to "1" | From "No" to "Complete" attention shifts respectively]
    p = Rapidness of Attention Shifts in punishment trials [same range as "r" | Higher value = better performance]
    d = Decision consistency parameter [Ranges .01 <= d <= 5 | Lower = More Random vs. Higher =  More Consistent Choice]
    f = Attentional Focus [Ranges "0.01" to "5" | 
        f ⇾ 0 = Even split of attention between dimensions given a signal;
        Higher (f = 1) = Proportional split of attention between dimensions;
        f ⇾ ∞ = Maximum attention shift to element that is consistent with the feedback.]

Implement: 

    Unambiguous Rewarded Signal Vector:
        Indicates that given a "Correct" (unambiguous) signal attention should now shift towards a particular criterion.
        s[t] = m[t][k]
        
    Unambiguous Punished Signal Vector: 
        Indicates that given a "Wrong" (unambiguous) feedback attention should now shift towards a particular dimension.
        s[t] = [1,1,1,1] - m[t][k]

    Matching Vector "m" vector on trial(t) and chosen pile(k):
        i-th element of the vector has a value of "1" if the card matches the pile [k] at trial [t] & "0" otherwise.
        m[t][k] = [1, 0, 0, 0] (Indicating attention should move toward "color" for current trial and chosen pile.) 
        
    Attention Weight vector On Next Trial:
        a[t+1] | Rewarded = (1-r) * attention_weight + r * signal  
        a[t+1] | Punished = (1-p) * attention_weight + p * signal
    
    Predicted probability of choosing a pile (k) on trial (t):
        P[t][k] = ( m[t][k] * a[t] ^ d ) / sum(m[t][j] * a[t] ^ d) 
        Where j ranges between "1" to "3" for summation across all piles forcing Prediction Probability to add up to 1.
                
    Ambiguous Signal Vectors:
        s[t] | Rewarded = m[t][k][i] * (a[t][i] ^ f) / sum(m[t][k][h] * (a[t][h] ^ f) 
        s[t] | Punished = (1 - m[t][k][i]) * (a[t][i] ^ f) / sum(1 - m[t][k][h] * (a[t][h] ^ f)
        where h ranges between "1" to "4" for summation across all dimensions forcing feedback signal to add up to 1.
    
"""
record: {}


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


def crit_focus(attention_weight: []):
    mx = max(attention_weight)
    mx_ind = [i for i, w in enumerate(attention_weight) if attention_weight[i] == mx]
    if len(mx_ind) == 1:
        focused_crit = mx_ind[0]
        print("IT ALL COMES TO THIS MX: " + str(focused_crit))
    else:
        print("I Have to select a criterion Randomly")
        print("MXIND: " + str(mx_ind))
        focused_crit = choice(mx_ind)
    return int(focused_crit)


def simulate(card_order: [], crit_order: [], pile_order: []):
    """
    :param card_order: The order of the deck in current trial
    :param crit_order: The order of expected criteria by the experiment in current trial
    :param pile_order: The order of Piles on the table in current trial
    :return: None
    """
    a = np.array([0.25, 0.25, 0.25, 0.25])
    m = np.zeros((len(card_order), 4), float)
    s = np.zeros((len(card_order), 4), float)
    streak = 0
    t_streaks = 0  # Total number of achieved streaks
    crit = 0
    """
       ### MODEL PARAMETERS:
    """
    r = 1
    p = 1
    d = 1
    f = 1
    Experiment.start(crit_order, pile_order)
    for t, card_num in enumerate(card_order):
        p_a = a
        print("\nTrial: " + str(t+1))
        card = Experiment.deal_card(card_num)
        print("CARD: " + str(card))
        if not card:
            print("Out of cards! Job Finished.")
            break
        focused_crit = crit_focus(a)
        k, alt = Subject.pick_suitable_pile(card, focused_crit)  # Selected Pile Based on Criterion in focus
        print("Demanded Criterion: " + str(crit_order[crit]))
        print("Selected Criterion: " + str(focused_crit))
        print("Selected Pile: " + str(k))
        print("Current Attention Weight:" + str(np.round(p_a, 3)))

        # booleans response and ambiguous are self-explanatory , m_ind is a list of all ambiguous dimension indices
        response, ambiguous, m_ind = Experiment.check_criteria(card, k, focused_crit)
        m[t][:] = 0.000001
        for i in m_ind:
            m[t][i] = 1 # Just creating the M vector based on indices from check_criteria()
        print("M[t]: " + str(np.round(m[t], 2)))
        print("Response: " + str(response) + "\nAmbiguity: " + str(ambiguous))
        if response:
            streak += 1
            print("StreakCOUNT: " + str(streak))
            s[t] = m[t]  # Unambiguous
            if ambiguous:
                m_sum = np.sum(m[t] * (a ** f))
                for dim in range(4):
                    s[t][dim] = ((m[t][dim]) * (a[dim] ** f)) / m_sum
            a = ((1 - r) * a) + (r * s[t])
        else:
            streak = 0
            if ambiguous:
                m_sum = np.sum((1-m[t])*(a ** f))
                for dim in range(4):
                    s[t][dim] = ((1 - m[t][dim]) * (a[dim] ** f)) / m_sum
            else:
                s[t] = np.array([1, 1, 1, 1] - m[t])  # Unambiguous
            a = ((1 - p) * a) + (p * s[t])
        print("SIGNAL: " + str(np.round(s[t], 3)))
        print("NEW ATTENTION WEIGHT: " + str(np.round(a, 3)))
        if streak == 10:
            streak = 0
            cur = crit_order[crit]
            crit = Experiment.change_criteria()
            try:
                post = crit_order[crit]
            except IndexError:
                print("All Criterion Sorted To, Task is Done!")
                break
            if t_streaks == 0:
                tries = t - 9
            else:
                tries = t - tries
            Statistics.record(tries, cur, post)
            t_streaks += 1
            print("STREAAAAAAK!" + str(t_streaks))
    print("Total STREAKS ACHIEVED: " + str(t_streaks))




