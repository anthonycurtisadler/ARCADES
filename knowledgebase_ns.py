"""Module containing knowledgebase
pylint rated 8.62/10
Pylint seems to think variables should be constants,
and objects to definitions outside outer scope of class
"""

from globalconstants import KNOWLEDGEITERATIONS,\
     QUESTIONMARK, SLASH, TILDA, UNDERLINE, EQUAL, EOL, BLANK, \
     SHOWTERMS, QUITTERMS, CLEARTERMS, LEARNTERMS, UNLEARNTERMS
from displaylist import DisplayList

class KnowledgeBase():

    """ A very simple knowledgebase designed to store and
    draw inferences from species-genus relations
    """

    def __init__(self,
                 displayobject=None,
                 headings=None,
                 terms=None):

        self.knowledge_dict = {}
        self.displayobject = displayobject
        if not headings:
            from plainenglish import DefaultConsoles
            self.headings = DefaultConsoles()
        else:
            self.headings = headings
        from plainenglish import ADDTERMS,DELETETERMS,\
                 SHOWTERMS,QUITTERMS,CLEARTERMS, LEARNTERMS, UNLEARNTERMS,\
                 YESTERMS, NOTERMS
        if not terms:
            
            self.ADDTERMS = ADDTERMS
            self.DELETETERMS = DELETETERMS
            self.SHOWTERMS = SHOWTERMS
            self.QUITTERMS = QUITTERMS
            self.CLEARTERMS = CLEARTERMS
            self.LEARNTERMS = LEARNTERMS
            self.UNLEARNTERMS = UNLEARNTERMS
            self.YESTERMS = YESTERMS
            self.NOTERMS = NOTERMS
        else:
            if len(terms)<8: terms = (ADDTERMS,
                                      DELETETERMS,
                                      SHOWTERMS,
                                      QUITTERMS,
                                      CLEARTERMS,
                                      LEARNTERMS,
                                      UNLEARNTERMS,
                                      YESTERMS,
                                      NOTERMS)
            self.ADDTERMS = terms[0]
            self.DELETETERMS = terms[1]
            self.SHOWTERMS = terms[2]
            self.QUITTERMS = terms[3]
            self.CLEARTERMS = terms[4]
            self.LEARNTERMS = terms[5]
            self.UNLEARNTERMS = terms[6]
            self.YESTERMS = terms[7]
            self.NOTERMS = terms[8]


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
        self.LEARNTERMS = terms[5]
        self.UNLEARNTERMS = terms[6]


    def learn(self, species, genus):

        """Teaches knowledge base that species is genus"""


        if genus in self.knowledge_dict:
            temp = self.knowledge_dict[genus]
            temp.add(species)
            self.knowledge_dict[genus] = temp

        else:
            self.knowledge_dict[genus] = {species}

        if species not in self.knowledge_dict:
            self.knowledge_dict[species] = set()

    def learned(self, item):

        """Tests knowledge of knowledge base"""

        if item not in self.knowledge_dict:
            return False
        return True

    def species(self, item):

        """Tests to see whether item is a species,
        i.e. at lower leve.
        """

        if item not in self.knowledge_dict:
            return False
        if self.knowledge_dict[item] == set():
            return True
        return False

    def genus(self, item):

        """Tests to see if an item is a genus,
        i.e. not at lower level
        """

        if item not in self.knowledge_dict:
            return False
        if self.knowledge_dict[item] == set():
            return False
        return True

    def unlearn(self, species, genus):

        """unlearns that species is genus"""

        print('unlearning')
        if genus in self.knowledge_dict:
            temp = self.knowledge_dict[genus]
            temp.discard(species)
            self.knowledge_dict[genus] = temp

    def load(self, entrylist):

        """Loads in a list of facts into the knowledgebase"""

        obj = self.learn
        for line in entrylist:
            line = line.lstrip(UNDERLINE).replace(UNDERLINE,BLANK)
            if line[0] == TILDA:
                obj = self.unlearn
            if SLASH in line:
                tag, definitions = line.split(SLASH)[0], line.split(SLASH)[1]
                if EQUAL in definitions:
                    definitions = [tag]+definitions.split(EQUAL)
                else:
                    definitions = [tag]+[definitions]

            else:
                definitions = line.split(EQUAL)


            if len(definitions) > 1:
                for r_temp in range(0,
                                    len(definitions)-1):
                    obj(definitions[r_temp],
                        definitions[r_temp+1])


    def reveal(self, genus):

        """Reveals knowledge"""

        if genus not in self.knowledge_dict:
            return set()
        found_higher = {genus}
        found_lowest = set()

        not_done = True
        counter = 0
        while not_done and counter <= KNOWLEDGEITERATIONS:
            # Second condition to prevent infinite loops

            counter += 1
            for g_temp in set(found_higher):
                found_higher.discard(g_temp)
                if g_temp in self.knowledge_dict:
                    found_higher.update(self.knowledge_dict[g_temp])
                    found_lowest.update(self.knowledge_dict[g_temp])
                else:
                    found_lowest.add(g_temp)

            if not found_higher:
                not_done = False
        return found_lowest


    def bore(self, listobject=None):

        """recite all knowledge"""
        listobject = DisplayList(displayobject=self.displayobject)

        if listobject is None:
            listobject = []

        for k in self.knowledge_dict:
            l_temp = self.knowledge_dict[k]
            if l_temp == set():
                listobject.append(self.headings.I_KNOW
                                  +k+self.headings.IS_WHAT_IT_IS)
            else:
                for m_temp in l_temp:
                    listobject.append(self.headings.I_KNOW
                                      +m_temp+self.headings.IS_AN+k)
        if isinstance(listobject,list):
            print(listobject)
        else:
            listobject.show()

    def record(self):

        listobject = []

        for k in self.knowledge_dict:
            l_temp = self.knowledge_dict[k]
            if l_temp == set():
                pass
            else:
                for m_temp in l_temp:
                    listobject.append((m_temp+EQUAL+k).replace(BLANK,UNDERLINE))
                    
        return EOL.join(listobject)

    def console(self):

        """ opens up console for adding and deleting """

        go_on = True
        while go_on:
            console = DisplayList([self.headings.LEARN_MENU,
                                   self.headings.UNLEARN_MENU,
                                   self.headings.SHOW_MENU,
                                   self.headings.CLEAR_MENU,
                                   self.headings.QUIT_MENU],
                                   displayobject=self.displayobject)
            i = input()
            if i in self.LEARNTERMS:

                self.learn(input(self.headings.LEARN_THAT_THIS), input(self.headings.IS_WHAT))
            if i in self.UNLEARNTERMS:

                self.unlearn(input(self.headings.UNLEARN_THAT_THIS), input(self.headings.IS_WHAT))
            if i in self.SHOWTERMS:
                self.bore()
            if i in self.CLEARTERMS:
                if input(self.headings.ARE_YOU_SURE) in self.YESTERMS:
                 self.knowledge_dict = {}
                                   
            if i in self.QUITTERMS:
                go_on = False


    


if __name__ == "__main__":

    knower = KnowledgeBase()
    keep_going = True
    while keep_going:

        say_what = input('Teach me!').lower()
        if (say_what.startswith('what is a ')
                or say_what.startswith('who is a ')):
            genus = say_what.split('is a ')[1].strip().lower().replace(QUESTIONMARK, EMPTYCHAR)
            print('Maybe I know this!')
            answers = knower.reveal(genus)
            if not answers:
                print("I'm stumped!")
            else:
                for a in answers:
                    print(a, ' is a '+genus)


        elif 'is a' in say_what:
            species = say_what.split('is a')[0].strip().lower()
            genus = say_what.split('is a')[1].strip().lower()
            knower.learn(species, genus)
            print('I learned that '
                  +species+' is a '+genus)

        elif say_what in ['bored now',
                          'stop',
                          'had enought',
                          'quit']:

            keep_going = False

            print('See you later!')
            print('But first let me bore you with everything I know!')
            knower.bore()
