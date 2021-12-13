from globalconstants import LEFTPAREN, RIGHTPAREN, ANDSIGN, VERTLINE, PERIOD, DASH,\
                       BLANK, LEFTPAREN, RIGHTPAREN,LEFTCURLY, RIGHTCURLY, COMMA, \
                       TILDA, EMPTYCHAR, DOLLAR, STAR, CARET, QUESTIONMARK, LEFTNOTE, \
                       RIGHTNOTE, POUND, SLASH, PLUS, PERCENTAGE, ATSIGN

from truth_table import TruthTable
import simple_parser as parser
import nformat
import string 
from substitutions import Substitutions
from display import Display
from indexclass import Index
import extract
from generalutilities import concatenate 


display = Display()

def new_search(query,
               onlyterms=False,
               defaultdictionaryobject = None,
               db_cursor=None,
               self=None):

    """Search function for performing complex searches over the notebase.
    Searches are formitted as follows:
        | : or
        & : and
        ~ : not
        * : wildcard
        () parantheses can be nested
        term   word in text
        <TERM> keyword
        ALLCAPS non-case sensitive
        #TERM tag
        ##TERM class defined through knowledge base

        RETURNS tuple (query, result, foundterms)

    """
            
       
    def elim_redundant_parens (x):
            level = 0
            x = x.strip()
            first_paren = False 
            
            for count, ch in enumerate(x):
                if ch == '(':
                    if level == 0 and count == 0:
                        first_paren = True
                    level+=1
                if ch == ')':
                    if count < len(x)-1:
                        level -= 1
                    else:
                        if first_paren:
                            return (x[1:-1])
                        return x
                    if level == 0:
                        return x
            return x

    def reduce_gaps (x):

        x = x.replace('( ','(').replace(' )',')')
        
        while '  ' in x:
            x = x.replace('  ',' ')
        return x 
                    
    
    def insert_perc (phrase):


        """Inserst percentages in spaces between keywords"""

        return phrase
##            reserved_chars = '()&~|<> '                
##            phrase = list(phrase)
##            for pos, ch in enumerate (range(1,len(phrase)-1)):
##                if phrase[pos] == ' ' and phrase[pos-1] not in reserved_chars and phrase[pos+1] not in reserved_chars:
##                    phrase[pos] = '%'
##            return ''.join(phrase)

    def stripped (term):
        unmodified = term

        for a_temp in ['##','<','>','#','~']:
            term = term.replace(a_temp,'')
        
        return term, unmodified.split(term)[0], unmodified.split(term)[1]
        

    def get_terms_from_query (query):


        query = nformat.reduce_blanks(query)

        for a_temp in [LEFTPAREN, RIGHTPAREN, ANDSIGN, VERTLINE]:
            query = query.replace(a_temp, '[ELIM]')

        
        termlist = [x.strip() for x in sorted(set(query.strip().split('[ELIM]'))) if x]

        return termlist


    ##The following three functions are used for implementing the equivalences in the search routine.
    ##An important lesson that I learned, alas too late, is analyse an object into its simplest elements before
    ##attempting complex transformations on it. Which is to say, I should not have tried, as I do here, to work
    ##directly with a search query in text form, but should have parsed it.
    ##In any case, though, in order to avoid the overwrite errors that occur when working with a string, I took the
    ##perhaps needless elaborate step, of converting substituting each of the search terms with a unique ten digit numerical key.'
    ##The implemenation proved very complicated, however...
    ##
    ##The encoding is achieved through the Substitutions object.

    def simplify_equivalences (query):

        """For simple equivalences from one single term to another"""
        get_terms = lambda x:{y for y in x.replace('(',' ').replace(')',' ').replace('&',' ').replace('|',' ').split(' ') if y}
        
        def well_formed(x):

            x = x.replace('&',' & ')
            x = x.replace('|',' | ')
            

            while '  ' in x:
                x = x.replace('  ',' ')
            x = x.replace('( ','(')
            x = x.replace(' )',')')
            x = x.replace(' (','(')
            x = x.replace(') ',')')

            x = x.replace('&',' & ')
            x = x.replace('|',' | ')
            while '  ' in x:
                x = x.replace('  ',' ')
            
            return x


        all_terms = get_terms(well_formed(query))

        get_first_free = lambda x:x.replace('[/','').replace('/]','')[0:min(len(x),10)]
        
        for count, x in enumerate(all_terms):
            query = query.replace(x,'['+get_first_free(x)+']')
        return query
        


    def substitute_equivalences (query,done_terms=None,working_terms=None):

        """In addition to simple equivalences, ARCADES allows a term to be substituted for search phrase.

        For example: frog = (green & amphibian)
        This functions performs substitutions on the query phrase.
            e.g frog => (frog | (green&amphibian))
        If more than one equivalent term is defined, they are applied accordingly.

        substitution is applied recursively, but done_terms is used to keep track of substitutions so as to avoid
        circular substititions leading to recursion error"""

        get_terms = lambda x:{y.strip() for y in x.replace('(','[ELIM]').replace(')','[ELIM]').replace('&','[ELIM]').replace('|','[ELIM]').split('[ELIM]') if y.strip()}

        mark_dict = {True: ' & ',
                     False: ' | '}

            

        def bracket_all (phrase,left_part,right_part):

            for term in get_terms_from_query (phrase):
                
                phrase = phrase.replace(term,left_part+term+right_part)
                
            return phrase 
                
        def get (x,query,working_terms):
            
           
            negating = query.get_negated(x)

            
            left_part, right_part = query.get_brackets(x)
   
            
            cancel_negation = False
            equivalent_term = defaultdictionaryobject['equivalences'].fetch_bracketed(query.unencode(x))
             #To fetch logical phrases rather than single terms.

            replace_term_bracketed = ''
            replace_term_single = ''
            if equivalent_term:

                    equivalent_term = insert_perc (equivalent_term)
                    if negating:
                        equivalent_term = equivalent_term.replace('&','/&/').replace('|','&').replace('/&/','|')

                        
                    new_terms = ['~'*negating+left_part+t+right_part.replace('~~','') for t in get_terms_from_query(equivalent_term)]
                    
                    working_terms.update(new_terms)

                    new_terms = [t for t in new_terms]


                    bracketed = bracket_all(equivalent_term,'~'*negating+left_part,right_part).replace('~~','')
##                        partial_bracketed = query.partial(bracketed)

                    

                    replace_term_bracketed = negating*'~'+left_part+query.unencode(x)+right_part+ mark_dict[negating] + bracketed

                                    
            terms = [tt for tt in defaultdictionaryobject['equivalences'].fetch(query.unencode(x).replace('[/','').replace('/]','')) ]#if tt  != query.unencode(x).replace('[/','').replace('/]','')
                #For the single terms
            
                
                
            
#                       
            #To keep terms with more than one word from being treated as  textwords
            if terms:

                    replace_term_single = insert_perc(mark_dict[negating].join(['~'*negating+left_part+t+right_part for t in terms ]))
                    done_terms.update([(negating*'~'+left_part+t+right_part) for t in terms if not t==query.unencode(x)])

            if len(get_terms(replace_term_single)) < 2 and replace_term_bracketed:
                replace_term_single = ''
            
            if replace_term_bracketed or replace_term_single:
                inserting_mark = ''
                if replace_term_bracketed and replace_term_single:
                    inserting_mark = mark_dict[negating]

                
                final_term = (replace_term_bracketed + ' ' + inserting_mark + ' ' +replace_term_single).replace('~~','')
                if len(get_terms_from_query(final_term))>1:
                    final_term = ' ( '+final_term+' ) '

               
                query.substitute(query.reverse().replace('~'*negating+left_part+query.unencode(x)+right_part,final_term))

             
                

                

            return query, working_terms
                
        #Main routine in function#

        if done_terms is None:
            done_terms = set()
        if working_terms is None:
            working_terms = set()


        if not working_terms:
            

            terms = get_terms (query.query)


            for term in terms:
                
                
                if not query.unencode(term,purging=False) in done_terms:
                    
                    query, working_terms = get(term,query,working_terms)
                done_terms.add(query.unencode(term,purging=False))
            
        else:
            for term in list(working_terms):
                if term not in done_terms:
                    query,working_terms = get(query.encode(term),query,working_terms)
                    done_terms.add(term)
                working_terms.remove(term)


        
        if working_terms:
            
            query, done_terms, working_terms = substitute_equivalences(query,done_terms,working_terms)

        return query, done_terms, working_terms 
    
    def substitute_complex_equivalences (query,done_terms=None,working_terms=None,initiating=True,iteration=0):

        

        def adjust_tilda (x):

            """Moves the tilda to the beginning"""

            
            tilda = '~' in x
            return tilda*'~'+x.replace('~','')
        
        def is_vapid (phrase):

            """Identifies a search phrases that have no logical meaning"""

            for x in ('!allnotes!','<','>','#','(',')','&','|',' ','[/','/]','~'):
                phrase = phrase.replace(x,'')

            return not phrase 

        def bracket_all (phrase,left_part,right_part):

            """Inserts left part and right part around every term in a phrase,
            though keeping the tilda on the outside left.
            """
            
            phrase = ' '+phrase+' '
            phrase = phrase.replace('(',' ( ').replace(')',' ) ')
            

            

            for term in get_terms_from_query (phrase):
                
                

                tilda = ''
                if '~' in term:
                    tilda = '~'
                term = term.replace('~','')

                
                phrase = phrase.replace(' '+tilda+term+' ', ' '+tilda+left_part+term+right_part+' ')


            return phrase.strip()
        
      
        def well_formed(x):

            x = x.replace('&',' & ')
            x = x.replace('|',' | ')
            

            while '  ' in x:
                x = x.replace('  ',' ')
            x = x.replace('(','( ')
            x = x.replace(')',' )')
            x = x.replace('(','( ')
            x = x.replace(')',' )')

            x = x.replace('&',' & ')
            x = x.replace('|',' | ')
            while '  ' in x:
                x = x.replace('  ',' ')
            
            return x

        unbrack = lambda x,y,z:({q[len(y):-len(z)] for q in x if q.startswith(y) and q.endswith(z)},{q for q in x if not (q.startswith(y) and q.endswith(z))})            
        get_terms = lambda x:{y for y in x.replace('(',' ').replace(')',' ').replace('&',' ').replace('|',' ').split(' ') if y}
        extract_tag = lambda x:unbrack(x,'<#','>')
        extract_key = lambda x:unbrack(x,'<','>')
        unparen = lambda x:{y.replace('%',' ') for y in x}
        
        def augment (phrase,lp,rp):

            """Surrounds phrase lp and rp, keeping the tilda on the far left.
            """

            phrase = ' ' + phrase + ' '

            for x in get_terms(phrase):
                tilda = ''
                if '~' in x:
                    tilda = '~'
                x = x.replace('~','')
            
                if lp not in x and rp not in x:
                    phrase = phrase.replace(' '+tilda+x+' ',' '+tilda+lp+x+rp+' ')

            return phrase.strip()
        

        # extract tags, keywords, texwords from query, since they will be evaluated separately.
        # A logical equivalence is only recognized in the same class

        if initiating:
            self.buffered_done_terms = set(done_terms)
            done_terms = set()
            

        if not working_terms and not initiating:

            return query, done_terms, working_terms   
        if working_terms is None:
            working_terms  = set()
        if done_terms is None:
            done_terms  = set()



        elif working_terms:
            query = list(working_terms)[0]

            working_terms = set()
        


        
##            all_terms = get_terms(query.query)
            #Gets all encoded terms 


        textwords_encoded = query.textwords
        keywords_encoded = query.keywords
        tags_encoded = query.tags
        textwords_unencoded = [query.unencode(x,keep_tilda=True) for x in textwords_encoded]
        keywords_unencoded = [query.unencode(x,keep_tilda=True) for x in keywords_encoded]
        tags_unencoded = [query.unencode(x,keep_tilda=True) for x in tags_encoded]
        



        temp_dict = {1: (tags_unencoded,'<#','>'),
                     2: (keywords_unencoded,'<','>'),
                     3: (textwords_unencoded,'[/','/]')}
        

        for count in range(1,4):

            term_set, left_part, right_part = temp_dict[count]

            complex_equivalent_terms = defaultdictionaryobject['equivalences'].fetch_reverse_bracketed(term_set)
                #Fetches the logical phrases containing only the given terms, if it exists.

            if complex_equivalent_terms:
            
                A = TruthTable (query.reverse(query.query.replace('||','&').replace('<','').replace('>','').replace('#',''),transform=iteration>2 and self.search_equiv_multiplied)
                                              .replace('[/', '').replace('/]',''),
                                log=self.truth_table_log,
                                subs=self.truth_table_subs) #CHANGED

                
                #forms a truth table from the encoded terms

                


           
            
            changed = False 
            for cet in complex_equivalent_terms:
                #Iterate over all the complex terms
                if cet  not in done_terms:
                    #Check if it has already been applied 
                    changed = True
                    
                    
                    bracketed_cet = bracket_all(cet,left_part,right_part)
                   
                    encoded_cet = query.partial(bracketed_cet,delete_tildas=True)

                    
                    
                    
                    additional_phrases = [augment(insert_perc(well_formed(x)),left_part,right_part) for x in  complex_equivalent_terms[cet]]
                  
                    replace_phrase = augment('( '+ ' | '.join(additional_phrases) + ' )',left_part,right_part)
                    encoded_replace_phrase = query.partial(replace_phrase,delete_tildas=False) # || > |
            

                    B = TruthTable (query.reverse(encoded_cet).replace('[/','').replace('/]',''),
                                log=self.truth_table_log,
                                subs=self.truth_table_subs)



                    if A>B: #Tests whether truth table A implies truth table B

                        



                        
                        
                        
##                            cet_aug = augment (well_formed(cet),left_part,right_part) 


                        temp_query = query.reverse()
                        
##                            for t in get_terms(well_formed(cet)+' '+' '.join(done_terms)):
##
##                                temp_query = temp_query.replace(adjust_tilda(left_part+t+right_part),'!allnotes!')
                            
    
                        
                        done_terms.add(cet)
                        non_query = temp_query

                        if is_vapid(non_query):
                            non_query = ''
                            temp_query =   '( ' + elim_redundant_parens(replace_phrase) + ' )'
##                                alternate_query =  '(' + elim_redundant_parens(alternative_replace_phrase)  + ')'
                        else:
                            temp_query= '( '+non_query + ' ) & ' + '( ' + elim_redundant_parens(replace_phrase) + ' )'
##                                alternate_query = '('+non_query + ') & ' + '(' + elim_redundant_parens(alternative_replace_phrase)  + ')'
                        query.substitute(temp_query,delete_tildas=True)
                        query.query = query.query.replace('| |','||')
                        query.query = query.query.replace('||','|')
                        
                        working_terms = {query}


                    
                        
                                       

        if working_terms:
           
            
##                query.delete_tildas()
            return substitute_complex_equivalences (query,done_terms=done_terms,working_terms=working_terms,initiating=False,iteration=iteration)
        query.query = query.query.replace('||','|')

        return query, done_terms.union(self.buffered_done_terms), working_terms                            

                                

    def eliminate_punctuation (x):
        #to eliminate punctuation marks 

        for ch in string.punctuation:
            x = x.replace(ch,'')
        return x 


    def modify(term,
               todo=EMPTYCHAR):
        """modifies term according to parameter todo"""

        if 'p' in todo:
            term = POUND+term
        if 'b' in todo:
            term = LEFTNOTE+term+RIGHTNOTE
        if 't' in todo:
            term = TILDA+term
        return term

    def is_regular(term):
        """used to test if the term is ready to be evaluated."""

        for a_temp in [PERIOD,
                       DASH,
                       BLANK,
                       LEFTPAREN,
                       RIGHTPAREN,
                       LEFTCURLY,
                       RIGHTCURLY,
                       COMMA,
                       'intersection',
                       'union',
                       'set',
                       "'"]:
            term = nformat.reduce_blanks(term).replace(a_temp, EMPTYCHAR)
        if term.isnumeric():
            return True

        

        return False

    def wildcards(term):

        """applies wildcards to the search term"""

        def find_terms(starts_with=EMPTYCHAR,
                       mid_terms=None,
                       ends_with=EMPTYCHAR,
                       searchedlist=None):

            if mid_terms is None:
                mid_terms = []
            if searchedlist is None:
                searchedlist = []
            returnlist = []
            for a_temp in searchedlist:
                yes_start = False
                yes_end = False
                yes_mid = False
                
                
                if a_temp.startswith(starts_with):
                    yes_start = True
                if a_temp.endswith(ends_with):
                    yes_end = True
                allin = True
                a_temp_copy = a_temp[1:-1]
                for mt_temp in mid_terms:
                    if mt_temp in a_temp_copy:
                        a_temp_copy = mt_temp.join(a_temp_copy.split(mt_temp)[1:])

                    elif mt_temp not in a_temp_copy:
                        allin = False
                if allin:
                    yes_mid = True

                    

                if (yes_start or starts_with=='@@@') \
                   and (yes_end or ends_with=='@@@') \
                   and (yes_mid or not mid_terms):
                            
                    returnlist.append(modify(a_temp, modifier))
                    

            return returnlist
        # beginning of wildcard main routine 

        if STAR not in term:

            return [term], (POUND in term or LEFTNOTE in term)

        brackets = False
        tilda = False
        pound = False
        caret = False
        
        qualifier = ''
        if term.count('"')==2:
            qualifier = '"'+term.split('"')[1]+'"'
            term = EMPTYCHAR.join([term.split('"')[0],term.split('"')[2]])
            

        if term[0] == TILDA:
            tilda = True
            term = term[1:]
        if term[0] == LEFTNOTE and RIGHTNOTE in term and term.count(RIGHTNOTE)==1:
            term = term[1:].replace(RIGHTNOTE,EMPTYCHAR)
            brackets = True

        if term[0] == POUND:
            term = term[1:]
            pound = True

        if term[0] == CARET:
            term = term[1:]
            caret = True

        mid_terms = term.split(STAR)

        if mid_terms[0] == EMPTYCHAR:
            mid_terms.pop(0)
            starts_with = '@@@'
        else:
            starts_with = mid_terms.pop(0)

        if mid_terms[-1] == EMPTYCHAR:
            mid_terms.pop(-1)
            ends_with = '@@@'
        else:
            ends_with = mid_terms.pop(-1)

        if brackets:
            modifier = 'b'+('t'*tilda)
            searched_list = list(self.keys())

        elif pound:
            modifier = 'p'+('t'*tilda)
            searched_list = list(self.tags())
        elif caret:
            modifier = 'c'+('t'*tilda)
            searched_list = list(self.tags())

        else:
            modifier = ('t'*tilda)
            searched_list = list(self.get_words())

##            nprint(starts_with,mid_terms,ends_with)

        return [x+qualifier for x in
                find_terms(starts_with,
                           mid_terms,
                           ends_with,
                           searched_list)], (brackets or pound)

    def add_keys(termlist):

        """expand term by adding possible tags to keys"""

        #THIS SHOULD BE RENAMED

        returnlist = []
        for term in termlist:
            if term in self.tag_dict_values():
                for tag in self.get_tags():
                    if term in self.get_keys_for_tag(tag):
                        returnlist.append(term+SLASH+tag)
        return returnlist

    def expand_term_list(termlist):

        """expand the list of search terms according to the type of query """
        def compound (func,entry_list,append=False):

                returnlist = []
                for x in entry_list:
                    if not append:
                        returnlist += func(x)
                    else:
                        returnlist.append(func(x))
                return returnlist 

        returnlist = []
        for term in termlist:

            qualifier = ''

            if term.count('"')==2:
                qualifier = '"'+term.split('"')[1]+'"'
                term = EMPTYCHAR.join([term.split('"')[0],term.split('"')[2]])
            brackets = False
            tilda = False
            

            if DOLLAR in term:
                returnlist.append(term)

            elif len(term)>1 and term[0] in [POUND, CARET] and compound(lambda x:x in self.tags(),defaultdictionaryobject['equivalences'].fetch(term[1:].replace(TILDA,EMPTYCHAR)),append=True):
                #    #TAG search for a tag
                for t in defaultdictionaryobject['equivalences'].fetch(term[1:].replace(TILDA,EMPTYCHAR)):
                    returnlist += [a_temp+SLASH+t
                                   for a_temp
                                   in self.get_keys_for_tag(t)]+[a_temp
                                                                for a_temp
                                                                in self.get_keys_for_tag(t)]


                # 1) adds keys+tags 2) adds keys without tags

                
            
            elif len(term)>2 and ((term[:2] == '##' and True in compound(defaultdictionaryobject['knower'].learned,defaultdictionaryobject['equivalences'].fetch(term[2:]),append=True)
                    and True in compound(defaultdictionaryobject['knower'].genus,defaultdictionaryobject['equivalences'].fetch(term[2:]),append=True))):
                definitionlist = compound(defaultdictionaryobject['knower'].reveal,defaultdictionaryobject['equivalences'].fetch(term[2:]))
                
                for d_temp in definitionlist:
                    if self.tag_dict_contains(d_temp):

                        returnlist += [a_temp+SLASH+d_temp
                                       for a_temp in self.get_keys_for_tag(d_temp)]\
                                       +[a_temp for a_temp in self.get_keys_for_tag(d_temp)]
            else:
                #if / is in the term, then separate it into word and suffixes
                if SLASH in term:
                    l_term = term.split(SLASH)[0]
                    r_term = term.split(SLASH)[1]

                else:
                    l_term = term
                    r_term = EMPTYCHAR


                if l_term == l_term.upper():
                    l_list = [l_term.lower(),
                              l_term.lower().capitalize(),
                              l_term.upper()]
                    # if the term is ALL CAPS, then expand to include
                    #lowercase, capitalized, and all-caps versions
                else:
                    l_list = [l_term]
                if COMMA in r_term:
                    r_list = r_term.split(COMMA)+[EMPTYCHAR]
                    # divide right term into all the different
                    # suffixes, and then assign to r list.

                else:
                    r_list = [r_term, EMPTYCHAR]
                    # Otherwise, r list is just the single
                    # suffix plus empty string.



                returnlist +=   concatenate(l_list, r_list)
                #generate all possible combinations
                # of l list and r list.

        

        middlelist, returnlist = list(returnlist), []

        for term in middlelist:
            if term[0] == DOLLAR:
                returnlist += [x+qualifier for x in defaultdictionaryobject['keymacros'].get_definition(term[1:])]
            if term[0] == PLUS:
                returnlist += [x+qualifier for x in defaultdictionaryobject['equivalences'].fetch(term[1:],override=True)]
                
            else:
                returnlist += [term+qualifier]


        
        

        
        return returnlist

    ##beginning of the main routine##

    returnstack = []
    foundterms = set()

    counter = 1
    done_terms = None

    
    dis_text = []
    query = Substitutions(query)
    query.substitute()

    #The following routine applies the equivalence substitutions until no more substitutions are possible
    
    is_code = lambda x:x.replace('{','').replace('}','').strip().isnumeric()
    
    while True:

        try:

            how_many_done = len([x for x in done_terms if is_code(x)])
        except:
            how_many_done = 0



        
        
        # Applies substitutions from a single term to a logical phrase      
        query, done_terms, dummy = substitute_equivalences(query,done_terms)
        dis_text.append(str(counter)+'/E ' + simplify_equivalences (reduce_gaps(query.reverse()).replace(' ','')))

        counter += 1


        

        # Applies substitutions from a logical phrase to a set of terms/logical phrases

        
        query, done_terms, dummy = substitute_complex_equivalences(query,done_terms,iteration=counter)
        dis_text.append(str(counter)+'/CE' + simplify_equivalences (reduce_gaps(query.reverse()).replace(' ','')))
        counter += 1







        
        if len([x for x in done_terms if is_code(x)]) <= how_many_done:
            break
        if counter == 10:
            break

    query = query.reverse()

    
    if self.convert_text_terms:
        for t in extract.extract(query,'[/','/]'):
            query = query.replace('[/'+t+'/]','[/'+t.replace(' ','$')+'/]')
            #For multi-word text search terms
        
        
    query = query.replace('( ','(').replace(' )',')').replace('[/','').replace('/]','')
    
    display.noteprint(('SEARCH CONSTITUTION','\n'.join(dis_text)))
    display.noteprint(('SEARCH TERM',query))

    if onlyterms:

        #extract all search terms from query and return the search terms 

        foundterms = set()
        for term in query.split(COMMA):

            t_temp = [wildcards(term)[0]]
                #analyse wildcards

            for tt_temp in t_temp:

                foundterms.update(expand_term_list(tt_temp))

        return foundterms
    

        
    if self.negative_results:

        searchset = self.apply_limit(self.indexes())
                # limit search set to applicable range
    else:
        searchset = self.apply_limit(self.find_within(indexfrom=Index(0),orequal=True))


    # add spaces around ( ) & |
    for a_temp in [LEFTPAREN, RIGHTPAREN, ANDSIGN, VERTLINE]:  
        query = query.replace(a_temp, '  '+a_temp+'  ')


    for a_temp in extract.extract(query, LEFTNOTE, RIGHTNOTE):
        # extract keywords, which are surrounded by arrow brackets.
        a_temp = LEFTNOTE+a_temp+RIGHTNOTE
        query = query.replace(a_temp, a_temp.replace(BLANK, PERCENTAGE))
          #spaces in keywords replaced with percentage sign


    query = nformat.reduce_blanks(query)
    querycopy = query

    for a_temp in [LEFTPAREN, RIGHTPAREN, ANDSIGN, VERTLINE]:
        querycopy = querycopy.replace(a_temp, EMPTYCHAR)

    
    termlist = [x for x in sorted(set(querycopy.strip().split(BLANK))) if x]



    termlist.reverse()

    def knowledge_from_word (word):
        originalword = word
        nonlocal query

        def rebracket (word,brackets=False):

            if brackets:
                return '<'+word+'>'
            else:
                return word

        if word.startswith('<') and word.endswith('>'):
            word = word[1:-1]
            is_bracketed = True
        else:
            is_bracketed = False

        node = relation = EMPTYCHAR

        if word.startswith(QUESTIONMARK):
            word = word[1:]
            if QUESTIONMARK  in word:
                node,relation = word.split(QUESTIONMARK)
            if relation.endswith(STAR):
                relation = relation[0:-1]
                relation_suffix = STAR
            else:
                relation_suffix = EMPTYCHAR
                

        ## to convert word based on general knowledge
        
        if  node and relation and defaultdictionaryobject['generalknowledge'].node_exists(node)\
           and defaultdictionaryobject['generalknowledge'].relation_exists(relation):
            newwords = [rebracket(x, is_bracketed)
                        for x in defaultdictionaryobject['generalknowledge'].text_interpret(DOLLAR
                                                                                      +DOLLAR+node
                                                                                      +COLON+relation+relation_suffix)[1].split('//')[0].split(',')]
            query = query.replace(originalword,
                                          '|'.join(newwords))
        else:
            newwords = [rebracket(word, is_bracketed)]
        return newwords
    
    def transform_list (wordlist):
        #to interpret knowldedge terms 

        returnlist = []
        for x in wordlist:
            if QUESTIONMARK in x:
                newwords = knowledge_from_word(x)
            else:
                newwords = [x]
            returnlist += newwords
        return returnlist 
            
        
    
    
    termlista = transform_list([a_temp for a_temp
                                in termlist
                                if LEFTNOTE in a_temp])
    
        #termlist a = list of keywords
    termlistb = transform_list([a_temp for a_temp
                                in termlist
                                if LEFTNOTE not in a_temp])

        #termlist b = list of words in text

    
    parsed_query = parser.parse(query) #Runs the parser on the query
                                       #To get a parsed object that
                                       #Can then be evaluated against the universe
    
    if isinstance(parsed_query,str):
        parsed_query = [parsed_query]
    upto = len(termlista)
    result_temp = set()

    universe = {}

    

    for counter, term in enumerate(termlista+termlistb):

        unmodified_term = term
        qualifier=''


        if not counter < upto:  #for the words
            temp_set = set()


            termcopy = term
            keyterm = False


            not_term = False
            if term[0] == TILDA:
                not_term = True
                term = term[1:]

            keyterm = False
            if term.startswith(DOLLAR) and term.endswith(DOLLAR):
                el_temp = [term]
                t_temp = [term],False
            else:
                t_temp = wildcards(term)

                el_temp = expand_term_list(t_temp[0])


        else:  #for the keywords
            temp_set = set()

            term = term.replace(PERCENTAGE, BLANK)
                #REPLACES BLANKS WITH PERCENTAGE SIGNS
            termcopy = term

            keyterm = True
            not_term = False
            if term[0] == TILDA:
                not_term = True
                term = term[1:]

            term = term.replace(LEFTNOTE,EMPTYCHAR).replace(RIGHTNOTE,EMPTYCHAR)


            if SLASH not in term.split('"')[0]:
                t_temp = wildcards(term)

                el_temp = expand_term_list(t_temp[0])
                el_copy = list(el_temp)
                for k_temp in el_copy:
                    for j_temp in self.keys():
                        if j_temp.startswith(k_temp+SLASH):
                            el_temp.append(j_temp)

            else:
                t_temp = [term], True
                el_temp = [term]

        if t_temp[1] or keyterm:   # if the term is a keyterm
            if not_term:
                temp_set = set(searchset)
                
            is_a_single_word = False        

            for word in el_temp:

                

                qualifier = ''

                if word.count('"')==2:
                    qualifier = '"'+word.split('"')[1]+'"'
                    word = EMPTYCHAR.join([word.split('"')[0],word.split('"')[2]])



                if ATSIGN in word:

                    #for the sequence keywords 
                            ft_temp = set()

                            if word[0] == LEFTBRACKET and word[-1] == RIGHTBRACKET and SLASH not in word:                              
                                result_temp, ft_temp = self.sequence_key_search('=_'+word[1:-1],
                                                                                return_found_terms=True)
                                

                            elif SLASH not in word:
                                if word and word[0] != LEFTBRACKET:
                                    if word and len(word)>2 and word[-2] == ATSIGN \
                                       and word[-1] in [DOLLAR,CARET,POUND,UNDERLINE,PLUS]:
                                        result_temp, ft_temp = self.sequence_key_search('ALL_'+word,
                                                                               return_found_terms=True)
                                    else:     
                                        result_temp,ft_temp = self.sequence_key_search('GT_'+word,
                                                                               return_found_terms=True)
                                else:
                                    result_temp,ft_temp = self.sequence_key_search('G_'+word[1:],
                                                                               return_found_terms=True)
                            elif SLASH in word and word and word[0] == SLASH:
                                if word[-1] == RIGHTBRACKET:
                                    result_temp,ft_temp = self.sequence_key_search('L_'+word[1:-1],
                                                                               return_found_terms=True)
                                else:
                                    result_temp,ft_temp = self.sequence_key_search('LT_'+word[1:],
                                                                               return_found_terms=True)

                            elif SLASH in word and word.count(SLASH) == 1:

                                result_temp,ft_temp = self.sequence_key_search('R_'+word,
                                                                       return_found_terms=True)
                                

                            if not not_term:

                                temp_set = temp_set.union(result_temp)
                                foundterms.update(ft_temp)

                            else:
                                if result_temp:
                                
                                    if not temp_set:
                                        temp_set = set(self.indexes())-result_temp
                                    else:                                            
                                        temp_set = temp_set - result_temp

                                    foundterms.update({'~'+f_temp for f_temp in ft_temp})
                                    

                            

                elif  self.key_dict_contains(word):
                    # for a regular keyword
                    if not not_term:

                        temp_set = temp_set.union(self.get_indexes_for_key(word))
                        if self.get_indexes_for_key(word).intersection(searchset):
                            foundterms.add(word)
                    else:

                        if not temp_set:
                            temp_set = set(self.indexes())-self.get_indexes_for_key(word)
                        else:
                            temp_set = temp_set - self.get_indexes_for_key(word)

                        foundterms.add('~'+word)
                else:
                    if not not_term:
                        pass


        else:   #if it is not a keyword

            is_a_single_word = False    

            for word in el_temp:
                
                qualifier = ''

                if word.count('"')==2:
                    #To extract the qualifier phrase and the word apart from the qualifier 
                    qualifier = '"'+word.split('"')[1]+'"'
                    word = EMPTYCHAR.join([word.split('"')[0],word.split('"')[2]])

                if word in ['!allnotes!']:
                    
                    temp_set = set(searchset)


                elif DOLLAR not in word:
                    #To search for single words
                    is_a_single_word = True

                

                    if self.word_dict_contains(word):
                        if not not_term:
                            temp_set = temp_set.union(self.get_indexes_for_word(word))
                            if self.get_indexes_for_word(word).intersection(searchset):
                                foundterms.add(word)
                        else:
                            if not temp_set:
                                temp_set = set(self.indexes())-self.get_indexes_for_word(word)
                            else:
                                temp_set = temp_set - self.get_indexes_for_word(word)
                            foundterms.add('~'+word)
                    else:
                        if not not_term:
                            pass
                        else:
                            if not temp_set:
                                temp_set = {a_temp for a_temp
                                            in self.indexes()}
                            else:
                                temp_set = temp_set.intersection(set(self.indexes()))

                else:
                    # to search for phrases

                    if not (word.endswith(DOLLAR) and word.startswith(DOLLAR)):

                        #for a searchphrase without wildcards
                        search_word = word.replace(DOLLAR,BLANK)
                        
 
                        words = [eliminate_punctuation(x) for x in word.split(DOLLAR) if eliminate_punctuation(x) not in English_frequent_words]
                        words = [x[0:-2] for x in words if x.endswith("'s")]
                        words = [x for x in words if x]
                          
                        temp_indexes = set(searchset)
                        for temp_word in words:
                            temp_indexes = temp_indexes.intersection(self.get_indexes_for_word(temp_word))

                        temp_set = set()
                        phrase_found = False
                        for temp_index in temp_indexes:
                            temp_text =  self.get_text_from_note(temp_index)
                            if search_word in temp_text:
                                temp_set.add(temp_index)
                                phrase_found = True
                        if phrase_found:
                            if not_term:
                                temp_set = set(searchset)-temp_set
                                foundterms.add('~'+search_word)
                            else:
                                foundterms.add(search_word)
                    else:
                        # for a searchphrase with wildcards


                        search_word = word
                        word = word[1:-1]
                        word = word.replace(DOLLAR,STAR+VERTLINE+STAR)
                        words = [x for x in word.split(VERTLINE) if x not in [EMPTYCHAR,STAR]]

                        

                        temp_indexes = set(searchset)

                        for segment  in words:

                            tt_temp = wildcards(segment)
                            all_terms = expand_term_list(tt_temp[0])


                            found_indexes = set()
                            

                            for temp_word in all_terms:
                                found_indexes = found_indexes.union(self.get_indexes_for_word(temp_word))

 
                            temp_indexes = temp_indexes.intersection(found_indexes)


                        def all_indexes(text,segment):
                            # get all indexes for a segment in text

                            returnlist = []
                            position = 0
                            while position < len(text) and segment in text[position:]:
                                pos = text.index(segment,position)
                                returnlist.append(pos)
                                position = pos+1
                            return returnlist

                        

                        
                        
                        if temp_indexes:
                            temp_set = set()
                            

                            for temp_index in temp_indexes:

                                temp_text =  self.get_text_from_note(temp_index)
                                position = 0
                                temp_found = True 
                                for segment in words:
                                    # To test whether the segments of the phrase
                                    # appear in order in the text

                                    segment = segment.replace(STAR,EMPTYCHAR)
                                    if segment in temp_text:
                                        positions = all_indexes(temp_text,segment)
                                        # finds all the positions in which a segment appears,
                                        # produces a set containing all those values above the current position,
                                        # and if the set is non-empty, sets the position to the minimum value of th
                                        # set. Otherwise, returns a negative result for the search.

                                        after_positions = [x for x in positions if x > position]
                                        if after_positions:
                                            position = min(after_positions)
                                        else:
                                            temp_found = False
                                            break
                                if temp_found:

                                    if not temp_set:
                                        foundterms.add(search_word)
                                    temp_set.add(temp_index)
                            if temp_set and not_term:
                                # for a negative search
                                # Here too: no result for a phrase that isn't found 
                                temp_set = set(searchset)-temp_set
                                
                            
                                    
                                    
                                            
                    

##            temp_set = temp_set.intersection(searchset)
        def get_slice_tuple (x):
            returnlist = []
            values = x.split('.')
            for v in values:
                if v.isnumeric():
                    returnlist.append(int(v))
                else:
                    returnlist.append(None)
            return tuple(returnlist)
                


        if qualifier and qualifier.count('"')==2:
            temp_qualifier = qualifier.split('"')[1]
            
            #interpret the qualifier
            
            qualifier_terms  = temp_qualifier.split('!')
            lowest_index, highest_index, users, lowest_date,highest_date, lowest_count, \
                          highest_count, lowest_size, greatest_size, min_depth, max_depth, low_slice, high_slice\
                          = None, None, None, None, None, None, None, None, None, None, None, None, None
            strict = False
            must = False
            for qt in qualifier_terms:

                # To extract the qualifier terms from the qualifier
                if qt.startswith('index=') and '/' in qt:
                    lowest_index, highest_index = qt[6:].split('/')[0],qt[6:].split('/')[1]
                if qt.startswith('user='):
                    users = qt[5:].split(PERIOD)
                if qt.startswith('date=') and '/' in qt:
                    lowest_date, highest_date = qt[5:].split('/')[0],qt[5:].split('/')[1]
                    
                if qt.startswith('count=') and '/' in qt:
                    lowest_count, highest_count = qt[6:].split('/')[0],qt[6:].split('/')[1]
                if qt.startswith('size=') and '/' in qt:
                    lowest_size,greatest_size = qt[5:].split('/')[0],qt[5:].split('/')[1]
                if qt.startswith('depth=') and '/' in qt:
                    min_depth,max_depth = qt[6:].split('/')[0],qt[6:].split('/')[1]
                if qt.startswith('slice=') and '/' in qt:
                    low_slice, high_slice = qt[6:].split('/')[0],qt[6:].split('/')[1]
                    if low_slice:
                        low_slice = get_slice_tuple(low_slice)
                    if high_slice:
                        high_slice = get_slice_tuple(high_slice)
                if qt.startswith('strict'):
                    strict = True
                if qt.startswith('must'):
                    must = True
                
                
                
                  
            old_temp_set = set(temp_set)
            temp_set = set()


            for nts in old_temp_set:
                accepted = True
                # test the notes that have been found to see if they satisfy the qualification
                if lowest_index and Index(nts) < Index(lowest_index):

                    accepted = False
                if highest_index and Index(nts) > Index(highest_index):

                    accepted = False
                if min_depth and min_depth.isnumeric() and Index(nts).level() < int(min_depth):
                    accepted = False
                if max_depth and max_depth.isnumeric() and Index(nts).level() > int(max_depth):
                    accepted = False
                if low_slice and not Index(nts).within(limit=low_slice,not_less=True,must_have=must):
                    accepted = False
                if high_slice and not Index(nts).within(limit=high_slice,not_more=True,must_have=must):
                    accepted = False
                    
                    
                if users or lowest_date or highest_date or lowest_size or greatest_size:

                    #For qualifier terms involving the metadata
                    temp_meta = self.get_metadata_from_note(nts)
                    if 'user' in temp_meta and users and temp_meta['user'] not in users:
                        accepted = False
                    if 'size' in temp_meta:
                        if lowest_size and lowest_size.isnumeric() and temp_meta['size'] < int(lowest_size):
                            accepted = False
                        if greatest_size and greatest_size.isnumeric() and temp_meta['size'] > int(greatest_size):
                            accepted = False
                    if 'date' in temp_meta:
                        
                        meta_year, meta_month, meta_day = [int(x.replace("'",EMPTYCHAR))
                                                           for x in temp_meta['date'][-1].split(BLANK)[0].split(DASH)][0:3]

                        if lowest_date:

                            
                            lowest_year,lowest_month,lowest_day = [int(x) for x in lowest_date.split(DASH)+['1','1']][0:3]

                            if (meta_year < lowest_year
                                or (meta_year==lowest_year and meta_month<lowest_month)
                                or (meta_year==lowest_year and meta_month==lowest_month and meta_day < lowest_day)):
                                accepted = False
                                
                            
                        if highest_date:
                            temp_highest_date  =  highest_date.split(DASH)
                            if len(temp_highest_date) == 3:
                                pass
                            elif len(temp_highest_date) == 2:
                                temp_highest_date += ['31']
                            elif len(temp_highest_date) == 1:
                                temp_highest_date += ['12','31']
                                
                            highest_year,highest_month,highest_day = [int(x) for x in temp_highest_date]
                            if (meta_year > highest_year
                                or (meta_year==highest_year and meta_month>highest_month)
                                or (meta_year==highest_year and meta_month==highest_month and meta_day > highest_day)):
                                accepted = False                          
                        
                        
                if is_a_single_word and (lowest_count or highest_count):
                    #For the count of a single word
                    temp_text =  BLANK+self.get_text_from_note(nts)+BLANK
                    temp_count = 0
                    if strict:
                        for l_char in string.punctuation+BLANK:
                            for r_char in string.punctuation+BLANK:
                            
                                temp_count += temp_text.count(l_char+word+r_char)
                    if not strict:
                        temp_count = temp_text.count(word)
                        
                    if lowest_count and lowest_count.isnumeric() and temp_count<int(lowest_count):
                        accepted=False
                    if highest_count and highest_count.isnumeric() and temp_count>int(highest_count):
                        accepted=False
                    
                if accepted:
                    temp_set.add(nts)
            qualifier=''
            if not_term:
                temp_set = set(searchset) - temp_set
                    
            
        universe[unmodified_term] = temp_set.intersection(searchset)#Populates the universe
                                                                    #with search results
    

    result = parser.interpret(parsed_query,universe=universe) #completes the search

    return query, result, foundterms

    
