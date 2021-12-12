from globalconstants import BLANK, EMPTYCHAR, QUESTIONMARK
import nformat

from notebookutilities import transpose_keys

from display import Display
display = Display ()


def nprint(*entries):
    """For printing in a boxed note"""
    
    text = ''
    for entry in entries:
        text += entry + BLANK

    if text.strip:    
        display.noteprint(('',text))
    else:
        print()
    

    

def si_input (prompt=EMPTYCHAR,
              inputtext=EMPTYCHAR,
              inputrange=range(-100000,100000),
              alert=(EMPTYCHAR,EMPTYCHAR)):

    """Inputs an integer value"""

    while True:
        if inputtext  in [EMPTYCHAR, QUESTIONMARK]:
            inputtext = input(prompt)
        if inputtext.isnumeric() and int(inputtext) in inputrange:
              return int(inputtext)
        inputtext = EMPTYCHAR
        display.noteprint(alert)






