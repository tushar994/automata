Hi everyone,

This post is regarding the programming questions submission.
1. We are fixing the input, output, and submission formats. The evaluation will be automated so please ensure that you follow these formats exactly, as you will face a penalty otherwise.

Submission format: <roll_no>.zip which has the following -
└── <roll_no>
    ├── q1.py
    ├── q2.py
    ├── q3.py
    ├── q4.py
    ├── README.md
    └── Video

Contents of the README and video are explained in the latter part of the post.

2. Make sure all your scripts can be run by the command `python3 q<no>.py arg1 arg2` where arg1 is the path to the input JSON file and arg2 is the path to the output JSON file.

3. Specific input and output formats are given below. We have also attached example files for the conversion of NFA to DFA question so there is more clarity.
    3.1) Regular expression: {"regex": "<any_valid_regex>"} 
    eg. {"regex":"(a+b)*+ba+c*"} where the letters a,b,c comprise the alphabet.
    
    3.2) NFA: 
    {
        "states": [<array_of_all_states>],
        "letters": [<array_of_letters>],
        "transition_matrix": [
                                [<original_state>, <input_letter>, <new_state>],
                                [<original_state>, <input_letter>, <new_state>],
                                .
                                .
                                .
                        
                            ],
        "start_states": [<array_of_start_states>],
        "final_states": [<array_of_final_states>],
    }

    Note that for an NFA, the original state and input letter combination can repeat across multiple rows, as it is a non-deterministic machine (see NFA.json). 

    3.3) DFA will follow the same format as the NFA when given as an input. It is slightly different when in output, as then a state will be represented by an array of strings and not a single string (see DFA_q2_output.json). Hence, if you want to denote a combination of states "Q1" and "Q2" as a state in the output, it will be represented as ["Q1", "Q2"].

4. You do not have to perform state reduction in q2, as that is being tested in q4. Please submit all possible states as outputs in q2 (see DFA_q2_output.json).   

5. Please add a README that briefly explains your approach to each question and includes any assumptions that you may have made.

6. You have to create a short 2 minute screen recording of you running the scripts. Make sure to display the input and output format for each question. This is done only as a precaution so that we can grade the students who have not followed the correct format as well. 

Kindly use this thread to ask any doubts related to this assignment.

Cheers,
Automata Theory TAs

# Questions

Write a program to :

Convert regular expression to NFA

Convert NFA to DFA

Convert DFA to Regular expression.

Minimize a DFA


**For the regular expressions, you only need to account for the symbols '+' (union) and '*' (star). Concatenation has no specific character, it is just represented by writing two REs one after the other. Parenthesis '()' can be present in the regex for grouping.**

**Precedence order is star, followed by concatenation, and then union**

1. Use the character "$" to represent epsilon. 
2. Input alphabet can consist of any digits or English letters ("a-z0-9") as that is the convention followed in most literature. If your code is written for binary encodings as inputs, you can develop a mapping between the input letters and the encodings. 
3. Only valid regular expressions will be given as input.