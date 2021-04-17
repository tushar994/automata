# from string_processing import *
import sys
import json


def remove_outer_bracket(str1):
    if(str1[0]=='('):
        bracket_var = 0
        for index,letter in enumerate(str1):
            if(letter=='('):
                bracket_var+=1
            elif(letter==')'):
                bracket_var-=1
            
            if(bracket_var==0 and index!=(len(str1)-1)):
                return str1
            
        return str1[1:len(str1)-1]

    else:
        return str1
# print(sys.argv[1])

File_object = open(sys.argv[1], "r")

data = json.loads(File_object.read())

dfa = data

dfa_transition_matrix = dfa["transition_function"]
dfa_start_states = dfa['start_states']
dfa_final_states = dfa['final_states']
dfa_states = dfa['states']
dfa_letters = dfa['letters']


# add starting start state with E to all the other Dfa start states
unique_start_state = ['unique_start_state']

for state in dfa_start_states:
    dfa_transition_matrix.append([unique_start_state[0], "$",  state])

dfa_states.append(unique_start_state[0])
# add final state with E going in from all actual final states
unique_final_state = ['unique_final_state']

for state in dfa_final_states:
    dfa_transition_matrix.append([state, "$",  unique_final_state[0]])

dfa_states.append(unique_final_state[0])

while(len(dfa_states)>2):
    # now we first make all the sets of edges between two common circles into one circle (+)
    new_transition_matrix = []
    for state1 in dfa_states:
        for state2 in dfa_states:
            # if(state1!=state2):
            all_edges =[]
            for edge in dfa_transition_matrix:
                if(edge[0]==state1 and edge[2]==state2):
                    all_edges.append(edge)

            new_edge = ""
            for index,edge in enumerate(all_edges):
                if(index!=0):
                    new_edge+="+"
                new_edge+= "(" + remove_outer_bracket(edge[1]) + ")"
            if(new_edge!=""):
                new_transition_matrix.append([state1, "(" + remove_outer_bracket(new_edge) + ")", state2])
            # else:
            #     for edge in dfa_transition_matrix:
            #         if(edge[0]==state1 and edge[2]==state2):
            #             new_transition_matrix.append(edge)

    # print("after making all same edges one")
    # print(new_transition_matrix)

    dfa_transition_matrix= new_transition_matrix

    # handle * case
    new_transition_matrix = []
    for edge in dfa_transition_matrix:
        new_transition_matrix.append(edge)

    for state1 in dfa_states:
        for edge in new_transition_matrix:
            if(edge[0]==state1 and edge[2]==state1):
                string_to_add = edge[1] + "*"
                dfa_transition_matrix.remove(edge)
                for index, edit_edge in enumerate(dfa_transition_matrix):
                    if(edit_edge[0]==state1 and edit_edge[2]!=state1):
                        dfa_transition_matrix[index][1] = "((" + string_to_add + ")(" + remove_outer_bracket(dfa_transition_matrix[index][1]) + ")"

    # print(dfa_transition_matrix)

    # now onto deleting states
    for state in dfa_states[:]:
        end_flag = 0
        if(not state in  unique_start_state and not state in unique_final_state):
            new_transition_matrix = [edge for edge in dfa_transition_matrix]
            going_in_list = []
            going_out_list = []
            for edge in dfa_transition_matrix:
                if(edge[2]==state):
                    going_in_list.append(edge)
                if(edge[0]==state):
                    going_out_list.append(edge)
            
            # for edge in dfa_transition_matrix:
            for edge_in in going_in_list:
                for edge_out in going_out_list:
                    dfa_transition_matrix.append([edge_in[0], "(" +remove_outer_bracket(edge_in[1]) + ")(" + remove_outer_bracket(edge_out[1]) + ")", edge_out[2]])
            
            
            for edge_in in going_in_list:
                dfa_transition_matrix.remove(edge_in)
            for edge_out in going_out_list:
                dfa_transition_matrix.remove(edge_out)
            end_flag = 1
            dfa_states.remove(state)
            break


# print(dfa_transition_matrix)
output = {'regex' : dfa_transition_matrix[0][1]}

# print(output)

json_object = json.dumps(output, indent = 4)


with open(sys.argv[2], "w") as outfile:
    outfile.write(json_object)