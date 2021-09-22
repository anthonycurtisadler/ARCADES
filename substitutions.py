import random, extract, nformat
from globalconstants import LEFTPAREN, RIGHTPAREN, \
     ANDSIGN, VERTLINE, BLANK,\
     PERCENTAGE, LEFTNOTE, RIGHTNOTE, EMPTYCHAR, POUND, TILDA


def transform_or_to_and (phrase,left_b='(',right_b=')',to_find='|',to_replace='&'):

    phrase = list(phrase)
    degree = 0
    results = []
    for count, ch in enumerate(phrase):

        if ch == left_b:
            degree+=1
        elif ch == right_b:
            degree-=1
        if ch==to_find and degree==0:
            results.append(count)

    for p in results:
        phrase[p] = to_replace

    return ''.join(phrase)


def get_terms_from_query (query, delete_tilda=False):

    """Fetches terms form query"""
    returnquery = query 
    for a_temp in [LEFTPAREN, RIGHTPAREN, ANDSIGN, VERTLINE]:  
        query = query.replace(a_temp, '  '+a_temp+'  ')


    query = nformat.reduce_blanks(query)

    for a_temp in [LEFTPAREN, RIGHTPAREN, ANDSIGN, VERTLINE]:
        query = query.replace(a_temp, '[ELIM]')
    if delete_tilda:
        query = query.replace(TILDA, EMPTYCHAR)
        

        
    termlist = [x.strip() for x in sorted(set(query.strip().split('[ELIM]'))) if x]

    return termlist, returnquery

def get_new_code ():

    code_set = set('0')
    while True:

        one_digit = lambda x:random.choice(range(0,10))
        new_code = '0'
        while new_code in code_set:
            
            new_code = ''.join([str(one_digit(None)) for x in range(10)])
        code_set.add(new_code)
        yield new_code

def get_left_right (x):

    x = x.strip()
    left_position = None
    right_position = None 
    for pos, ch in enumerate(x):
        if not left_position is None and right_position is None and ch in ['>','"','/']:
            right_position = pos
        if left_position is None and ch not in ['<','~','#','/','[']:

            left_position = pos
                
    if not left_position:
        left_position = 0
    if not right_position:
        right_position = len(x)
    
    return x[left_position:right_position],x[0:left_position],x[right_position:]

        
        


class Substitutions:

    def __init__ (self, query):

        self.query = query
        self.substitution_dictionary = {}
        self.encloser_dictionary = {}
        self.reverse_substitution_dictionary = {}
        self.negated_dictionary = {}
        self.keywords = set()
        self.textwords = set()
        self.tags = set()
        



    def substitute (self,query=None,keeping=False,delete_tildas=True):

        """For replacing the terms with 10 digit codes so that replacement errors
        won't occur.

        Accepts string as input, returns dictionary for unsubstituting"""


        remove_enclosing = lambda x:x.replace('<','').replace('#','').replace('>','')

        if query is None:
            query = self.query

            
       
        code = get_new_code()
        query = ' '+query.replace('&',' & ').replace('|',' | ').replace('(','( ').replace(')',' )')+' '
        all_terms, query = get_terms_from_query(query)
        
        def not_key_bracket (x):

            if not '<' in x and not '>' in x and not '[/' in x and not '/]' in x:
                if not '"' in x:
                    return '[/'+x+'/]'
                else:
                    return '[/'+x.split('"')[0]+'/]"'+x.split('"')[1]
                

            else:
                return x

        while '  ' in query:
            
            query = query.replace('  ',' ')
            

        for at in sorted(all_terms,key=lambda x:-len(x)):
            query = ' '+query+' '
            at = at.strip()

            if '~~' in at:
                oldat=at
                at = at.replace('~~','')
               
            if at.startswith('~'):
                    negated = True
                    at = at[1:]
            else:
                negated = False


            if at.replace('{','').replace('}','').strip().isnumeric():

                pass

            else:

                if (not_key_bracket(at),negated) not in self.reverse_substitution_dictionary:
                    # for a new term
                    new_code = '{'+next(code)+'}'
                    bare_term, left_part,right_part = get_left_right(not_key_bracket(at))
                    if left_part == '<#' and right_part.startswith('>'):
                        self.tags.add(new_code)
                    elif left_part == '<' and right_part.startswith('>'):
                        self.keywords.add(new_code)
                    else:
                        self.textwords.add(new_code)
                        left_part, right_part = '[/', '/]'
                        at = '[/'+ at + '/]'
                    
                    
                    self.substitution_dictionary[new_code]=(at,negated)
                    self.reverse_substitution_dictionary[at,negated]=new_code
                    
                    if '[/' in at:

                        query = query.replace(' '+negated*'~'+at.replace('[/','').replace('/]','')+' ',' '+negated*'~'+at+' ')
                        
                    
                    query = query.replace(' '+(delete_tildas*negated)*'~'+at+' ',' '+((not delete_tildas)*negated)*'~'+new_code+' ')
                    
                    self.encloser_dictionary[new_code]= (left_part,right_part)
                   
              
                   
                    
                else:

                    # For a term being used again, replace with same code as before
                    

                    if (not_key_bracket(at),negated) in self.reverse_substitution_dictionary:
                        

                        query = query.replace(' '+negated*'~'+at+' ',' '+((not delete_tildas)*negated)*'~'+self.reverse_substitution_dictionary[(not_key_bracket(at),negated)]+' ').strip()
                        
                
    ##            else remove_enclosing(at) in self.substitution_dictionary:
    ##                #if a code is appearing again
    ##                pass
            query = query.strip()   
            
                           
        if not keeping:
            self.query = query.strip()
        
        return ' '+query.strip()+' '

    def reverse (self,query=None,transform=False):
        if query is None:
            return_query = self.query
        else:
            return_query = query
        return_query = ' '+return_query+' '
        

##        return_query = return_query.replace('~','')
       
        for code in self.substitution_dictionary:
            sub_term, negated = self.substitution_dictionary[code]
            
            
            term_to_replace = ('~'*negated+sub_term).replace('~~','')
            
            
            return_query = return_query.replace(' '+code+' ',' '+term_to_replace+' ')

        if transform:
            return transform_or_to_and(return_query.strip())

        return return_query.strip()

    def update (self,query):

        return self.substitute (query)

    def unencode (self, entryset,sign=False,reversing=False,purging=True,keep_tilda=False):

        purge = lambda x:x 
        if purging and not keep_tilda:
            purge = lambda x:x.replace(LEFTNOTE,EMPTYCHAR).replace(RIGHTNOTE,EMPTYCHAR).replace(POUND,EMPTYCHAR).replace(TILDA,EMPTYCHAR).replace('[/','').replace('/]','')
        elif purging:
            purge = lambda x:x.replace(LEFTNOTE,EMPTYCHAR).replace(RIGHTNOTE,EMPTYCHAR).replace(POUND,EMPTYCHAR).replace('[/','').replace('/]','')

        
        with_string = False
        
        if isinstance(entryset,str):
            entryset = {entryset}
            with_string = True 
            

        returnset = set()
        for x in entryset:
            if not reversing:
                if x in self.substitution_dictionary:
                    returnset.add('~'*(keep_tilda*self.substitution_dictionary[x][1])+purge(self.substitution_dictionary[x][0]))
                    
            else:
                if (x, sign) in self.reverse_substitution_dictionary:
                    returnset.add(self.reverse_substitution_dictionary[(x,sign)])
        if with_string:
            if len(returnset)==1:
                return list(returnset)[0]
            else:
                return ''
        return [x for x in returnset]

    def add_tildas (self,only_text=True):

        if not '~' in self.query:

            query_text = self.query
            

            for x in self.substitution_dictionary:
                if self.substitution_dictionary[x][1]:
                    query_text = self.query.replace(x,'~'+x)
                    
        if not only_text:
            self.query = query_text
            return self
        return query_text

    def delete_tildas (self):
        self.query = self.query.replace('~','')
        return self

    def encode (self, entryset):

        return self.unencode (entryset,sign=False, reversing=True)

    def partial (self,query,delete_tildas=True):
        return self.substitute(query=query,keeping=True,delete_tildas=delete_tildas)

    def get_brackets (self,term):
        if term in self.encloser_dictionary:
            return self.encloser_dictionary[term]
        else:
            return ('','')

    def get_negated (self, term):
        if term in self.substitution_dictionary:
            return self.substitution_dictionary[term][1]
        else:
            return False

    def double_vert (self):

        self.query = self.query.replace('| |','||')

        self.query = self.query.replace('||','|')
        return self
    
        
    

    

        
        
            
            

        


