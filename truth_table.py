"""TRUTH TABLE GENERATOR
 by ANTHONY CURTIS ADLER"""



to_replace = {'=>':'>',
                   '->':'>',
                   '<>':'#',
                   'AND':'&',
                   '^':'&',
                   'v':'|',
                   'OR':'|',
                   'and':'&',
                   'or':'|',
                   'iff':'#',
                   'is equivalent to':'#',
                   'implies':'>',
                   '[':'(',
                   ']':']',
                   '-':'~'}

ENTERSCRIPT = "          TRUTH TABLE GENERATOR    **"+\
              "         by Anthony Curtis Adler***"+\
              "     ENTER A PHRASE TO INTERPRET *"+\
              "     USING THE FOLLOWING SYMBOLS:**"\
              "AND,and,&,^                = LOGICAL AND *"+\
              "OR,or,V,|                  = LOGICAL OR *"+\
              "iff,is equivalent to,<>    = LOGICAL EQUIVALENCY*"+\
              ">,=>,->,implies            = LOGICAL IMPLICATION*"+\
              "-,~                        = NEGATION*"+\
              "[] ()                      = BRACKETS***"

ENTERSCRIPT = ENTERSCRIPT.replace('*','\n')

              

                    

def contains (phrase,chars):

     """Returns TRUE if <phrase> contains ANY one of <chars>"""

     for x in chars:

          if x in phrase:
               return True
     return False

def bracketed (phrase):

     """Returns TRUE if <phrase> is encompassed by a left bracket and a right bracket
     at the same hierarchical level"""

     level = 0
     left_point = None
     right_point = None
     

     for count,char in enumerate(phrase):

          if char == '(':
               if level == 0:
                    left_point = count
               level+=1
          if char == ')':
               level-=1
               if level == 0:
                    right_point = count
     if not (left_point is None)  and (not right_point is None) and left_point == 0 and right_point == len(phrase)-1:
          return True
     return False 

def all_boolean (phrase):
     
     """Returns TRUE if all elements of <phrase> are boolean"""

     if not isinstance(phrase,list):
          return False
     for x in phrase:
          if not isinstance(x,bool):
               return False
     return True 

     

def split_into_phrases (phrase):
     
     """Inputs a string and returns a list containing elemenets, split according to parsing rules.
     IF the list is of elements to be combined with AND, then no header.
     If the list if of elements to be combined with OR, then '@' at the head of the list.

     """

     if not contains(phrase,'()'):

          #For a phrase without parantheses
          

          if '|' in phrase:
               return ['@']+[x for x in phrase.split('|')]
          elif '&' in phrase:
               return [x for x in phrase.split('&')]

     #If the phrase contains parantheses.
     
     phrase = list (phrase)
         #convert string into a list of chars
     level = 0
     found = False # if one of the operators is found in the phrase 

     for operator in ['#','>','|','&']:
          level = 0 # reset level
          if not found:
          
          
               for x,char in enumerate(phrase):
                    if char == '(':
                         level += 1
                    if char == ')':
                         level -=1
                         # level indicates level within hierarchy established by parantheses

                    if level == 0 and x+1 < len(phrase) and phrase[x+1] == operator:
                         phrase[x+1] = '<<'+operator+'>>'
                         found = True
                         break
                    
               

     if '<<&>>' in phrase:
          # For AND
          phrases = ''.join(phrase).split('<<&>>')
     elif '<<|>>' in phrase:
          # For OR 
          phrases = ['@']+''.join(phrase).split('<<|>>')
     elif '<<>>>' in phrase:
          # For INFERENCE 
          premise = ''.join(phrase).split('<<>>>')[0]
          conclusion = ''.join(phrase).split('<<>>>')[1]
          phrases = ['@','~'+premise,conclusion]
          #  A => B  translated as ~A OR B
     elif '<<#>>' in phrase:
          # FOR EQUIVALENCY 
          premise = ''.join(phrase).split('<<#>>')[0]
          conclusion = ''.join(phrase).split('<<#>>')[1]
     
          phrase1 = '~'+'('+premise+'&'+'~'+conclusion+')'
          phrase2 = '~'+'('+conclusion+'&'+'~'+premise+')'
          phrases = [phrase1,phrase2]
          # A<>B translated as (~A or B) & (~B or A) 
          
     return [x for x in phrases]

def all_is_P (phrase,predicate_function=None):

     """Returns TRUE if <predicate_function> is TRUE of
     every element in <phrase>"""

     returnvalue = True
     for x in phrase:
          if not predicate_function(x):
               returnvalue = False
     return returnvalue

def all_is_None (phrase):

     """Returns TRUE if all elements in <phrase> is null"""

     phrase = [x for x in phrase if not x is None]
     return phrase == []

def some_is_None (phrase):

     """Returns TRUE if some elements in <phrase> are none"""

     for x in phrase:
          if x is None:
               return False
     return True 

def is_simple (phrase):

     """Returns TRUE if <phrase> is a simple name, i.e. a variable"""

     return not contains(phrase,'()&|>#')
     
def is_bool (phrase):
     """Returns TRUE if <phrase> is boolean."""
     
     return isinstance(phrase,bool)

def and_sum (phrase):

     """Returns TRUE iff every element in <phrase> is TRUE"""
     for x in phrase:
          if not x:
               return False
     return True

def or_sum (phrase):

     """Returns TRUE iff one element in <phrase> is TRUE"""
     for x in phrase:
          if x:
               return True
     return False

def heading_count(phrase,char='~'):

     """Returns the number of negating prefixes in <phrase> and the <phrase> shorn of prefixes."""
     count = 0
     for x in phrase:
          if x  != char:
               break
          count+=1
     return count,phrase[count:]




def parse (phrase):

     """The primary recursive parsing function"""

     if isinstance(phrase,str):
          #If the phrase is a string
          if is_simple(phrase):
               #EXITS the recursion
               if phrase[0:2] == '~~':
                    return phrase[2:]
                    #Eliminates negations that cancel each other
               return phrase
          elif bracketed(phrase):
               #Eliminate top-level parantheses
               return parse(phrase[1:-1])
          elif phrase[0] == '~':
               #If the phrase begins with a negating prefix...
               negations,phrase = heading_count(phrase)
               
               if bracketed(phrase):
                    #If the negated phrase is bracketed
                    if negations % 2 == 1:
                         subphrase = split_into_phrases(phrase[1:-1])
                         if subphrase[0] != '@':                                     
                              #De Morgan's Law 
                              return parse(['@']+['~'+x for x in subphrase])
                         else:
                              #De Morgan's Law
                              return parse(['~'+x for x in subphrase[1:]])
                    else:
                         return parse(phrase[1:-1])
               return parse(split_into_phrases((negations%2)*'~'+phrase))
               
          else:
               return parse(split_into_phrases(phrase))
     # IF the phrase is a list
     if all_is_P(phrase,predicate_function=is_simple):
          #If every terms of the phrase list is simple...
          #This prepares for EXIT from recursion
          return [parse(x) for x in phrase]
     return parse([parse(x) for x in phrase])



def extract_lists (phrase):

     """IF <phrase> = [ITEM1,ITEM2,[LIST1,LIST2]] yields
          [ITEM1,ITEM2,LIST1,LIST2]"""

     def list_of_lists (phrase):
          # TRUE if every element of <phrase> is a list
          for x in phrase:
               if not isinstance(x,list):
                    return False
          return True

     def some_lists (phrase):
          # True if some elements of <phrase> are lists.
          for x in phrase:
               if isinstance(x,list):
                    return True
          return False
          
          

     

     def extract (x):
          # Recursive function to extract lists.
          returnlist = []
          if not isinstance(x,list):
               returnlist = x
          elif not some_lists(x):
               returnlist = x
          elif not list_of_lists(x):
               returnlist = x
          else:
               # For a list composed of lists
               for y in x:
                    
                    if isinstance(y,list) and not list_of_lists(y):
                         returnlist.append(extract(y))
                    else:
                         for z in y:
                              # Extracts elements of a list of lists into the containing list
                              returnlist.append((extract(z)))
          return returnlist

     return extract(phrase)
               
                    
               

def no_or_clauses (phrase):
     """ Returns TRUE if <phrase> contains no OR lists."""
     
     for x in phrase:
          if isinstance(x,list) and x[0] == '@':
               return False
     return True 

def enter (phrase,universe=None):

     """Enters the truth value of <phrase> into <universe>.
     """

     negations, phrase = heading_count(phrase)
     value = {0:True,
              1:False}[negations % 2]
     if phrase not in universe:
          universe[phrase] = value
     else:
          # If there is a contradiction, return NULL
          if universe[phrase] != value:
               return None
     
     return True

    

def multiply (phrase):

     """Recursive function to combine AND or OR lists.
     The PRODUCT of OR lists is used to generate the TRUTH TABLE.
     """

     if not isinstance(phrase,list):
          return phrase
     
     if no_or_clauses(phrase):
          # IF there are only AND lists at the top level


          return [multiply(x) for x in phrase]

     else:
          # For a combination of AND and OR lists
          and_clauses = []
          or_clauses = []
          
          for x in phrase:
               # DIVIDES into AND and OR lists 
               if isinstance(x,list) and x[0]=='@':
                    or_clauses.append(x)
               else:
                    and_clauses.append(x)
          multiplied_phrases = [and_clauses]


          for x in or_clauses:
               # Produces the product of two OR lists.
               # [A,B][C,D] = [[A,C],[A,D],[B,C],[B,D]]

               new_phrases = []
               for y in x[1:]:


                    for z in list(multiplied_phrases):
                         if not isinstance(z,list):
                              
                              new_phrases.append([z,y])
                         else:
                              new_phrases.append(z+[y])
               multiplied_phrases =  [multiply(x) for x in new_phrases]
               
     return extract_lists(multiplied_phrases)
                    



def interpret (phrase,universe=None):

     """Recursive function interpreting LIST of AND and OR lists containing BOOLEAN values to
     yield a BOOLEAN value.
     <universe> is the dictionary representing the true facts with reference to which the
     value of <phrase> will be calculated."""


     if phrase is None:
          return phrase

     if isinstance(phrase,str):
          
          if phrase=='@':
               return '@'
          negations,phrase = heading_count(phrase)
          if phrase not in universe:
               # IF the truth value of phrase not defined in universe.
               return None
               
          if negations % 2 == 0:
               if phrase in universe:
                    # If no negative prefix, return value of phrase in universe.
                    
                    return universe[phrase]
          else:
               if phrase in universe:
                    # If negative prefix...
                         
                    return not universe[phrase]
               
     
     if isinstance(phrase,bool):
          
          return phrase
     elif all_is_P(phrase,predicate_function=is_bool) or (phrase[0]=='@' and all_is_P(phrase[1:],predicate_function=is_bool)):
               # If an AND or OR LIST, return TRUE or FALSE for the list.
               if phrase[0]=='@':
                    return or_sum(phrase[1:])
               else:
                    return and_sum(phrase)
     phrase = [x for x in phrase if not (x is None)]
          #Eliminate null elements.
     if not phrase:
          return None 
     return interpret([interpret(x,universe=universe) for x in phrase],universe=universe)
          #Recursively calls function.


def get_variables (phrase):

     """Get all variables from a phrase."""

     for char in '()&~|>#':
          phrase = phrase.replace(char,' ')
     phrase = phrase.split(' ')
     phrase = list(set([x for x in phrase if x]))
     return phrase

def generate_truth_tables (variables):

     """Generates list for the entered variables.
     V1,V2 => ['@',V1,~V1]*['@',V2,~V2] => [[V1,V2],[V1,~V2],[~V1,V2],[~V1,~V2]]
     This list represents all the possible values for the given variables.
     """

     variable_pairs = []

     for x in variables:
          variable_pairs.append(['@',x,'~'+x])
     return multiply(variable_pairs)

def populate_universe (phrase):

     """Returns a universe populated with truth values.
     """
     
     new_universe = {}

     for x in phrase:
          enter(x,new_universe)
     return new_universe

def generate_truth_universes(phrase):

     """Returns a list of universes corresponding to possible
     values of variables."""

     universe_list = []

     for x in generate_truth_tables(get_variables(phrase)):
          universe_list.append((x,populate_universe(x)))
     return universe_list 



     

def format_input (phrase):

     """Formats input to account for different symbolic conventions"""
     

     to_replace = {'=>':'>',
                   '->':'>',
                   '<>':'#',
                   'AND':'&',
                   '^':'&',
                   'v':'|',
                   'OR':'|',
                   'and':'&',
                   'or':'|',
                   'iff':'#',
                   'is equivalent to':'#',
                   'implies':'>',
                   '[':'(',
                   ']':']',
                   '-':'~'}

     for x in to_replace:

          phrase = phrase.replace(x,to_replace[x])
          phrase = phrase.replace(' ','')
          
     return phrase

def help():

     return ENTERSCRIPT 

class TruthTable:

     def __init__ (self,phrase):

          self.finished_table = {}
          self.text = self.generate(phrase)
          self.phrase = phrase
          

     def generate (self,phrase):

          """Print out the truth table for <phrase>
          """
          self.finished_table = {}
          return_text = []
          return_text.append('TRUTH TABLE FOR '+phrase)
          return_text.append('_')
          phrase = format_input(phrase)

          universes = generate_truth_universes(phrase)
               # Generate the universes
          for counter, x in enumerate(universes):

               universe = x[1]
               row = sorted(x[0],key=lambda x:x.replace('~',''))
               result = interpret(parse(phrase),universe=universe)
                    # the values of the rows in the truth table
                    # determined by interpreting PHRASE in the
                    # given universe
               header = ''
               head_list = []
               rank = '('+str(counter)+')'
               rank =  rank + ((len(str(len(universes)))+2)-len(rank))*' '
               for r in row:
                    header+=('~' not in r)*' '+r+' '
                    head_list.append(r)
                    
               
               return_text.append(rank+': '+header+ ' | ' + str(result))
               temp_tup = tuple(sorted(head_list,key=lambda x:x.replace('~','')))
               self.finished_table[temp_tup] = result
          max_length = max([len(x) for x in return_text])
          final_text = ''
          for x in return_text:
               if x != '_':
                    final_text += x+(max_length-len(x))*' '+'\n'
               else:
                    final_text += '_'*max_length+'\n'
          return final_text
     


     def __eq__ (self,other):

          listify = lambda x:sorted(','.join(y)+'/'+str(x[y]) for y in x)
          return listify (self.finished_table)==listify(other.finished_table)

     def __str__ (self):
          return self.text

     def __truediv__ (self,other):

          return TruthTable(self.phrase+'&'+other.phrase)

     def __mul__ (self,other):

          return TruthTable(self.phrase+'|'+other.phrase)

     def __gt__ (self,phrase):

          return self==(self/phrase)
     
                            
     

                     
def truth_table (x):

     T = TruthTable(x)
     return_text = str(T)

     return return_text
          

     
     
          
     
     
     
     

          
               
               


          


