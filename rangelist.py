"""Module for transforming lists of numbers into formatted ranges
and formatted ranges into lists of numbers
pylint rated 9.68/10
"""

from globalconstants import EMPTYCHAR, DASH, COMMA, BLANK, COMMABLANK, SLASH, LONGDASH
from indexclass import Index
from indexutilities import index_reduce

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

def range_find(pageset,reduce=True,compact=True):

    """Tranforms a list of pages into a formatted range
    Reduce to give indexes in a reduced form!
    """


    if compact:

        def integer_part (x):

            if '.' in str(x):
                return int(str(x).split('.')[0])
            else:
                return int(x)
            

        pages = set()
        pair_list = []
        integer_pages = set()
        for page in pageset:
            ip_temp = integer_part(page)
            integer_pages.add(ip_temp)
        
        all_indexes = sorted(integer_pages)
        del integer_pages
        try:
            starting = all_indexes[0]
        except:
            starting = 0
        
        ending = starting

        if len(all_indexes)>0:
            
            for ind in all_indexes[1:]:

                 if ind == ending + 1:
                      ending = ind
                 elif ind > ending + 1:
                      pair_list.append((starting,ending))
                      starting = ind
                      ending = ind
                 else:
                      pass
            if (len(pair_list)>0 and pair_list[-1] != (starting,ending)) or len(pair_list) == 0:
                     pair_list.append((starting,ending))
                 
            result = ''
            for pair in pair_list:
                 starting,ending = pair[0],pair[1]
                 if ending>starting:
                      result+=str(starting)+LONGDASH+str(ending)+', '
                 else:
                      result+=str(starting)+', '
            if len(result)>2:
                return result[0:-2]
            else:
                return ''
        else:
            return ''


        
    pagerangelist = []

    for page in sorted(pageset):

        if isinstance(page,int):

            if page in pageset and page-1 in pageset:

                pagerangelist[-1].append(str(page))

            elif page in pageset and not page-1 in pageset:

                pagerangelist.append([str(page)])

        elif isinstance(page,str):
            if page.isnumeric():
                if page in pageset and str(int(page)-1) in pageset:

                    pagerangelist[-1].append(str(page))

                elif page in pageset and not str(int(page)-1) in pageset:

                    pagerangelist.append([str(page)])

        elif type(page) == type(Index(0)):
            if page in pageset and page-Index(1) in pageset:

                pagerangelist[-1].append(str(page))

            elif page in pageset and not page-Index(1) in pageset:

                pagerangelist.append([str(page)])

    def redux (x):
        if reduce:
            return index_reduce(x)
        else:
            return x            
            

    pagerangestringlist = []

    for pagerange in pagerangelist:

        if len(pagerange) == 1:
            pagerangestringlist.append(redux(str(pagerange[0])))
        else:
            pagerangestringlist.append(redux(str(pagerange[0]))
                                       +LONGDASH+redux(str(pagerange[-1])))

    return COMMABLANK.join(pagerangestringlist)

