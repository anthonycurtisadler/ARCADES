"""Module containing the extract function
pylint rated 9.64/10
"""

from globalconstants import LEFTNOTE, RIGHTNOTE, EMPTYCHAR
def extract(entrytext,
            lchar,
            rchar):

    """extracts all the textblocks surrounded by lchar and rchar from
        entrytext"""


    def indexlist(entrytext,
                  char):

        """Creates a list of the indexes of segments
        to be extracted
        """

        rl_temp = []
        indexfrom = 0
        for a_temp in range(entrytext.count(char)):


            indexat = entrytext.index(char)

            rl_temp.append(indexat+indexfrom)
            indexfrom += indexat+len(char)
            entrytext = entrytext.split(char, 1)[1]


        return rl_temp

    def isregular(entrytext,
                  lchar,
                  rchar):
        """checks to see if the text has an equal number of
        properly nested lchar and rchar
        """

        llist = indexlist(entrytext, lchar)
        rlist = indexlist(entrytext, rchar)

        returnlist = []

        if len(llist) != len(rlist) or not llist:
            return False
        rlist = iter(indexlist(entrytext, rchar))

        for a_temp in llist:
            returnlist.append(a_temp)
            returnlist.append(next(rlist))

        if returnlist == sorted(returnlist):
            return True
        return False

    if not isregular(entrytext, lchar, rchar):
        return []
    llist = indexlist(entrytext, lchar)

    literator = iter(llist)
    riterator = iter(indexlist(entrytext, rchar))

    returnlist = []
    for a_temp in range(len(llist)):

        returnlist.append(entrytext[next(literator)
                                    +len(lchar): next(riterator)])
    return returnlist

def embedded_extract(text,
                     lchar=LEFTNOTE,
                     rchar=RIGHTNOTE,
                     eliminate=True):

    """extracts the first level of textblock starting with lchar
    ending with rchar. Optionally eliminates extracted blocks from text.
    """


    both = lchar+rchar
    count = 0
    maxcount = 0
    updown = 0
    returnlist = []
    leftplace = 0


    if text.count(lchar) != text.count(rchar):
        return [], text, 0

    for b_temp, a_temp in enumerate(text):

        if a_temp in both:
            updown = {lchar: 1, rchar: -1}[a_temp]
            count += updown
            if count > maxcount:
                maxcount = count
            if updown == 1 and count == 1:
                leftplace = b_temp
            if updown == -1 and count == 0:
                returnlist.append(text[leftplace: b_temp+1])
        updown = 0
    if eliminate:
        for a_temp in returnlist:
            text = text.replace(a_temp, EMPTYCHAR)
    return returnlist, text, maxcount
##while True:
##
##    print(embedded_extract(input('?')))
