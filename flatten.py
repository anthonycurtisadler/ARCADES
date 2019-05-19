"""Module to test and flatten a list into a flat list"""

def isflat(untyped):

    """tests if object is a flat set or list. Returns True for other types"""

    onlyelements = True
    if isinstance(untyped, (set, list)):
        for e_temp in list(untyped):
            if isinstance(e_temp, (set, list)):
                onlyelements = False
    return onlyelements

def flatten(untyped):

    """flattens a set or a list to a flat list"""

    return_elements = []
    if isinstance(untyped, (set, list)):

        for e_temp in list(untyped):
            if isflat(e_temp):
                if not isinstance(e_temp, (set, list)):
                    return_elements.append(e_temp)
                else:
                    for ee_temp in e_temp:
                        return_elements.append(ee_temp)

            else:
                print('not flat')
                for ee_temp in list(flatten(e_temp)):
                    return_elements.append(ee_temp)

    else:
        return untyped
    return return_elements
##while True:
##    x = input('?')
##    print(isflat(eval(x)))
##    print(flatten(eval(x)))pyton
