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

def create_parts(str1):
    components = []
    bracket_var = 0
    current_component = ""
    current_index = 0
    index = 0

    while index<len(str1):
        current_letter = str1[index]
        current_component += current_letter
        if(current_letter=='('):
            bracket_var+=1
        elif(current_letter==')'):
            bracket_var-=1
        
        if(bracket_var==0):
            if(index<len(str1)-1 and str1[index+1]=='*'):
                index+=1
                current_component+='*'
            components.append([current_component, current_index])
            current_index = index+1
            current_component = ""
        index+=1
    
    return components


def create_operation(str1):
    # get the parts
    components = create_parts(str1)

    # iif only one component then we have to do star
    if(len(components) == 1 and str1[len(str1)-1]=='*' ):
        return ['*' , str1[0:len(str1)-1] ]
    elif(len(components) == 1 and str1[len(str1)-1]!='*' ):
        return ['DONE']

    # try and get a plus
    for element in components:
        if(element[0]=='+'):
            return ['+' , str1[0:element[1]] , str1[element[1]+1 : len(str1)] ]
    
    # if all the above fail then gg
    return ['_' , str1[0:components[1][1]]  , str1[components[1][1] : len(str1)] ]


# print(sys.argv[1])

File_object = open(sys.argv[1], "r")

data = json.loads(File_object.read())

regex = data['regex']


# regex = input("please give regex\n\n")

output = {'states' : [], "letters" : [], "transition_matrix" : [], "start_states" : [], "final_states" : [] }

output['states'].append(1)
output['states'].append(2)

output['start_states'].append(1)
output['final_states'].append(2)

output["transition_matrix"].append([1,regex,2])

transition_matrix = []
transition_matrix.append([1,regex,2])

total_states = 2
start_states_set = {1}
final_states_set = {2}
states = set()
letters = set()

regex = list(regex)
while ' ' in regex:
    regex.remove(" ")




# convert to NFA with eta
while(True):
    number_edges_done = 0
    new_transition_matrix = []
    for edges in transition_matrix[:]:
        operation = create_operation(remove_outer_bracket(edges[1]))
        if(operation[0]=='DONE'):
            number_edges_done+=1
            new_transition_matrix.append([edges[0], remove_outer_bracket(edges[1]), edges[2]])
        else:
            if(operation[0]=='*'):
                new_circle1 = total_states+1
                total_states+=1
                new_circle2 = total_states+1
                total_states+=1
                new_transition_matrix.append(  [edges[0], '$' , new_circle1] )
                new_transition_matrix.append(  [new_circle1, remove_outer_bracket(operation[1]) , new_circle2] ) 
                new_transition_matrix.append(  [new_circle2, '$' , new_circle1] )
                new_transition_matrix.append(  [new_circle2, '$' , edges[2]] )
                new_transition_matrix.append(  [edges[0], '$' , edges[2]] )



                # new_transition_matrix.append(  [edges[0], remove_outer_bracket(operation[1]) , edges[0]] )
                # new_transition_matrix.append(  [edges[0], '$' , edges[2]] ) 
            elif(operation[0]=='+'):
                # new_circle1 = total_states+1
                # total_states+=1
                # new_circle2 = total_states+1
                # total_states+=1

                # new_circle3 = total_states+1
                # total_states+=1
                # new_circle4 = total_states+1
                # total_states+=1

                # new_transition_matrix.append( [ edges[0]  , '$' , new_circle1 ]  )
                # new_transition_matrix.append( [ new_circle1 , remove_outer_bracket(operation[1]) , new_circle2 ]  )
                # new_transition_matrix.append( [ new_circle2 , '$' , edges[2] ]  )

                # new_transition_matrix.append( [ edges[0]  , '$' , new_circle3 ]  )
                # new_transition_matrix.append( [ new_circle3 , remove_outer_bracket(operation[2]) , new_circle4 ]  )
                # new_transition_matrix.append( [ new_circle4  , '$' , edges[2] ]  )

                new_transition_matrix.append( [ edges[0]  , remove_outer_bracket(operation[1]) , edges[2] ]  )
                new_transition_matrix.append( [ edges[0]  , remove_outer_bracket(operation[2]) , edges[2] ]  )
            elif(operation[0]=='_'):
                new_transition_matrix.append( [ edges[0]  , remove_outer_bracket(operation[1]) , total_states+1 ]  )
                total_states+=1
                new_transition_matrix.append( [ total_states  , remove_outer_bracket(operation[2]) , edges[2] ]  )

    if(number_edges_done == len(transition_matrix)):
        break
    else:
        transition_matrix = new_transition_matrix

# print("first thing is")
# print(transition_matrix)

# print("\n\n\n\nstart of hell\n\n\n")
# remove eta
while(True):
    number_edges_done = 0
    new_transition_matrix = []
    epi_flag = 0
    for edges in transition_matrix[:]:
        if(edges[1]!='$'):
            new_transition_matrix.append(edges)
            number_edges_done += 1
        # elif(epi_flag==1):
            # new_transition_matrix.append(edges)
        else:
            first_state = edges[0]
            second_state = edges[2]
            if(first_state!=second_state):
                for line in transition_matrix[:]:
                    if(line[0]==second_state):
                        if( not [first_state, line[1], line[2] ] in transition_matrix):
                            new_transition_matrix.append( [first_state, line[1], line[2] ] )
                if(second_state in final_states_set):
                    final_states_set.add(first_state)
                if(first_state in start_states_set):
                    start_states_set.add(second_state)
                epi_flag = 1
            else:
                epi_flag = 1
    transition_matrix = new_transition_matrix
    # print(transition_matrix, end = "\n\n\n\n")
    if(epi_flag==0):
        break


for index,element in enumerate(transition_matrix):
    transition_matrix[index][0] = str("q" + str(transition_matrix[index][0]))
    transition_matrix[index][2] = str("q" + str(transition_matrix[index][2]))

for element in transition_matrix:
    letters.add(element[1])
    states.add(element[0])
    states.add(element[2])

letters = list(letters)
states = list(states)
final_states_set = [ "q"+str(ele) for ele in list(final_states_set)] 
start_states_set = [ "q"+str(ele) for ele in list(start_states_set)]

output = {'states' : states, "letters" : letters, "transition_matrix" : transition_matrix, "start_states" : start_states_set, "final_states" : final_states_set }

# print(output)

json_object = json.dumps(output, indent = 4)


with open(sys.argv[2], "w") as outfile:
    outfile.write(json_object)
# print("\n\nsecond thing is")
# print(transition_matrix)
# print("start states: ")
# print(start_states_set)
# print("final states: ")
# print(final_states_set)