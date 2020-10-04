table=(['m',1000],['cm',900],['d',500],
       ['cd',400],['c',100],
       ['xc',90],['l',50],['xl',40],
       ['x',10],['ix',9],['v',5],['iv',4],['i',1])

def rom_to_int(entrystring):


    returnint=0
    for pair in table:

        continueyes=True
        
        while continueyes:
            if len(entrystring)>=len(pair[0]):

                if entrystring[0:len(pair[0])]==pair[0]:
                    returnint+=pair[1]
                    entrystring=entrystring[len(pair[0]):]
 
                else: continueyes=False
            else: continueyes=False

    return returnint


def int_to_roman (integer,lower=False):

    returnstring=''

    for pair in table:

        while integer-pair[1]>=0:

            integer-=pair[1]
            returnstring+=pair[0]
            
    if lower==True:
        lowerstring=''
        for a in returnstring: lowerstring+=a.lower()
        returnstring=lowerstring
    return returnstring

def range_find(pageset,romanize=False):

    def convert (x):

        if not romanize:
            return x
        else:
            return int_to_roman(int(x))

    pagerangelist=[]

    

    for page in sorted(pageset):

        if page in pageset and page-1 in pageset:

            pagerangelist[-1].append(str(page))
            
        elif page in pageset and not (page-1 in pageset):

            pagerangelist.append([str(page)])

    pagerangestringlist=[]

    for pagerange in pagerangelist:
        
        if len(pagerange)==1:
            pagerangestringlist.append(convert(pagerange[0]))
        else:
            pagerangestringlist.append(convert(pagerange[0])+'-'+convert(pagerange[-1]))

    return ','.join(pagerangestringlist)


def format_range(page_set):

    roman_numerals = [rom_to_int(x) for x in page_set if not x.isnumeric()]
    arabic_numerals = [int(x) for x in page_set if x.isnumeric()]
    to_return = ''
    roman_range = range_find(roman_numerals,romanize=True)
    arabic_range = range_find(arabic_numerals,romanize=False)
    if roman_range.replace(' ',''):
        to_return += roman_range
    if to_return and arabic_range.replace(' ',''):
        to_return += ',' + arabic_range.replace(' ','')
    elif arabic_range.replace(' ',''):
        to_return += arabic_range.replace(' ','')
    

    return to_return

