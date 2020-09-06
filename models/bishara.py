from util import Subject, create_path
from random import randrange, choice
import numpy as np
import pandas as pd
import os

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
df_path = os.path.join('data', 'output', 'bishara')


def select_criterion(attention_weight: []):
    mx = max(attention_weight)
    max_ind = [i for i, w in enumerate(attention_weight) if attention_weight[i] == mx]
    if len(max_ind) == 1:
        focused_crit = max_ind[0]
    else:
        focused_crit = choice(max_ind)
    return int(focused_crit)


def simulate(exp, par: []):
    # Model's three Vectors
    a = np.array([0.25, 0.25, 0.25, 0.25])
    m = np.zeros((len(exp.card_order), 4), float)
    s = np.zeros((len(exp.card_order), 4), float)

    # MODEL'S PARAMETERS:
    r = par[0]
    p = par[1]
    d = 1
    f = par[2]

    # Other Variables
    streak = 0
    total_streaks = 0
    rows = []

    for t in range(0, len(exp.card_order)):

        card_dimensions = exp.deal_card()
        selected_criterion = select_criterion(a)
        k, _ = Subject.select_pile(card_dimensions, selected_criterion)
        response, ambiguous, m_ind = exp.check_criterion(card_dimensions, k, selected_criterion)

        # Creating the current trial's Matching (m) vector
        m[t][:] = 0.000001
        for i in m_ind:
            m[t][i] = 1

        # Bishara Model:
        if response:
            streak += 1
            if ambiguous:
                m_sum = np.sum(m[t] * (a ** f))
                for dim in range(4):
                    s[t][dim] = ((m[t][dim]) * (a[dim] ** f)) / m_sum
            else:
                s[t] = m[t]
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
        # print(f"Trial: {exp.trial}, Current Card: {response}")
        row = [exp.trial, card_dimensions, exp.demanded_criterion, selected_criterion, response]
        if streak == 10:
            streak = 0
            total_streaks += 1
            row.append(total_streaks)
            demanded_criterion = exp.change_criterion()
            if demanded_criterion is None:
                print("All dimensions have been sorted to, The task is Done.")
                rows.append(row)
                break
        rows.append(row)
    results_df = pd.DataFrame(rows, columns=['trial', 'card', 'demanded_criterion', 'selected_criterion', 'feedback',
                                             'total_streaks'])
    create_path(df_path)
    results_df.to_csv(os.path.join(df_path, f'{exp.id}.csv'), index=False)
    print(f"Results for {exp.id}.csv successfully saved.\n")
    return results_df
