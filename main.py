from DFA.dfa import mainDFA
from NFA.nfa import mainNFA

def run(DFA=False, NFA=False):
    if DFA:
        mainDFA()
    if NFA:
        mainNFA()


run(DFA=True, NFA=True)


#DFA
# 		0		1
# >q0		q2		q1
# *q1		q3		q0
# q2		q0		q3
# q3		q1		q2

#NFA
# 		0			1
# >q0		{q0,q1}		{q0}
# q1		{q2,q3}	    {q4}
# q2		{q0,q2}		{q4}
# *q3		{}			{}
# *q4		{}			{}

# 10101011
# 001