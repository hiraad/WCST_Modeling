"""
CardsKeys:

    0) Color	1) Fill	    2) Topology		    3) Position    
    1: Blue		1: Empty	1: Contain  		1: Top
    2: Red		2: Full	    2: Partial overlap	2: Middle
    3: Yellow	3: Semi	    3: Disconnected		3: Bottom
"""

attention_weight = [0.25, 0.25, 0.25, 0.25]
signal = [0, 0, 0, 0]

feedback = [0, 0, 0, 0]

"""
    
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


"""
Free Parameters: 

    r = Rapidness of Attention Shifts toward feedback signals in reward trials
    [ranges from "0" to "1" | From "No" to "Complete" attention shifts respectively]
    p = Rapidness of Attention Shifts in punishment trials [same range as "r" | Higher value = better performance]
    d = Decision consistency parameter [Ranges .01 <= d <= 5 | Lower = More Random vs. Higher =  More Consistent Choice]
    f = Attentional Focus [Ranges "0.01" to "5" | 
        f ⇾ 0 = Even split of attention between dimensions given a signal;
        Higher (f = 1) = Proportional split of attention between dimensions;
        f ⇾ ∞ = Maximum attention shift to element that is consistent with the feedback.]
    
"""






