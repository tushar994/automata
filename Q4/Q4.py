
# from minimize_dfa_functions import *
import sys
import json


def check_if_state_in_list_set(list_set, state):
    for states in list_set:
        if(state in states):
            return 1
    return 0



def are_identical(state1,state2,P, transition_matrix,letters):
    for letter in letters:
        flag1 = -1
        flag2 = -1
        for transition in transition_matrix:
            if(transition[1]==letter):
                if(transition[0]==state1):
                    flag1 = find_set_belonging(transition[2],P)
                if(transition[0]==state2):
                    flag2 = find_set_belonging(transition[2],P)
        if(flag1!=flag2):
            return 0
    return 1



def find_set_belonging(state, P):
    for index,states in enumerate(P):
        if(state in states):
            return index
    return -1




# print(sys.argv[1])

File_object = open(sys.argv[1], "r")

data = json.loads(File_object.read())

dfa = data

dfa_transition_matrix = dfa["transition_function"]
dfa_start_states = dfa['start_states']
dfa_final_states = dfa['final_states']
dfa_states = dfa['states']
dfa_letters = dfa['letters']


P = [set(), set()]

# initialise P

reach_able_states = set()
for state in dfa_start_states:
    reach_able_states.add(state)

while True:
    flag = 0
    new_reach = set()
    for i in reach_able_states:
        new_reach.add(i)
    for i in reach_able_states:
        for step in dfa_transition_matrix:
            if(step[0]==i):
                new_reach.add(step[2])
    for i in new_reach:
        if(not i in reach_able_states):
            flag = 1
    if(flag==0):
        break
    reach_able_states = new_reach

dfa_states = list(reach_able_states)

for i in dfa_states:
    if(i in dfa_final_states):
        P[1].add(i)
    else:
        P[0].add(i)


while True:
    flag = 0
    new_P = []
    for state_set in P[:]:
        new_sets = []
        for state1 in state_set:
            if(not check_if_state_in_list_set(new_sets, state1)):
                current_set = set()
                current_set.add(state1)
                for state2 in state_set:
                    if(are_identical(state1,state2, P, dfa_transition_matrix, dfa_letters)):
                        current_set.add(state2)
                new_sets.append(current_set)
        
        for sets in new_sets:
            new_P.append(sets)
    
    for i in new_P:
        if not i in P:
            flag = 1
    if(flag==0):
        break
    P = new_P

# print(P)

final_transition_matrix = []

for state in P:
    i = list(state)
    cur_state = i[0]
    for transit in dfa_transition_matrix:
        if(transit[0]==cur_state):
            final_transition_matrix.append([i, transit[1], list(P[find_set_belonging(transit[2],P)] )])

# print(final_transition_matrix)

final_final_states = []

for state in P:
    i = list(state)
    if(i[0] in dfa_final_states):
        final_final_states.append(i)

# print(final_final_states)

final_start_states = []

for state in P:
    i = list(state)
    for k in i:
        if(k in dfa_start_states):
            if(not i in final_start_states):
                final_start_states.append(i)

# print(final_start_states)



output = {'states' : [list(i) for i in P], "letters" : dfa_letters, "transition_function" : final_transition_matrix, "start_states" : final_start_states, "final_states" : final_final_states }

# print(output)

json_object = json.dumps(output, indent = 4)


with open(sys.argv[2], "w") as outfile:
    outfile.write(json_object)