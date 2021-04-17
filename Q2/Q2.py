# from find_epsilon import *
import sys
import json

def find_epsilon(dfa_start_state,transition_matrix):
    while True:
        dummy_set = set()
        for state in dfa_start_state:
            dummy_set.add(state)
            for move in transition_matrix:
                if(move[0]==state and move[1]=='$'):
                    dummy_set.add(move[2])
        if(dfa_start_state==dummy_set):
            break
        dfa_start_state = dummy_set
    return dfa_start_state


def find_next_state(state, transition_matrix, letter):
    final_set = set()
    for j in transition_matrix:
        if(j[1]==letter):
            if(j[0] in state):
                final_set.add(j[2])
                for k in find_epsilon(j[2], transition_matrix):
                    final_set.add(k)
    return final_set


def compare_lists(list1,list2):
    for i in list1:
        if not i in list2:
            return 0

    for j in list2:
        if not j in list1:
            return 0
    
    return 1


def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]


# print(sys.argv[1])

File_object = open(sys.argv[1], "r")

data = json.loads(File_object.read())

nfa = data

transition_matrix = nfa["transition_function"]
start_states = nfa['start_states']
final_states = nfa['final_states']
the_states = nfa['states']

from find_epsilon import *

power_states = list(powerset(nfa['states']))

power_states = [set(ele) for ele in power_states]

dfa_states = []
dfa_start_state = set()
dfa_states = []
dfa_letters = nfa['letters']

# find start state
for states in start_states:
    dfa_start_state.add(states)


# while True:
#     dummy_set = set()
#     for state in dfa_start_state:
#         dummy_set.add(state)
#         for move in transition_matrix:
#             if(move[0]==state and move[1]=='$'):
#                 dummy_set.add(move[2])
#     if(dfa_start_state==dummy_set):
#         break
#     dfa_start_state = dummy_set
dfa_start_state = find_epsilon(dfa_start_state,transition_matrix)


# dfa_states.append(dfa_start_state)
dfa_states = power_states

# print(dfa_start_state)

# Now we have the start state

dfa_transition_matrix = []

while True:
    flag = 0
    temp_states = []

    for state in dfa_states:
        if(not state in temp_states):
            temp_states.append(state)
        
        for letter in dfa_letters:
            reachables = set()
            for actions in transition_matrix:
                if(actions[1]==letter):
                    if(actions[0] in state):
                        reachables.add(actions[2])
            # if(len(reachables)==0):
                # continue
            reachables = find_epsilon(reachables,transition_matrix)
            if(not reachables in temp_states):
                temp_states.append(reachables)
            
            if( not [state, letter, reachables] in dfa_transition_matrix):
                dfa_transition_matrix.append([state, letter, reachables])
    
    for state in temp_states:
        if(not state in dfa_states):
            flag = 1
    dfa_states = temp_states
    if(flag==0):
        break


# finding final states
dfa_final_states = []
for state in dfa_states:
    for final_ones in final_states:
        if(final_ones in state):
            if(not state in dfa_final_states):
                dfa_final_states.append(state)



# print("transition matrix is")
# print(dfa_transition_matrix)
# print("\n")
# print("set of states is")
# print(dfa_states)
# print("start states are")
# print(dfa_start_state)
# print("final states are")
# print(dfa_final_states)


# getting transition matrix
final_transition_matrix = [ [(list(ele[0])),ele[1], (list(ele[2])) ]  for ele in dfa_transition_matrix]
final_states = [(list(ele)) for ele in dfa_states]
final_start_state = [(list(dfa_start_state))]
final_final_states = [  (list(ele)) for ele in dfa_final_states ]
final_letters = nfa['letters']


# print("yeah yeah yeah\n")
# x = len(the_states)
# masks = [1 << i for i in range(x)]
# for i in range(1 << x):
#     current_check = [ss for mask, ss in zip(masks, the_states) if i & mask]
#     for state in final_states:
#         if(compare_lists(state, current_check)):
#             continue
#     final_states.append(current_check)
#     for letter in final_letters:
#         if( not [current_check, letter, list(find_next_state(current_check, transition_matrix, letter))] in final_transition_matrix  ):
#             final_transition_matrix.append([current_check, letter, list(find_next_state(current_check, transition_matrix, letter))])



output = {'states' : final_states, "letters" : final_letters, "transition_function" : final_transition_matrix, "start_states" : final_start_state, "final_states" : final_final_states }


# print(output)

json_object = json.dumps(output, indent = 4)


with open(sys.argv[2], "w") as outfile:
    outfile.write(json_object)


