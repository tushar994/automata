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