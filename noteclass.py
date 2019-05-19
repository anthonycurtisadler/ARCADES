"""Module for the basic note class
pylint rated at 10.0/10
"""

import datetime
from globalconstants import EMPTYCHAR, EOL, UNDERLINE

class Note:


    """ The basic Note object, which consists
    in a set of keys, text, and a dictionary of metadata
     Basic metadata is the width of the note,
     a list of dates when the note was made and edited,
     and the user who created the note. """

    def __init__(self,
                 keyset=None,
                 text=EMPTYCHAR,
                 meta=None):

        if keyset is None:
            keyset = set()
        self.keyset = keyset
        self.text = text
        if meta is None:
            self.meta = {'size':60,
                         'date':[str(datetime.datetime.now())],
                         'user':'user'}
        else:
            self.meta = meta


    def __add__(self,
                other):
        """operator overloading for adding together two notes."""

        tempkeys = self.keyset.union(other.keyset)
        maxsize = max([self.meta['size'],
                       other.meta['size']])
        temptext = self.text+other.text
        tempmeta = {'size':maxsize,
                    'date':[str(datetime.datetime.now())],
                    'user':'user'}

        return Note(tempkeys,
                    temptext,
                    tempmeta)

    def add_keys(self,
                 keyset):

        """adds a set of keys to the note"""

        return Note(self.keyset.union(keyset), self.text, self.meta)

##    def delete_key (self, key):
##        """deletes a key from the note"""
##        return Note(self.keyset-key, self.text, self.meta)


    def add_text(self,
                 text,
                 inbetween=EMPTYCHAR):

        """adds text to note"""

        return Note(self.keyset,
                    self.text+inbetween+text,
                    self.meta)


    def change_size(self,
                    newsize):

        """changes the size of the note"""

        tempdict = self.meta
        tempdict['size'] = newsize

        return Note(self.keyset,
                    self.text,
                    tempdict)

    def change_user(self,
                    newuser):

        """changes the user of the note"""

        tempdict = self.meta
        tempdict['user'] = newuser

        return Note(self.keyset,
                    self.text,
                    tempdict)

    def delete_keys(self,
                    keyset):

        """deletes a set of keys"""

        tempkeys = self.keyset-keyset

        return Note(tempkeys,
                    self.text,
                    self.meta)

    def replace_in_text(self,
                        phrase_a,
                        phrase_b,
                        ask=False):

        """Replaces phrase_a in the text with phrase_b.
        ask is True to query if change should be made.
        """

        if phrase_a != EMPTYCHAR:
            if not ask or input('Replace?')[0].lower() == 'y':
                return Note(self.keyset,
                            self.text.replace(phrase_a, phrase_b),
                            self.meta)

        return Note(self.keyset,
                    self.text,
                    self.meta)
    def date(self,
             most_recent=False,
             short=False,
             convert=True):

        """Retrieves either the most recent or
        the first date of the note
        """
        dates = self.meta['date']
        if not isinstance(dates,list) :
            dates = [dates]
        
        if not most_recent:
            date = dates[0]
        else:
            date = dates[-1]
        if not isinstance(date,str):
            date = str(date)

        date = date.strip()
        date = date.replace("'",'')
        yearmonthday = date.split(' ')[0].split('-')
        if not short:
            hourminutesecond = date.split(' ')[1].split('.')[0].split(':')
        else:
            if not convert:
                date = date.split(' ')[0]
        if convert:
            if short:
                date = datetime.datetime(int(yearmonthday[0]),
                                         int(yearmonthday[1]),
                                         int(yearmonthday[2]))
            else:
                date = datetime.datetime(int(yearmonthday[0]),
                                         int(yearmonthday[1]),
                                         int(yearmonthday[2]),
                                         int(hourminutesecond[0]),
                                         int(hourminutesecond[1]),
                                         int(hourminutesecond[2]))
                                             
                                    
        return date

    def alldates(self):
        
    
        dates = self.meta['date']
        if isinstance(dates,(tuple,list,set)):
            return set(dates)
        elif isinstance(dates,str):
            return set({dates})
        return set({str(dates)})

    
        return set(dates)
    

            
