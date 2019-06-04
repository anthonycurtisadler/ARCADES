"""Module for transforming lists of numbers into formatted ranges
and formatted ranges into lists of numbers
pylint rated 9.68/10
"""

from globalconstants import EMPTYCHAR, DASH, COMMA, BLANK, COMMABLANK, SLASH, LONGDASH
from indexclass import Index

def de_range(range_string):

    """Takes a single formatted range and returns a list
    """

    if DASH not in range_string:
        return [int(range_string)]

    try:

        starting_number = int(range_string.split(DASH)[0])
        ending_number = int(range_string.split(DASH)[1])
        return list(range(starting_number, ending_number+1))

    except:
        pass

def range_set(entrystring):

    """takes a string with a sequence of ranges and returns
    list"""

    rangeset = set()
    if entrystring == EMPTYCHAR:
        return []

    if DASH not in entrystring and COMMA not in entrystring:
        return [int(entrystring)]

    for e_temp in [e_temp.strip() for e_temp in entrystring.split(COMMA) if
                   (e_temp.isnumeric() or e_temp.replace(DASH, EMPTYCHAR).isnumeric())]:
        rangeset = rangeset.union(set(de_range(e_temp)))
    return rangeset

def range_find(pageset):

    """Tranforms a list of pages into a formatted range
    """
        
    pagerangelist = []

    for page in sorted(pageset):

        if isinstance(page,int):

            if page in pageset and page-1 in pageset:

                pagerangelist[-1].append(str(page))

            elif page in pageset and not page-1 in pageset:

                pagerangelist.append([str(page)])

        if isinstance(page,str):
            if page.isnumeric():
                if page in pageset and str(int(page)-1) in pageset:

                    pagerangelist[-1].append(str(page))

                elif page in pageset and not str(int(page)-1) in pageset:

                    pagerangelist.append([str(page)])

        if type(page) == type(Index(0)):
            if page in pageset and page-Index(1) in pageset:

                pagerangelist[-1].append(str(page))

            elif page in pageset and not page-Index(1) in pageset:

                pagerangelist.append([str(page)])
            
            

    pagerangestringlist = []

    for pagerange in pagerangelist:

        if len(pagerange) == 1:
            pagerangestringlist.append(str(pagerange[0]))
        else:
            pagerangestringlist.append(str(pagerange[0])
                                       +LONGDASH+str(pagerange[-1]))

    return COMMABLANK.join(pagerangestringlist)
