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
