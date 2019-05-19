"""Module containing input functions
pylint rated 10.0/10
"""
from globalconstants import YESTERMS, EMPTYCHAR, QUESTIONMARK


def i_input(prompt):


    """input function to return an integer."""

    while True:
        q_temp = input(prompt)
        if q_temp.isnumeric():
            return int(q_temp)

def s_input(prompt,
            inputtext):


    """ solicits input with prompt if inputtext is not
    empty, otherwise returns inputtext
    """

    if inputtext in [EMPTYCHAR, QUESTIONMARK]:
        inputtext = input(prompt)
    return inputtext



def q_input(prompt='CAUTION. Are you sure?',stackobject=None):

    """ This function is used to query if the
    user wishes to continue
    """
    if stackobject and stackobject.size() > 0:
        return stackobject.pop() in YESTERMS

    print(prompt, 'Yes to continue!')
    return input() in YESTERMS
