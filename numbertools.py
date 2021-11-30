table=(['m',1000],['cm',900],['d',500],
       ['cd',400],['c',100],
       ['xc',90],['l',50],['xl',40],
       ['x',10],['ix',9],['v',5],['iv',4],['i',1])

def is_roman (entrystring):

    entrystring_copy = entrystring
    for x in ['cm','cd','xc','xl','ix','iv','m','c','d','l','x','v','i']:
        entrystring_copy = entrystring_copy.replace(x,'')
    if entrystring_copy:
        return False

    for x in ['m','c','x','i']:
        if entrystring.count(x)>5 or x*5 in entrystring:
            return False
    return True 
    

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

def de_range_numeric(string):

    returnset = set()
    for x in string.split(','):
        x = x.strip()
        if '-' not in x:
            if x.isnumeric():
                returnset.add(int(x))
        else:
            fh,th = x.split('-')[0:2]
            if fh.isnumeric() and th.isnumeric() and int(fh) <  int(th):
                for y in range(int(fh),int(th)+1):
                    returnset.add(y)
    return returnset
                
                              

def de_range(page_string):

    #ONLY WORKS FOR POSITIVE VALUES
    returnset = set()

    segments = [x.strip() for x in page_string.split(',')]
    for segment in segments:

        arabic_from, arabic_to, roman_from, roman_to = 0,0,0,0

        if not '-' in segment:
            returnset.add(segment)
        else:
            from_value, to_value = segment.split('-')[0],segment.split('-')[1]
            if from_value.isnumeric():
                arabic_from = int(from_value)
            else:
                roman_from = rom_to_int(from_value)
            if arabic_from and to_value.isnumeric() and int(to_value)>arabic_from:
                arabic_to = int(to_value)
            if roman_from and not to_value.isnumeric() and rom_to_int(to_value)>roman_from:
                roman_to = rom_to_int(to_value)

            if roman_from and roman_to:
                for x in range(roman_from,roman_to+1):
                    returnset.add(int_to_roman(x))
            if arabic_to and arabic_from:
                for x in range(arabic_from,arabic_to+1):
                    returnset.add(str(x))
    return returnset

                        
def abbreviate_range(range_string):
    
    rehyphen = lambda x,y:str(x)+'-'+str(y)
    def return_dif(x,y,two_or_more=False):
        x = str(x)
        y = str(y)
        if not len(x)==len(y):
            return x+'-'+y
        else:
            for index in range(len(x)-two_or_more):
                if x[index]!=y[index]:
                    break
            return x+'-'+y[index:]
     
            
    # for positive values only 
    if '-' not in range_string:
        return range_string
    left_value,right_value = range_string.split('-')
    if not (left_value+right_value).isnumeric():
        return range_string
    if not right_value>left_value:
        return rehyphen(left_value,right_value)
    left_value,right_value = int(left_value),int(right_value)
    if 0<=left_value<100:
        return rehyphen(left_value,right_value)
    elif left_value%100==0:
        return rehyphen(left_value,right_value)
    elif 0<left_value%100<10 and right_value-left_value<10:
        return return_dif(left_value,right_value)
    else:
        return return_dif(left_value,right_value,two_or_more=True)
        
def convert_range(ranges,split_phrase=',',join_phrase=', '):

    return join_phrase.join([abbreviate_range(x.strip()) for x in ranges.split(split_phrase)])

        
