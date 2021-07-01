#Class for implementing the "fetch" command


from globalconstants import LEFTPAREN, RIGHTPAREN, COMMA, DASH,\
                            SLASH, TILDA, POUND, BLANK, \
                            ANDSIGN, VERTLINE

from indexclass import Index
from indexutilities import index_expand
import simple_parser as parser


class NB:

    """For testing with interfacing to the actual notebook
    """
    

    def __init__(self):
        pass
    
    def find_within(self,
                    term_from,
                    term_to,
                    orequal=False):
        return {str(x) for x in range(int(term_from),int(term_to+1))}
    

class Fetcher:

    """The fetcher is used to implement the "fetch" command,
    which returns the indexes for notes belonging to general classifications, such
    as a given project, marked noted, unmarked note, etc.

    It is analogous to the "search" command, also making use of the parcer module.

    Logical primatives include: ~ () & |
    & = Intersection
    | = Union

    The ~ is equivalent to NOT. Note, however, that it can be applied only to individual elements, and
    not to a paranthetical construction.

    Atomic elements:
        (1) one or more ranges of notes separated by parentheses.
        (2) MARKED, UNMARKED, POS(ITIVE), NEG(ITIVE), ALL, FLIPBOOK (or FB)
        (3) The name of a project.
        (4) The name of a variable.
        

    
    """

    def __init__(self,
                 notebook=None,
                 default_dictionary=None,
                 variables=None):

        self.universe = {}
        if notebook:
            self.notebook = notebook
        else:
            #For testing 
            self.notebook = NB()

        if default_dictionary:
            self.default_dictionary = default_dictionary
        
        else:
            self.default_dictionary = {}
        if variables:
            self.variables = variables

        

    
    def get_range(self,
                  entryterm,
                  sort=True,
                  orequal=True,
                  complete=False,
                  indexes=False):

        """gets a range of indexes from a string of index ranges
        IR1, IR2, IR3... Each indexrange is formated INDEXFROM-INDEXTO
        or -INDEXFROM/-INDEXTO. orequal True is less than equal to
        upper range. if complete true find top level indexes between
        top-level form of entered indexes. Sort is true to sort output.
        Many is true if term includes a number of ranges
        """
        term = entryterm


        # For more than one range of indexes
        returnrange = []
        bigterm = term
        for term in bigterm.split(COMMA):
            if term.strip():
                term = term.strip()
                if (term[0]!=DASH and (SLASH in term or DASH in term)) \
                   or (term[0]==DASH and (SLASH in term[1:] or DASH in term[1:])):

                    if DASH + DASH in term:
                        term = term.replace(DASH+DASH,
                                            SLASH+DASH)
                    if SLASH not in term:
                        if term[0] != DASH:
                            term = term.replace(DASH,
                                                SLASH)
                        else:
                            term = term[0] + term[1:].replace(DASH,SLASH)

                    if POUND not in term:
                        termfrom = Index(index_expand(term.split(SLASH)[0]))
                        termto = Index(index_expand(term.split(SLASH)[1]))

                    else:
                        termfrom = term.split(SLASH)[0]
                        termto = term.split(SLASH)[1]
        
                        
                    returnrange += [str(x) for x in self.notebook.find_within(termfrom,
                                                                termto,
                                                                orequal=orequal)]                 

                else:
                    if indexes:
                        returnrange += [Index(term)]
                    else:
                        returnrange += [str(term)]
            if complete and returnrange == []:
                if indexes:
                    returnrange = [Index(a_temp) for a_temp
                                   in range(int(termfrom), int(termto)+1)]
                else:
                    returnrange = [str(a_temp) for a_temp in range(int(termfrom),
                                                              int(termto)+1)]
                if sort:


                    return sorted(returnrange,
                              key=lambda x_temp: Index(str(x_temp)))

                return set(returnrange)


        if sort:


            return set(sorted(returnrange,
                              key=lambda x_temp: Index(str(x_temp))))

        return set(returnrange)


    def get_search_terms (self,
                          query):

        """Extracts atomic elements from query"""

        for x in [LEFTPAREN,
                  RIGHTPAREN,
                  ANDSIGN,
                  VERTLINE]:
            
            query = query.replace(x,BLANK)

        while COMMA+BLANK in query:
            query = query.replace(COMMA+BLANK,BLANK)
        
        while BLANK+BLANK in query:
            query = query.replace(BLANK+BLANK,BLANK)

        return query.split(BLANK)

    def evaluate_term (self,
                       term):

        """Returns a set of indexes for a given atomic element"""

        
        def is_index_range (y):
            #tests if a term is an index range

            for x in ['0','1','2','3','4','5','6','7','8','9','-',',','/','.','^','~']:
                y=y.replace(x,'')
            return y==''

        
        negative = False
        variable = False

        if term and term[0] == '~':
            negative = True
            term = term[1:]
        if not term:
            return set()

        if is_index_range(term):
            returnset = self.get_range(term)

        elif term == 'MARKED':
            returnset = set(self.default_dictionary['marked'])
        elif term == 'UNMARKED':
            returnset = {str(x) for x in self.default_dictionary['indexlist'].list
                    if not str(x) in self.default_dictionary['marked']}
        elif term == 'ALL':
            returnset = {str(x) for x in self.default_dictionary['indexlist'].list}
        elif term in ['POSITIVE','POS']:
            returnset = {str(x) for x in self.default_dictionary['indexlist'].list if x>=Index(0)}
        elif term in ['NEGATIVE','NEG']:
            returnset = {str(x) for x in self.default_dictionary['indexlist'].list if x<Index(0)}
        elif term in ['FLIPBOOK','FB']:
            returnset = {str(x) for x in self.default_dictionary['flipbook']}
        elif term in self.variables:
            #For a variable
            returnset = {str(x).strip() for x  in self.variables[term].split(',')}


        elif term in self.default_dictionary['projects'].get_all_projects():
            #For a project 
            returnset = {str(x) for x
                    in self.default_dictionary['projects'].get_all_indexes(project=term)}
        
        if not negative:
            return returnset
        else:
            return {str(x) for x in self.default_dictionary['indexlist'].list if not str(x) in returnset}
        


    def populate_universe (self,
                           all_terms):

        """Populates the "universe" with values corresponding to the
        individual terms"""

        for term in set(all_terms):
            self.universe[term] = self.evaluate_term(term)

    def run_search (self,
                    query):

        """Implements the fetch"""

        terms = self.get_search_terms(query)
        

        parsed_query = parser.parse(query)

##        if isinstance(parsed_query, str):
##            parsed_query = [parsed_query]
        self.populate_universe (terms)
        
        return [x for x in parser.interpret (parsed_query,
                                             universe=self.universe)]

    

    

    
            
        

    

    
