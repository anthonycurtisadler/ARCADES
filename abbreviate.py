"""Module for keeping track of abbreviations that are applied to notes
pylint rated 9.63/10
"""


from displaylist import DisplayList
from globalconstants import YESTERMS, ADDTERMS, DELETETERMS, CLEARTERMS, \
     LEFTNOTE, RIGHTNOTE, LEFTCURLY, RIGHTCURLY, BLANK, COLON, QUESTIONMARK, UNDERLINE,\
     EMPTYCHAR, SHOWTERMS, QUITTERMS, EQUAL,EOL, TILDA

class Abbreviate:


    """ Holds and applies preset transformations
    Do applies a transformation, undo undoes it.
    This is needed in order to allow arrow brackets
    and curly brackets in the note text...
    These should be preceded with a single underscore
    """

    def __init__(self,
                 newdefaults=None,
                 use_presets=True,
                 displayobject=None,
                 headings=None,
                 terms=None):
        #displayobject must be passed in

        self.displayobject = displayobject
        if newdefaults is None:
            newdefaults = {}

        if use_presets:
            self.default_debreviations = {LEFTNOTE:'/060/',
                                          RIGHTNOTE:'/062/',
                                          LEFTCURLY:'/123/',
                                          RIGHTCURLY:'/125/'}
        else:
            self.default_debreviations = {}

        self.default_debreviations.update(newdefaults)
        self.default_abbreviations = {value:key for  key,
                                      value in self.default_debreviations.items()}

        if not headings:
            from plainenglish import DefaultConsoles
            self.headings = DefaultConsoles()
        else:
            self.headings = headings
        if not terms:
            from plainenglish import ADDTERMS,DELETETERMS,\
                 SHOWTERMS,QUITTERMS,CLEARTERMS
            self.ADDTERMS = ADDTERMS
            self.DELETETERMS = DELETETERMS
            self.SHOWTERMS = SHOWTERMS
            self.QUITTERMS = QUITTERMS
            self.CLEARTERMS = CLEARTERMS
        else:
            self.ADDTERMS = terms[0]
            self.DELETETERMS = terms[1]
            self.SHOWTERMS = terms[2]
            self.QUITTERMS = terms[3]
            self.CLEARTERMS = terms[4]

    def change_language(self,headings=None,terms=None):

        if not headings:
            from plainenglish import DefaultConsoles
            self.headings = DefaultConsoles()
        else:
            self.headings = headings
        self.ADDTERMS = terms[0]
        self.DELETETERMS = terms[1]
        self.SHOWTERMS = terms[2]
        self.QUITTERMS = terms[3]
        self.CLEARTERMS = terms[4]
        
           
    def do(self,
           text,
           lchar=UNDERLINE,
           rchar=EMPTYCHAR):

        """ to apply 'debreviations'=shorter to longer.
        These must be preceded with _.
        This is mainly done in order to circumvent
        reserved characters <>{} in entering text.
        """

        keys = reversed(sorted(self.default_debreviations.keys()))
        for key in keys:
            value = self.default_debreviations[key]
            text = text.replace(lchar+key+rchar, value)

        return text

    def undo(self,
             text,
             lchar=EMPTYCHAR,
             rchar=EMPTYCHAR):

        """apply 'abbreviations' ---
        The reverse of debreviations.
        """

        for key, value in self.default_abbreviations.items():
            text = text.replace(lchar+key+rchar, value)

        return text

    def add(self,
            from_this,
            to_this,
            no_query=False):

        """add a conversion formula
        to the abbreviation/debreviation dictionary
        """

        if (from_this not in self.default_debreviations
                and to_this not in self.default_abbreviations
                and (no_query or input(self.headings.ADD
                                       +from_this
                                       +BLANK+COLON+BLANK
                                       +to_this+QUESTIONMARK) in YESTERMS+[EMPTYCHAR])):
            self.default_debreviations[from_this] = to_this
            self.default_abbreviations[to_this] = from_this

    def delete(self,
               from_this,
               to_this):

        """delete a conversion formulat from the
        abbreviation/debreviation dictionary"""

        if (from_this in self.default_debreviations
                and to_this in self.default_abbreviations
                and from_this not in [LEFTCURLY, RIGHTCURLY, LEFTNOTE, RIGHTNOTE] and
                input('Delete|'+from_this+BLANK+COLON+BLANK+to_this) in YESTERMS):

            self.displayobject.noteprint((self.headings.DELETING, EMPTYCHAR))
            del self.default_debreviations[from_this]
            del self.default_abbreviations[to_this]

    def show(self,returntext=False):

        """show all the stored debreviations"""
        if not returntext:
            show_debreviations = DisplayList(displayobject=self.displayobject)
            spacer = BLANK
        else:
            show_debreviations = []
            spacer = EMPTYCHAR
        for counter, key in enumerate(sorted(self.default_debreviations)):
            if not returntext:
                countermark = str(counter+1)
            else:
                countermark = EMPTYCHAR
            deb_temp = self.default_debreviations[key]
            if returntext:
                deb_temp = deb_temp.replace(BLANK,TILDA)                                        
            show_debreviations.append(countermark+spacer+key+EQUAL+deb_temp)
        if returntext:
            return EOL.join(show_debreviations)
        show_debreviations.show()

    def load(self,
             entrylist):

        """load a list in... LOAD is standard method name for analogous classes... """

        for l_temp in entrylist:
            from_to = l_temp.split(EQUAL)
            from_this = from_to[0].replace(UNDERLINE, EMPTYCHAR)
            to_this = from_to[1].replace(UNDERLINE,BLANK).replace(TILDA,BLANK)
            self.add(from_this.strip(), to_this.strip(), no_query=True)
        self.show()

    def console(self):

        """ opens up console for adding and deleting """

        go_on = True
        while go_on:
            console = DisplayList([self.headings.ADD_MENU,
                                   self.headings.DELETE_MENU,
                                   self.headings.SHOW_MENU,
                                   self.headings.CLEAR_MENU,
                                   self.headings.QUIT_MENU],
                                   displayobject=self.displayobject)
            i = input()
            if i in self.ADDTERMS:

                self.add(input(self.headings.FROM_THIS), input(self.headings.TO_THIS))
            if i in self.DELETETERMS:

                while True:
                    self.show()
                    to_delete = input (self.headings.DELETE)
                    if to_delete == EMPTYCHAR:
                        break
                    if to_delete.isnumeric() and int(to_delete) > 0 and int(to_delete) < len(self.default_debreviations)+1:
                        from_temp = sorted(self.default_debreviations)[int(to_delete)-1]
                        to_temp = self.default_debreviations[from_temp]
                        self.delete(from_temp,to_temp)
            if i in self.SHOWTERMS:
                self.show()
            if i in self.CLEARTERMS:
                if input(self.headings.ARE_YOU_SURE) in YESTERMS:
                    self.default_debreviations = {}
                    self.default_abbreviations = {}                 
            if i in self.QUITTERMS:
                go_on = False
