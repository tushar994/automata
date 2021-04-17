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