"""TRUTH TABLE GENERATOR
 by ANTHONY CURTIS ADLER"""

left_mark = '{'
right_mark = '}'


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

          if char == left_mark:
               if level == 0:
                    left_point = count
               level+=1
          if char == right_mark:
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

     if not contains(phrase,left_mark+right_mark):

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

     for operator in ['|','&']:
          level = 0 # reset level
          if not found:
          
          
               for x,char in enumerate(phrase):
                    if char == left_mark:
                         level += 1
                    if char == right_mark:
                         level -=1
                         # level indicates level within hierarchy established by parantheses

                    if level == 0 and x+1 < len(phrase) and phrase[x+1] == operator:
                         phrase[x+1] = '!@'+operator+'@!'
                         found = True
                         break
                    
               

     if '!@&@!' in phrase:
          # For AND
          phrases = ''.join(phrase).split('!@&@!')
     elif '!@|@!' in phrase:
          # For OR 
          phrases = ['@']+''.join(phrase).split('!@|@!')
     print('PHRASE',phrase)

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

     return not contains(phrase,left_mark+right_mark+'&|')
     
def is_set (phrase):
     """Returns TRUE if <phrase> is boolean."""
     
     return isinstance(phrase,set)

def and_sum (phrase):

     """Returns TRUE iff every element in <phrase> is TRUE"""
     if len(phrase) > 0:
          total = set(phrase[0])
     else:
          total = set() 
     for x in phrase:
          total = total.intersection(x)
     return total 

def or_sum (phrase):

     """Returns TRUE iff one element in <phrase> is TRUE"""

     total = set()
     for x in phrase:
          total = total.union(x)
     
     return total 

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
          phrase = phrase.strip()
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

     elif isinstance(phrase,str):
          phrase = phrase.strip()
          
          if phrase=='@':
               return '@'
          if phrase in universe:
                         
               return universe[phrase]
          else:
               return set()
               
     
     elif isinstance(phrase,set):         
          return phrase
     elif all_is_P(phrase,predicate_function=is_set) or (phrase[0]=='@' and all_is_P(phrase[1:],predicate_function=is_set)):
               # If an AND or OR LIST, return TRUE or FALSE for the list.
               if phrase[0]=='@':
                    return or_sum(phrase[1:])
               else:
                    return and_sum(phrase)

     if isinstance(phrase,str):
          phrase = [phrase]
               
                    #Eliminate null elements.
     return interpret([interpret(x,universe=universe) for x in phrase],universe=universe)
                    #Recursively calls function.


def get_variables (phrase):

     """Get all variables from a phrase."""

     for char in left_mark+right_mark+'&|':
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


def truth_table (phrase):

     """Print out the truth table for <phrase>
     """
     
     return_text = []

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
          rank = left_mark+str(counter)+right_mark
          rank =  rank + ((len(str(len(universes)))+2)-len(rank))*' '
          for r in row:
               header+=('~' not in r)*' '+r+' '
          
          
          return_text.append(rank+': '+header+ ' | ' + str(result))
     max_length = max([len(x) for x in return_text])
     final_text = ''
     for x in return_text:
          if x != '_':
               final_text += x+(max_length-len(x))*' '+'\n'
          else:
               final_text += '_'*max_length+'\n'
     return final_text 
          
     


##print(ENTERSCRIPT)
##
##while True:
##
##     try:
##
##          print(truth_table(input('?')))
##     except:
##          print('INVALID INPUT')
##
##
     


          
          
     

     
          
     
     
     
     

          
               
               


          


