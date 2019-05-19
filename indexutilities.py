## UTILITIES FOR INDEX REDUCTION & EXPANSION

from globalconstants import PERIOD,RIGHTPAREN, LEFTPAREN

def index_is_reduced (string):

    """Checks if an index-string is reduced"""

    x = string.split(PERIOD)
    for y in set(x):
        if y:
            if PERIOD+y+PERIOD+y+PERIOD in string or string.startswith(y+PERIOD+y+PERIOD) or string.endswith(PERIOD+y+PERIOD+y) or string == y+PERIOD+y:
                return False
    return True 
    
def index_reduce (string,paren=False):

    """Reduces an index-string to the abbreviated form"""
    
    string = PERIOD + string + PERIOD 

    if not index_is_reduced(string):
        x = string.split(PERIOD)
        for y in set(x):
            if y:
                for z in reversed(range(2,x.count(y)+1)):
                    if PERIOD + ((y + PERIOD) * (z-1))+y + PERIOD in string:
                        string  = string.replace(PERIOD + ((y + PERIOD) * (z-1))+y +PERIOD,PERIOD + LEFTPAREN*paren+y+'^'+str(z)+RIGHTPAREN*paren+PERIOD)
                        break 

    if not index_is_reduced(string):

        return index_reduce(string)
    while PERIOD+PERIOD in string:
        string = string.replace(PERIOD+PERIOD,PERIOD)
    return string[1:-1]

def index_expand (string):

    """Expands an index-string fro the abbreviated form"""

    if '(' in string:
        

        for x in string.split('('):
            if x:

                phrase = x.split(')')[0]
                if '^' in phrase:
                    a,b = phrase.split('^')[0], phrase.split('^')[1]
                    string = string.replace('('+phrase+')',(a+PERIOD)*(int(b)-1)+a)
        return string

    else:

        for x in string.split(PERIOD):
            if '^' in x:
                    a,b = x.split('^')[0], x.split('^')[1]
                    string = string.replace(x,(a+PERIOD)*(int(b)-1)+a)
        return string 

            
