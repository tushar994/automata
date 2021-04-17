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