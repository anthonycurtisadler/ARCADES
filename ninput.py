"""Module containing input functions
pylint rated 10.0/10
"""
from globalconstants import YESTERMS, EMPTYCHAR, QUESTIONMARK
from indexclass import Index

def conv(x):

    if isinstance(x,str):
        return x
    if isinstance(x,(set,tuple,list)):
        return ', '.join(str(y) for y in x)
    


def i_input(prompt):


    """input function to return an integer."""

    while True:
        q_temp = input(prompt)
        if q_temp.isnumeric():
            return int(q_temp)

def s_input(prompt='',
            inputtext=None,
            typeflag=None,
            conditions=None,
            must_be_in=None,
            returnvalue=EMPTYCHAR):


    """ solicits input with prompt if inputtext is not
    empty, otherwise returns inputtext
    """

    if typeflag is None and conditions is None:
        if not inputtext or inputtext in [EMPTYCHAR, QUESTIONMARK]:
            inputtext = input(prompt)
        return inputtext
    if typeflag not in ['str','float','int','index']:
        return returnvalue

    else:
        not_ok = True
        condition_met = False
        query = ''
        counter = 0
        while counter<5 and (not_ok or (conditions and not condition_met) or (must_be_in and not condition_met)):
            if (not_ok and counter > 0) or (conditions and not condition_met and counter>0) \
               or (must_be_in and not condition_met and counter>0) \
               or not inputtext or inputtext in [EMPTYCHAR, QUESTIONMARK]:
                inputtext = input(prompt)
            not_found_in = False

            value = inputtext
                
            if typeflag:
                if typeflag == 'str':
                    not_ok = False
                elif typeflag == 'int':
                    try:
                        value = int(inputtext)
                        not_ok = False
                    except:
                        query = 'Input value must be integer '
                elif typeflag == 'float':
                    try:
                        value = float(inputtext)
                        not_ok = False
                    except:
                        query = 'Input value must be floating point '
                elif typeflag == 'index':
                    try:
                        value = Index(inputtext)
                        not_ok = False
                    except:
                        query =  'Input value must be an index '
            if not not_ok \
               and ((conditions and isinstance(conditions,(list,tuple)) and \
               len(conditions) > 1 and \
               (isinstance(conditions[0],(str,int,float)) or type(conditions[0])==type(Index(0))) and \
               (isinstance(conditions[1],(str,int,float)) or type(conditions[1])==type(Index(0)))) or
                    (must_be_in and isinstance(must_be_in,(str,list,set,tuple)))):

                if must_be_in and isinstance(must_be_in,(str,list,set,tuple)):
                    if inputtext in must_be_in:
                        condition_met = True
                    else:
                        query += '\nInput value must be in ' + conv(must_be_in)
                        not_found_in = True 
                        

                if  not not_found_in and (conditions and isinstance(conditions,(list,tuple)) and \
                    len(conditions) > 1 and \
                    (isinstance(conditions[0],(str,int,float)) or type(conditions[0])==type(Index(0))) and \
                    (isinstance(conditions[1],(str,int,float)) or type(conditions[1])==type(Index(0)))):
                    
                    
                
                    if value >= conditions[0] and value <= conditions[1]:
                        condition_met = True
                    else:
                        query += '\n Input value must be between ' + str(conditions[0]) + ' and ' + str(conditions[1])
            if not_ok or (not condition_met and (conditions or must_be_in)):
                print('ATTENTION',query)
            counter += 1
        if not inputtext:
            inputtext = returnvalue
        if (not_ok or (conditions and not condition_met) or (must_be_in and not condition_met)):
            if (not_ok and counter > 0) or (conditions and not condition_met and counter>0) \
               or (must_be_in and not condition_met and counter>0):
                return returnvalue
        return inputtext 
            
               
                       
                                                                                 
        
                    



def q_input(prompt='CAUTION. Are you sure?',stackobject=None):

    """ This function is used to query if the
    user wishes to continue
    """
    if stackobject and stackobject.size() > 0:
        return stackobject.pop() in YESTERMS

    print(prompt, 'Yes to continue!')
    return input() in YESTERMS
