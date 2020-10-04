# Simple program for facilitating the creation of book indexes.
# To help determine the key words, establish page numbers,
# and format the final index. 


import pdfplumber, os, string, simple_parser_mod as parser, pickle
import copy
import nltk
from nltk import word_tokenize


from lexical import English_frequent_words
from spellchecker import SpellChecker
from globalconstants import YESTERMS
from numbertools  import format_range, rom_to_int, int_to_roman






first_romans = [int_to_roman(x) for x in range(1,300) if x]
NAME_WORDS = ['von','van','de','della','la','da','les','los','las']

max_title_length = 15

directoryname = os.getcwd()
folder = os.altsep+'pdfs'+os.altsep
index_folder = os.altsep+'indexer'+os.altsep
speller = SpellChecker()
os.system('color F0')

YESTERMS += [' ']
string.punctuation += '—'
DIVIDER = '__________________________________________________________'

from colorama import Fore, Back, Style 

def some_letters (x):

    """Returns TRUE if a phrase has some characters that are
    not whitespace or punctuation."""

    letters = set(x)
    for char in letters:
        if char not in string.whitespace+string.punctuation:
            return True
    return False



def extract_page_number (text,from_top=False):

    """Determines the first numeric string in either
    the top or the bottom of the text"""

    # to test whether the text has not blank and non
    # punctuation characters
    if not text:
        return ''
    text = text.rstrip()
    text = text.replace('\n',' ')
    ghost_text = text
    for x in string.punctuation+string.whitespace:
        ghost_text = ghost_text.replace(x,'')
    if not ghost_text:
        return ''
    
        
    if ' ' not in text:
        return ''
    numeric_found = False
    for x in '0123456789ivx':
        if x in text:
            numeric_found = True
    if not numeric_found:
        return ''

    #Testing for the simplest case,
    #Namely that the page number is
    #immediately at top or bottom
    #of the page
    
    if not from_top:
    
        page_no = text.split(' ')[-1]
    else:
        page_no = text.split(' ')[0]

    if page_no.isnumeric() or page_no in first_romans:
        return page_no

    if not from_top:
        text = ''.join(reversed(text))

    #In case the page no. is not
    #immediately at the top or bottom
    #of the page 
    numeric_found = False
    page_no = ''
    for char in text:
        if char.isnumeric():
            page_no += char
            if not numeric_found:
                numeric_found = True
        else:
            if numeric_found:
                break
    if not from_top:
        page_no = ''.join(reversed(page_no))
    
    
    return page_no

def is_date (x):

    """Returns TRUE if a string
    is formatted like a date.
    """

    x = x.replace('-','').replace('–','').strip()
    return x.isnumeric()

def un_date (x):

    """Removes the date/date range from the
    end of a book title"""

    while ',' in x and  last_is_date(x):
        x = ','.join(x.split(',')[0:-1])
    return x

def last_is_date (x):

    """True if a string ends with a date/date-range"""
    
    if not ',' in x:
        return True
    return is_date(x.split(',')[-1])

SMALL_WORDS = ['and','of','from','the','a','but','as','if','is','was','because','has']

class Reader:

    """ Interprets a PDF into text divided into pages, indexed words,
    sentences, quoted phrases, parenthesized phrases, bracketed phrases.
    The READER class is instantiated as a TEXT object, which contains all the
    basic information about the TEXT"""
    
    

    def __init__ (self):

        self.page_record = [] #list of pages found in PDF
        self.sentence_record = [] #List of sentences found
                                  #consisting of a tupple:
                                  #(starting position,
                                  #(finishing position,
                                  #(sentence count)
        
        self.page_dict = {}       #keys = page #
                                  #values = (starting position,
                                  #          ending position)
        self.sentences = set()    #Set of sentence strings
        self.brackets = set()     #Set of bracketed phrases       
        self.sentence_dict = {}
        
        self.pages = {}           #keys = page #
                                  #value = page text
        self.italicized_chars = set() #keeps track of positions in
                                      #text of italicized characters
        self.italicized_phrases = set()
        self.parenthetical_phrases = set()
        self.bracketed_phrases = set()
        self.capitalized_phrases = set() 
        self.quoted_phrases = set()
        self.all_text = ''       #The entire text as a single object      
        self.words = {}          #keys = words / values = page#
        self.words_in_sentences = {} #keys = words / values = sentence#
        self.nouns = set()           #identifies all nouns
        self.histio = {}             #keeps track of word frequency
        self.italic_dict = {}      #keeps track of pages in which italic expressions are found
        self.title_dict = {}      #keeps track of pages in which titles are found 
        self.capital_histio = {}  #keeps track of capitalized expressions 
        self.first_words = set()  #first words in sentences

        ##This data structure is very messy; could be simplified, cleaned up;
        ##too much redundancy.

        
    def get_pages_for_sentences(self,sentence_list=None):

        """Returns pages in which a sentence can be found"""
        
        return_pages = set()
        for s in sentence_list:
            if s in self.sentence_dict:
                return_pages.update(set(self.sentence_dict[s][2].split(',')))
        return return_pages
        
    def load (self,filename='test.pdf'):

        """Reads a PDF file and analyzes it,
        dividing it into page, and extracting
        italicized, bracketed, quoted, etc.
        phrases, and well as creating a general histogram,
        and dividing it into sentences."""

        def get_parameters ():

            """Query user for the parameters for intepreting"""
            from_top = input('Is the page number on top of the page?') in YESTERMS
            add_italic_caps = input('Include italicized capital expressions?') in YESTERMS

            return from_top, add_italic_caps

        def get_all_fonts_from_page (page_data):

            """Retrieves unique fonts from a single page"""
            
            fonts = set()
            for char in page_data.chars:
                if char['fontname'] not in fonts:
                    fonts.add(char['fontname'])
            return fonts

        def get_all_fonts_from_text (text,from_this=0,to_that=1000):

            """To retrieve all unique fonts from all texts"""
            
            all_fonts = set()
            query = True
            for counter, page in enumerate(text.pages[from_this:to_that]):
                print(DIVIDER)
                print(counter)
                found = get_all_fonts_from_page(page)
                print(found)
                if query:
                    inp = input('RETURN to continue, SPACE+RETURN to stop querying! ')
                    if inp:
                        query = False
                all_fonts.update(found)
            return all_fonts

        def determine_exclude_set (font_set):

            """To query which fonts are to be excluded"""
            
            return_set = set()
            print('ALL FONTS: ',','.join(font_set))
            for f in sorted(font_set):
                if input('EXCLUDE'+f+'? ') in YESTERMS:
                    return_set.add(f)
            return return_set

        

     
        position_at = 0
        sentence_starts_at = 0
        found_left_paren = False
        found_left_bracket = False
        found_left_quote = False
        paren_string = ''
        bracket_string = ''
        quoted_string = ''
        sentence_string = ''
        sentence_count = 0
        word_starting = False
        capitalized_words = []
        last_capitalized = False
        word_position_in_sentence = 0
        italic_pages = []
        last_not_alpha = False
        if not filename.endswith('.pdf'):
            filename+= '.pdf'
        excluded_fonts = set()
        sentence_pages = set()

            
        
        word = ''
        text_to_exclude = []
        
        
        first_page = True
        last_found_page = None
        from_top, add_italic_caps = get_parameters()

        def get_limits (pdf,from_this,to_that):

            """To make sure page limit is within bounds
            """
            
            if from_this >= len(pdf.pages):
                from_this = len(pdf.pages)-1
            if to_that >= len(pdf.pages):
                to_that = len(pdf.pages)-1
                            
            return from_this, to_that
        
        def proper_page (x,to=False):

            """Returns an integer for a numeric string,
            otherwise 0 or high upperbound"""

            if x.isnumeric():
                x = int(x)
            else:
                if to:
                    x = 10000000000000 
                else:
                    x = 0
            return x

        
                    
        
        
        with pdfplumber.open(directoryname+folder+filename) as pdf:

            #Main procedure for analyzing the pdf and extracting text
            
            from_this, to_that = proper_page(input('START FROM? ')), proper_page  (input('GO TO? '),to=True)
            
            from_this, to_that = get_limits(pdf,from_this,to_that)
            if input('REVIEW ALL FONTS IN PDF? ') in YESTERMS:
                excluded_fonts = determine_exclude_set(get_all_fonts_from_text(pdf,from_this,to_that))
            for page in pdf.pages[from_this:to_that]:
                page_start = position_at
                
                text = page.extract_text()

                tokenized_text = word_tokenize(text)
                words_with_tokens = nltk.pos_tag(tokenized_text)
                all_nouns = set()

                for w in words_with_tokens:

                    if w[1] in ['NN','NNS']:
                        all_nouns.add(w[0])
                
                self.nouns.update(all_nouns)
                
                        
                
                
                query = False
                once_through = False
                exclude = False
                while True:
                    page_no = extract_page_number(text,from_top=from_top).strip()
                    print(page_no)
                    if (not page_no.replace(' ','')
                        or page_no.isnumeric()
                        or page_no in first_romans):
                        break
                    if query:
                        print(text)
                        print(DIVIDER)
                        page_no = input('Page no ?')
                        query = False
                        if page_no.isnumeric():
                            break
                    
                        
                    if not once_through:
                        query = True
                        from_top = not from_top
                        once_through = True
                if (page_no.isnumeric() and last_found_page
                    and last_found_page.isnumeric()
                    and int(page_no) == int(last_found_page)+1):
                    last_found_page = page_no
                else:
                    
                    print(text)
                    print(DIVIDER)
                    inp = input('Keep '+page_no+' or X to exclude PAGE ')
                    if not inp in YESTERMS + ['X']:
                        page_no = input('Enter new page number?')
                    if inp == 'X':
                        exclude = True
                    last_found_page = page_no
                    
                if first_page:
                    inp = input('Keep '+page_no+' or X to exclude PAGE ')
                    if not inp in YESTERMS + ['X']:
                        page_no = input('Enter new page number?')
                    if inp in 'X':
                        exclude = True
                    first_page = False
                    last_found_page = page_no
                
                if not exclude:
                    italic_pages.append(page_no)
                    
                    self.pages[page_no]=text
                    italics = ''
                    
                    

                    italic_found = False
                    for char in page.chars:
                        if char['fontname'] not in excluded_fonts:
                            self.all_text += char['text']

                                                
                            if 'Italic' in char['fontname']:
                                self.italicized_chars.add(position_at)
                                
                                if not italic_found and italics and italics[0].isupper():
                                    italics = italics.strip()
                                    if italics.endswith(')') and '(' in italics:
                                        italics = italics.split('(')[0].strip()                         
                                    self.italicized_phrases.add(italics)
                                    if italics not in self.italic_dict:    
                                        self.italic_dict[italics] = set()
                                    self.italic_dict[italics].add(page_no)
                                    if italics not in self.title_dict:
                                        self.title_dict[italics] = set()
                                    self.title_dict[italics].add(page_no)
                                    
                                    italics = char['text']
                                    italic_found = True 
                                else:
                                    italics += char['text']
                                    italic_found = True
                            else:
                                if italic_found and char['text'] not in string.whitespace:
                                    italic_found = False

                            if char['text'] == '(':
                                found_left_paren = True
                                
                            if char['text'] == '[':
                                found_left_bracket = True

                            if char['text'] == '“':
                                if not found_left_quote:
                                    found_left_quote = True

                                    
                                else:
                                    self.quoted_phrases.add(quoted_string)
                                    quoted_string = ''
                            
                            
                            if char['text'] in string.punctuation+string.whitespace:
                                if word in self.words:
                                    self.words[word].add(page_no)
                                    self.histio[word]+=1
                                    
                                else:
                                    self.words[word] = {page_no}
                                    self.histio[word] = 1

                                if word in self.words_in_sentences:
                                    self.words_in_sentences[word].add(sentence_count)
                                    
                                else:
                                    self.words_in_sentences[word] = {sentence_count}
                                    
                                    
                                    
                                if word:
                                    if ((word[0].islower() and last_capitalized)
                                        and (not italic_found or add_italic_caps)) :
                                        # To exclude the first word of a series of capital words
                                        # if it is either the first word of a sentence or has an apostrophe
                                        while capitalized_words:
        
                                            if ((capitalized_words and
                                                 capitalized_words[0]
                                                 in self.first_words) or
                                                (capitalized_words
                                                 and len(capitalized_words)>0
                                                 and capitalized_words[0].endswith("'s"))):
                                                capitalized_words = capitalized_words[1:]
                                            else:
                                                break
                                                
                                            
                                        if len(capitalized_words)>1:
                                            # join together capitalized words and add them to dictionary
                                            
                                            cap_phrase = ' '.join(capitalized_words)
                                            self.capitalized_phrases.add(cap_phrase)
                                            if cap_phrase in self.capital_histio:
                                                self.capital_histio[cap_phrase].add(page_no)
                                            else:
                                                self.capital_histio[cap_phrase] = {page_no}
                                                
                                            capitalized_words = []
                                            last_capitalized = False
                                        elif len(capitalized_words)>0:
                                            if not speller.unknown(set(capitalized_words[0].lower())):
                                                self.first_words.add(capitalized_words[0])
                                    if word[0].isupper() or word in NAME_WORDS:
                                        capitalized_words.append(word)
                                        last_capitalized = True
                                       
                                word = ''
                                if char['text'] in string.punctuation:
                                    capitalized_words = []
                                    last_capitalized = False
                                
                                    
                            else:
                                word+=char['text']
                            if char['text'] == '.':
                                last_not_alpha = True
                            if char['text'] not in string.whitespace+string.punctuation+'0123456789':
                                last_not_alpha = False

                            if char['text'] in ' ' and last_not_alpha:

                                sentence_string  += char['text']

                                self.sentence_record.append((sentence_starts_at,
                                                             position_at,
                                                             sentence_count))
                                self.sentence_dict[sentence_count] = (sentence_starts_at,
                                                                      position_at,','.join(sentence_pages))
                                self.sentences.add(sentence_string)                    
                                sentence_count += 1
                                sentence_pages = set()
                                sentence_string = ''
                                sentence_starts_at = position_at
                            else:
                                sentence_string  += char['text']
                                sentence_pages.add(page_no)
                            if found_left_paren:
                                paren_string += char['text']
                            if found_left_bracket:
                                
                                bracket_string += char['text']
                            if found_left_quote:
                                quoted_string += char['text']
                            

                            if found_left_paren and char['text'] == ')':
                                paren_string = paren_string[1:-1]
                                
                                self.parenthetical_phrases.add(paren_string)
                                if ',' in paren_string and is_date(paren_string.split(',')[-1]):
                                    paren_string = ','.join(paren_string.split(',')[0:-1])
                                    
                                if paren_string not in self.title_dict:
                                    self.title_dict[paren_string] = {page_no}
                                else:
                                    self.title_dict[paren_string].add(page_no)
                                
                               
                                found_left_paren = False
                                paren_string = ''
                            if found_left_bracket and char['text'] == ']':
                                bracket_string = bracket_string[1:-1]
                                self.brackets.add(bracket_string)
                                found_left_bracket = False
                                bracket_string = ''
                            if found_left_quote and char['text'] == '”':
                                quoted_string = quoted_string[1:-1]
                                self.quoted_phrases.add(quoted_string)
                                if quoted_string not in self.title_dict:
                                    self.title_dict[quoted_string] = set()
                                    self.title_dict[quoted_string].add(page_no)
                                found_left_quote = False
                                quoted_string = ''
          


                            position_at +=1
                    self.page_record.append((page_start,position_at,page_no))
                    self.page_dict[page_no]=(page_start,position_at)

    def print_section (self,from_point=0,to_point=0,italics=True,line_len=50):

        """Prints text from from_point to to_point.
        Line_len to determine the length of the line to be shown
        """

        

        text = self.all_text[from_point:to_point]
        return_text = ''
        line=''
        for char in text:
            if char == '\n':
                print(line)
                print()
                line = ''
            if len(line) > line_len:
                if char == ' ':
                    return_text += line + '\n'
                    line = ''
            line += char
        return_text += line
        return return_text
            
    def get_from (self,index,obj=None):

        """Used for printing a section of an object
        containing a collection of different ordered text
        segments, such as the dictionary of pages.
        """
        
        if obj==None:
            obj=self.page_dict

        if index in obj:
            from_point,to_point = obj[index][0],obj[index][1]
            return self.print_section(from_point,to_point)

    def get_page (self,page):

        """Returns the text of an entire page"""
        
        return self.get_from(page,obj=self.page_dict)
    def get_sentence (self,sentence):

        """The a sentence"""
        
        return self.get_from(sentence,obj=self.sentence_dict)
        
        
class Headings:

    """For establishing the titles of the index"""

    def __init__ (self,book_object=None):

        self.names = {'keep':set(),'purge':set(),'unprocessed':None}
        self.titles = {'keep':set(),'purge':set(),'ip':None,'qp':None,'pp1':None,'pp2':None}
        self.concepts = {'keep':set(),'purge':set()}
        self.book_object = book_object
        self.names_done = False
        self.titles_done = False
        self.italicized_phrases_done = False
        self.quoted_phrases_done = False
        self.paren_phrases1_done = False
        self.paren_phrases2_done = False 

    def get_names (self,name):

        """Takes a long name and divides it into its components
        """
        
        if ',' in name:
            last, first = name.split(',')[0].strip(),name.split(',')[1].strip()
        else:
            last, first = name.strip(),''
            
        return_names = set()
        for x in sorted(self.names['keep']):
            if ',' in x:
                if last in x.split(',')[0] and first in x.split(',')[1]:
                    return_names.add(x)
            else:
                if last in x:
                    return_names.add(x)
        return return_names 
                
            
            

    def divide_set (self,entry_set,before,after,add_to=False,queries='krmnaxy',obj_type=''):

        """
        Processes a set into various groups, and modifies forms of entries
        The basic format of an entry is:

        <AUTHOR>HEADING_SUBHEADING;SEARCH
        """

        return_keep = set()
        return_purge = set()
        input_phrase = ('RETURN to KEEP\n'*('k' in queries)+
                        'SPACE+RETURN to PURGE\n'*('r' in queries)+
                        '/ to MODIFY\n'*('m' in queries)+
                        '? to ADD SEARCH STRING\n'*('s' in queries)+
                        ': to CONVERT A NAME TO REGULAR FORM\n'*('n' in queries)+
                        '> to ADD AUTHOR\n'*('a' in queries)+
                        '_ to ADD SUBHEADINGS\n'*('x' in queries)+
                        '< to ADD AN ADDITIONAL HEADING\n'*('y' in queries)+
                        '^ to ADD A REFERENCE (see also)'*('z' in queries)+
                        'Q to QUIT\n')
        
        go_on = True
        returned_entry_set = copy.copy(entry_set)
        new_x = ''
        inp = ''
         
        
        for x in sorted(entry_set):

            if not inp == 'Q':
                returned_entry_set.discard(x)
 

            if add_to and not x.startswith(before):
                x = before+x
            if add_to and not x.endswith(after):
                x = x+after
            
            while go_on:

                print(before+after+'  '+x)
                print(input_phrase)
                inp = input('? ')


                
                if not inp and 'k' in queries:
                    return_keep.add(x)
                    print(x+' KEPT')
                    break

                elif inp == 'Q':
                    go_on = False                  
                
                elif inp == ' ' and 'r' in queries:
                    return_purge.add(x)
                    return_keep.discard(x)
                    print(x+' PURGED')
                    
                    break
                
                elif inp == '/' and 'm' in queries:
                    new = input(x)
                    if new:
                        new_x = new
                        
                elif inp == ';' and 's' in queries:
                    sh = input('ENTER SEARCHSTRING!')
                    if not input('\nRETURN TO ACCEPT\n'):
                        new_x = x+';;'+sh

                elif inp == '^' and 'z' in queries:
                    cross_reference = input('ENTER CROSSREFERENCE? ')
                    if input('ACCEPT '+cross_reference) in YESTERMS:
                        if ';;' in x:
                            new_x = x.split(';;')[0]+'['+cross_reference+']'+';;'+x.split(';;')[1]
                        
                elif inp == ':' and 'n' in queries:
                    final_name = ''
                    all_names = x.replace("'s",'').replace('’s','').split(' ')
                    standard_name = all_names[-1]+', '+' '.join(all_names[0:-1])
                    for counter, name in enumerate(all_names):
                        print(counter,name)
                    
                    order = input('\n\tINPUT NAME for example: 01,23; 1von 0\n\tor RETURN FOR '+standard_name)
                    if not order:
                        final_name = standard_name
                    else:
                        for char in order:
                            print(char)
                            if char in '01234567809' and int(char) < len(all_names):
                                final_name += all_names[int(char)]
                                final_name += ' '
            
                            elif char == ',':
                                final_name += ', '
                            elif char:
                                final_name += char
                        final_name = final_name.strip().replace('  ',' ').replace(' ,',',')
                    if not input('\n\tRETURN TO ACCEPT: '+final_name+'\n'):
                        new_x = final_name
                elif inp == '<' and 'y' in queries:
                    while True:
                        new_entry = input('\nENTER NEW HEAD ENTRY!')
                        if  new_entry and not input('RETURN TO ACCEPT'):
                            break
                    if new_entry:
                        return_keep.add(new_entry)
                elif inp == '>' and 'a' in queries:
                    name = input('Name of author for '+x+'\n')
                    possible_names = sorted(self.get_names (name))
                    for counter, pos_name in enumerate(possible_names):
                        print(counter,pos_name)
                    fulfilled = False
                    while True:
                        entered = input('ENTER NUMBER OR ? to ADD A NEW NAME')
                        if entered == '?':
                            while True:
                                new_name = input('ENTER NEW NAME!')
                                if new_name and not input('RETURN to ACCEPT!'):
                                    break
                            if new_name:
                                self.names['keep'].add(new_name)
                                new_x = '<'+new_name+'>'+x
                                break
                                
                               
                            
                        elif (entered.isnumeric() and
                              (int(entered) < len(possible_names))):
                            
                            if not input('RETURN TO KEEP: '+possible_names[int(entered)]):
                                new_x = '<'+possible_names[int(entered)]+'>'+x
                                break
                    
                elif inp == '_' and 'x' in queries:
                    while input('SPACE + RETURN to ENTER A SUBHEADING!'):
                        subheading = input('SUBHEADING?')
                        if not input('RETURN TO ACCEPT '+subheading):
                            if '[' in x:
                                head,body = x.split('[')
                                new_x = head+'_'+subheading+'['+body
                            elif ';;' in x:
                                head, body = x.split(';;')
                                new_x = head+'_'+subheading+';;'+body
                            else:
                                new_x = x+'_'+subheading

                if new_x and new_x != x and inp != '_':            
                    return_keep.add(new_x)
                    return_purge.add(x)
                    print(new_x+' ADDED')
                else:
                    if new_x and new_x != x:
                        return_keep.add(new_x)
                        print(new_x+' ADDED')
                    if inp != ':':
                        return_keep.add(x)
                        print(x+' KEPT')
                    else:
                        return_purge.add(x)
                        print(x +' PURGED')
                    
        if entry_set and not returned_entry_set and input('FINISH FIRST STAGE? ') in YESTERMS:
            if obj_type == 'n':
                self.names_done = True
            if obj_type == 'ip':
                self.italicized_phrases_done = True
            if obj_type == 'qp':
                self.quoted_phrases_done = True
            if obj_type == 'pp1':
                self.paren_phrases1_done = True
            if obj_type == 'pp2':
                self.paren_phrases2_done= True
                    
                
                
                    
                            
                            
        print('TO KEEP:',','.join(return_keep))
        print('TO PURGE:',','.join(return_purge))
        return return_keep, return_purge, returned_entry_set
        
    def add (self,entered_set,obj=None,before='',after='',add_to=False,queries='krmna',obj_type=''):

        """Divides the entered set and add the two parts into the set of terms to be kept,
        and the set of terms to be removed"""
        
        keep, discard,returned_entry_set = self.divide_set(entered_set,before,after,add_to,queries,obj_type=obj_type)
        obj['keep'].update(keep)
        obj['purge'].update(discard)
        if not obj_type or obj_type == 'n':
            obj['unprocessed'] = returned_entry_set
        else:
            obj[obj_type] = returned_entry_set
        return returned_entry_set

    def reform (self,obj=None,before='',after='',from_keep_to_purge=True,queries='kr'):

        """To revise a division that has already been made
        """

        if from_keep_to_purge:
            entered_set = obj['keep']
        else:
            entered_set = obj['purge']
        keep, discard, dummy = self.divide_set(entry_set=entered_set,
                                        before=before,
                                        after=after,
                                        add_to=False,
                                        queries=queries)
        print('keep',';'.join(keep))
        print('discard',';'.join(discard))
        if from_keep_to_purge:
            for x in discard:
                if x in obj['keep']:
                    obj['keep'].discard(x)
                    obj['purge'].add(x)
            for x in keep:
                print('keeping ',x)
                obj['keep'].add(x)
                
        else:
            for x in discard:
                if x in obj['purge']:
                    obj['purge'].discard(x)
                    obj['keep'].add(x)
                else:
                    obj['keep'].add(x)
              
                
    def run_reform (self,obj,
                    first_query='krmnxsyz',
                    second_query='kr',title=False,name=False):

        """Queries which of the "reformations" are to be made
        (from purge to keep, or keep to purge)
        and calls the reform function accordingly"""

 

        if obj['keep'] or obj['purge']:
            if input('REVISE? ') in YESTERMS:
                print(DIVIDER)
                print('REVISING FROM KEEP TO PURGE')
                print(DIVIDER)
                self.reform(obj,
                            before='',
                            after='',
                            from_keep_to_purge=True,
                            queries=first_query)
                print(DIVIDER)
                print('REVISING FROM PURGE TO KEEP')
                print(DIVIDER)
                self.reform(obj,
                            before='',
                            after='',
                            from_keep_to_purge=False,
                            queries=second_query)
            return True
        return False 

    def define_names (self):

        """Initiates the determination of the proper names
        that will be used in the index,
        or resumes the determination"""

        print('NAMES')

        if not self.names_done:

            if not self.names['unprocessed']:

                self.add(self.book_object.capitalized_phrases,
                         obj=self.names,
                         before='',
                         after='',
                         queries='krmnxsyz',
                         obj_type='n')
            else:
                self.add(self.names['unprocessed'],
                         obj=self.names,
                         before='',
                         after='',
                         queries='krmnxsyz',
                         obj_type='n')
                
            
        else:
            self.run_reform(self.names)

    def define_titles (self):

        """Initiates the determination of the titles
        that will be used in the index,
        or resumes the determination"""

        print('TITLES')       

        if not self.titles_done:
            
            print('________TITLES IN ITALICS_________')

            if not self.italicized_phrases_done:

                if self.titles['ip'] is None:
                    op_set = self.book_object.italicized_phrases
                else:
                    op_set = self.titles['ip']
                if not op_set:
                    self.italicized_phrases_done = True

                self.add({x for x in op_set
                        if (x[0].isupper() and some_letters(x))},
                       obj=self.titles,
                       before='/&it/',
                       after='/it$/',
                       add_to=True,
                       queries='krmaxsyz',
                       obj_type='ip')

                
            print('________TITLES IN QUOTATION MARKS_______')

            if not self.quoted_phrases_done:

                if self.titles['qp'] is None:
                    op_set = self.book_object.quoted_phrases
                else:
                    op_set = self.titles['qp']
                if not op_set:
                    self.quoted_phrases_done = True
                self.add({x for x in op_set
                          if (x[0].isupper() and len(x.split(' '))<max_title_length)},
                         obj=self.titles,
                         before='“',
                         after='”',
                         add_to=True,
                         queries='krmaxsyz',
                         obj_type='qp')
            print('_________TITLES IN PARENTHESES________')
            if not self.paren_phrases1_done:
                if self.titles['pp1'] is None:
                    op_set = self.book_object.parenthetical_phrases
                else:
                    op_set = self.titles['pp1']
                if not op_set:
                    self.paren_phrases1_done  = True 
                
                self.add({un_date(x) for x in op_set if (x[0].isupper() and ',' in x and not '“' in x and not '"' in x and last_is_date(x))},
                         obj=self.titles,
                         before='/&it/',
                         after='/it$/',
                         add_to=True,
                         queries='krmaxsyz',
                         obj_type='pp1')

            if not self.paren_phrases2_done:

                if self.titles['pp2'] is None:
                    op_set = self.book_object.parenthetical_phrases
                else:
                    op_set = self.titles['pp2']
                if not op_set:
                    self.paren_phrases2_done  = True 
                    
                
                self.add({un_date(x) for x in op_set if (x[0].isupper() and ',' in x
                                                         and ('“' in x or
                                                              '"' in x)
                                                         and last_is_date(x))},
                         obj=self.titles,
                         before='',
                         after='',
                         add_to=True,
                         queries='krmaxsyz',
                         obj_type='pp2')
            if (self.italicized_phrases_done and
                self.quoted_phrases_done and
                self.paren_phrases1_done and
                self.paren_phrases2_done):
                 self.titles_done = True 
        else:
            print('REFORM')
            print('T',self.titles)

            self.run_reform(self.titles,
                            first_query='krmaxsyz',
                            second_query='kr')
            

    def define_concepts (self):

        """Initiates the determination of the concepts
        that will be used in the index,
        or resumes the determination"""

        print('CONCEPTS')

        if not self.run_reform(self.concepts,
                               first_query='krmnxsz',
                               second_query='kr'):
            terms = self.book_object.nouns
            print(len(terms))
            terms = [x for x in terms if not x.isnumeric()]
            
            if input('Purge frequent?') in YESTERMS:
                
                terms = [x for x in terms if x not in English_frequent_words]
            print(len(terms))
            if input('Purge mispelled?') in YESTERMS:
                
                unknown = speller.unknown(terms)
                terms = [x for x in terms if x not in unknown]
            print(len(terms))
            if input('Pure capital words?') in YESTERMS:
                terms = [x for x in terms if not x[0].isupper()]
            
            while True:

                while True:
                    lower, upper = None, None

                    lower = input('LOWER THRESHOLD?')
                    if lower.isnumeric():
                        lower = int(lower)
                    upper = input('UPPER THRESHOLD?')
                    if upper.isnumeric():
                        upper = int(upper)
                    if lower and upper:
                        break
                terms = [x for x in terms if x in self.book_object.words and lower<=len(self.book_object.words[x])<=upper]
                print('There are '+str(len(terms))+' terms in your set')
                if input('Show?') in YESTERMS:
                    print(', '.join(terms))
                if input('Accept?') in YESTERMS:
                    break
            self.add(set(terms),
                     self.concepts,
                     queries='krmnx')
            if input('Add additional terms?') in YESTERMS:
                new_terms = [x.strip() for x in input('?').split(',')]
                print (', '.join(new_terms))
                if input('ADD to concepts?') in YESTERMS:
                    self.add(set(new_terms),
                             self.concepts,
                             queries='krmnxsz')
            
        
        
class Searcher:

    """Find headings in the interpreted PDF text
    """

    def __init__ (self,book_object=None):

        self.book_object = book_object

    

    def get_pages (self,term,dictionary_object=None):

        """Core search routine. Retrieves pages for the given term.
        """

        if term.startswith('~'):
            negative = True
            term = term[1:]
        else:
            negative = False
        result = set()

        if '/' in term:
            #to search for only the portion of a word to the left of the slash
                
            term = term.split('/')[0]
            all_terms = [x for x in dictionary_object.keys() if x.startswith(term)]
            return_pages = set()
            for term in all_terms:
                return_pages.update(dictionary_object[term])
            result = return_pages
                
        elif term in dictionary_object:
            result = dictionary_object[term]
            all_terms = [term]
        else:
            all_terms = []
            
        if negative:
            result = {x for x in self.book_object.pages.keys() if x not in result}
        return result, all_terms
        

    def search_entry(self,term,dictionary_object=None):

        """Interprets a search term and runs the search accordingly"""

        
        if '>' in term:
            term = term.split('>')[1]
        if ';;' in term:
            head, term = term.split(';;')[0], term.split(';;')[1]
            term = term.replace('%',head)
        term = term.replace('/&it/','').replace('/it$/','')
        x = self.search (term,dictionary_object=dictionary_object)
        return x[0],x[1]

    def search (self,search_phrase,dictionary_object):

        """Searches a complex search phrase
        ---allowing &=AND, |=OR, nested parentheses ---
        in the disctionary object.
        Uses the parser."""
        
        

        def get_terms (entry):

            """Extracts individual terms from search phrase"""

            for char in '()&|':
                entry = entry.replace(char,'[#]')
            all_terms = [x.strip() for x in entry.split('[#]') if x]
            return all_terms

        universe = {}

        all_terms = get_terms (search_phrase)
        parsed_phrase = parser.parse(search_phrase)
        found_terms = set()
        for term in all_terms:
            x = self.get_pages(term,dictionary_object=dictionary_object)
            universe[term] = x[0]
            found_terms.update(set(x[1]))
            
        result = parser.interpret(parsed_phrase,universe)
        return result, found_terms

class Index_Maker:

    """Basic class for making indexes, once the text has been interpreted, and
        the list of entries has been determined"""
    

    def __init__ (self):

        self.project_name = ''
        self.text_filename = ''
        self.project_file = None
        self.text_object = None 
        self.names = False
        self.titles = False
        self.concepts = False
        self.index = None
        self.index_name = ''
        self.index_made = False
        self.index_text = ''
        self.project_object = None
        self.searcher_object = None
        self.reverse_table = {}
        self.index = {'names':{},
                      'titles':{},
                      'concepts':{}}
        self.return_dict = {}
        self.override = False

    def reverse_index (self):

        """Reverses the index, such that the keys are pages,
        and the values are the indexed terms"""

        if self.index:

            for index_type in self.index:
                for entry in self.index[index_type]:
                    typed_entry = entry + ' ('+index_type+')'
                    for page in self.index[index_type][entry]:
                        if page not in self.reverse_table:
                            self.reverse_table[page] = {typed_entry}
                        else:
                            self.reverse_table[page].add(typed_entry)

    def input_term (self):

        menu = """
(0) LOAD TEXT %%
(1) OPEN PROJECT %
(2) SAVE PROJECT AS 
(3) SAVE PROJECT
(4) INITIATE PROJECT
(5) DEFINE NAMES %%%
(6) DEFINE TITLES %%%%
(7) DEFINE CONCEPTS %%%%%
(8) FIND PAGES %%%%%%
(9) DISPLAY INDEX
(10) DISPLAY ALL TERMS
(11) DISPLAY ALL PURGED TERMS
(12) FORMAT INDEX 
(13) EXAMINE PAGES
(14) CREATE REVERSE INDEX
(15) SHOW REVERSE INDEX
(16) CORRECT INDEX
(17) SAVE INDEX
(18) LOAD INDEX
(19) SAVE AS TEXT FILE 
(20) SEARCH TEXT BY PAGES
(21) SEARCH TEXT BY SENTENCES/ SHOW PAGES
(22) SEARCH TEXT BY SENTENCES/ SHOW SENTENCES
(23) OVERRIDE ERROR EXCEPTION
(24) RETURN INDEX
(25) QUIT

"""
      

        def reform_term (x,obj_name='names'):

            """Takes the entire index term,
            and returns the appropriate search phrases,
            which is either all the words of the term joined together with the "&"
            or is a separate search phrase. If the latter includes %%,
            then this is replaced with the AND-form of the regular term.

            e.g. Frog life;;(%%) | Toad

            => (Frog & Life) | Toad
            
            """

            search_phrase = None
            all_terms = []
            if ';;' in x:
                heading, search_phrase = x.split(';;')[0], x.split(';;')[1]
            else:
                heading = x
            if '>' in heading:
                heading = heading.split('>')[1]
            if '[' in heading:
                heading = heading.split('[')[0]
            if obj_name == 'names':
                if ',' in heading:
                    heading, body = heading.split(',')[0],heading.split(',')[1:]
                    all_terms = [heading] + body
            if not all_terms:
                if '_' in heading:
                    all_terms = [x for x in heading.split('_') if x]
                    heading = ' & '.join(all_terms)
                elif obj_name == 'names':
                    all_terms = [x for x in heading.split(' ') if x]
                    heading = ' & '.join(all_terms)
            if search_phrase:
                for char in '0123456789':
                    if char in search_phrase and int(char) < len(all_terms):
                        search_phrase = search_phrase.replace(char,all_terms[int(char)])
                if '%%' in search_phrase:
                    search_phrase = search_phrase.replace('%%',' & '.join(all_terms))
                heading = search_phrase
            if '/&it/' in heading or '/it$/' in heading:
                heading = heading.replace('/&it/','').replace('/it$/','')
            return heading 
            
        replace_term = '%%%%%%'
        for x in [self.index,
                  self.concepts,
                  self.titles,
                  self.names,
                  self.project_file,
                  self.text_object]:
            if x:
                menu = menu.replace(replace_term,'')
            else:
                menu = menu.replace(replace_term,'*')
            replace_term = replace_term[0:-1]
        print(menu)
        inp = input('?')

        def complete_file_name (x,first_ending='TXTOB',second_ending='.pkl'):

            """Adds the appropriate suffix to a file name"""
            
            if not x.endswith(first_ending+second_ending):
                if not x.endswith(second_ending):
                    if not x.endswith(first_ending):
                        x += first_ending+second_ending
                    else:
                        x += second_ending
                elif not first_ending in x:
                    x = x.replace(second_ending,
                                  first_ending+second_ending)
            return x

        def show_pages (page_list=None,sentences=False):

            """Shows pages in the index"""
            
            page_list_saved = page_list

            if not sentences:

                all_pages = self.text_object.pages.keys()
                roman_pages = [int_to_roman(x)
                               for x in sorted([rom_to_int(x) for x in all_pages
                                                if not x.isnumeric()])]
                italic_pages = [str(x) for x in sorted([int(x) for x in all_pages
                                                        if x.isnumeric()])]
                all_pages = roman_pages + italic_pages

            else:

                all_pages = sorted(list(self.text_object.sentence_dict.keys()))
                
            if not page_list:
                page_at = 0
            else:
                page_at = all_pages.index(page_list[0])
                page_list = page_list[1:]
            max_len = len(all_pages)

            def convert (x):

                """In x is the index of a sentence,
                it returns the corresponding page index"""

                if not sentences:
                    return x
                return self.text_object.sentence_dict[x][2]

            while all_pages:
                indexed_terms = {}
                if self.reverse_table:
                    if convert(all_pages[page_at]) in self.reverse_table:
                        indexed_terms = self.reverse_table[convert(all_pages[page_at])]
                if not sentences:
                    show_text = self.text_object.get_page(all_pages[page_at])
                else:
                    show_text = self.text_object.get_sentence(all_pages[page_at])
                words_from_terms = ' '.join(indexed_terms).replace('.','')
                for char in string.punctuation:
                    words_from_terms = words_from_terms.replace(char,' ')
                words_from_terms = [x for x in words_from_terms.split(' ')
                                    if x and x not in SMALL_WORDS]
                for word in words_from_terms:
                    show_text = show_text.replace(word,'<<'+word+'>>')\
                                .replace('<<<<','<<').replace('>>>>','>>')
                show_text = show_text.replace('>> <<',' ').replace('>><<','')
                
                
                print(DIVIDER+'\n'+str(all_pages[page_at])+'/'+convert(all_pages[page_at])+'\n'+DIVIDER+'\n'+show_text+'\n')
                if self.reverse_table:
                    if convert(all_pages[page_at]) in self.reverse_table:
                        print(','.join(indexed_terms))
                if not page_list and not page_list_saved:
                    inp =  input('<> PAGE # (Q)uit ')
                
                    if not inp:
                        page_at += 1
                    if inp == 'Q':
                        break
                    elif inp == '<':
                        page_at -= 1
                    elif inp == '>':
                        page_at += 1
                    elif inp in all_pages:
                        page_at = all_pages.index(inp)
                    elif page_at == max_len:
                        page_at = 0
                    elif page_at == -1:
                        page_at = max_len - 1
                else:
                    if not page_list:
                        page_list = page_list_saved
                    page_at = all_pages.index(page_list[0])
                    page_list = page_list[1:]
                    inp = input('ANY KEY to ADVANCE or (Q)uit')
                    if inp == 'Q':
                        break
                    
                    
        #FOR SELECTION THE ACTION CORRESPONDING TO THE INPUT 

        if inp in ['2','3']:

            #Save project, or save project as

            if not self.project_name or inp == '0':
                self.project_name = input('Name of file to save to? ')
                self.project_name = complete_file_name (self.project_name,first_ending='PROB')
                
            if (input('SAVE TO '+self.project_name)
                in ['yes','y','Y','Yes',' ']):
                if self.project_object:
                    self.project_file = open(directoryname+index_folder+self.project_name,'wb')
                    pickle.dump(self.project_object,
                                self.project_file)
                    self.project_file.close()
                    
                    
        elif inp == '1':

            #Open project
            
            self.project_name = input('Name of project to open? ')
            self.project_name = complete_file_name (self.project_name,first_ending='PROB')
            self.project_file = open(directoryname+index_folder+self.project_name,'rb')
            self.project_object = pickle.load(self.project_file)
            self.project_file.close()
            self.searcher_object = Searcher(self.text_object)

        elif inp == '0':

                if not self.text_object or input('Overwrite existing TEXT OBJECT?') in YESTERMS:

                    if input('Load existing TEXT OBJECT ') in YESTERMS:
                        self.text_filename = complete_file_name(input('Name of project to open?'))
                        tempfile = open(directoryname+index_folder+self.text_filename,'rb')
                        self.text_object = pickle.load(tempfile)
                        tempfile.close()

                    else:
                    
                        self.text_object = Reader()
                        pdf_filename = input('PDF TO READ? ')
                        self.text_object.load(pdf_filename)
                        if not input('SAVE as '+complete_file_name(pdf_filename)+'? ') in YESTERMS:
                            self.text_filename = complete_file_name(input('Save as? '))
                        else:
                            self.text_filename = complete_file_name(pdf_filename)
                        print(index_folder+self.text_filename)
                        tempfile = open(directoryname+index_folder+self.text_filename,'wb')
                        pickle.dump(self.text_object,tempfile)
                        tempfile.close()
                    if not self.project_object:
                        if input('Initiate new project? ') in YESTERMS:
                            self.project_object = Headings(self.text_object)
                            self.searcher_object = Searcher(self.text_object)

                    if not self.index:
                        if input('LOAD INDEX? ') in YESTERMS:
                            inp = input('INDEX NAME? ')
                            self.index_name = complete_file_name (inp,first_ending='IND')
                            tempfile = open(directoryname+index_folder+self.index_name,'rb')
                            self.index = pickle.load(tempfile)
                            tempfile.close()
                            
                            
                    
        elif inp == '4':

            if self.text_object:
                self.project_object = Headings(self.text_object)
                self.searcher_object = Searcher(self.text_object)
            else:
                print('YOU MUST FIRST LOAD TEXT BEFORE YOU CAN INITIATE A PROJECT!')

        elif inp == '5':
            if self.project_object:
                self.project_object.define_names()
                self.names = True
                
            else:
                print('NO PROJECT')
        elif inp == '6':
            if self.project_object:
                self.project_object.define_titles()
                self.titles = True 
            else:
                print('NO PROJECT')
        elif inp == '7':
            if self.project_object:
                self.project_object.define_concepts()
                self.concepts = True

        elif inp in ['20','21', '22']:

            if inp == '20':
                obj = self.text_object.words
            else:
                obj = self.text_object.words_in_sentences
            if not self.searcher_object:
                self.searcher_object = Searcher(self.text_object)
            search_term = input('SEARCH TERM: ')
            x = self.searcher_object.search_entry(search_term,obj)
            results,terms = x[0], x[1]
            if inp == '20':

                print('RESULTS: ',', '.join(sorted(results)))
            else:
                print('RESULTS: ',', '.join(sorted([str(x)+'/'+self.text_object.sentence_dict[x][2] for x in results])))
            print('TERMS: ',', '.join(terms))
            if results and input('SHOW? ') in YESTERMS:
                if inp == '21':
                    show_pages (sorted(list(self.text_object.get_pages_for_sentences(results))))
                elif inp == '22':
                    
                    show_pages (sorted(list(results)),sentences=True)
                else:
                    show_pages(sorted(list(results)))
            
                    
            

        elif inp == '8':
            
            object_dict = {'names':self.project_object.names['keep'],
                          'titles':self.project_object.titles['keep'],
                          'concepts':self.project_object.concepts['keep']}
            to_search_object = {'names':self.text_object.words,
                          'titles':self.text_object.title_dict,
                          'concepts':self.text_object.words}

            
            query = input('Query?') in YESTERMS

            for obj_name in self.index:
                if input('Create index for '+obj_name+'? ') in YESTERMS:
                    searching_set = object_dict[obj_name]
                    searching_object = to_search_object[obj_name]
                    searching_set = sorted(searching_set)
                    length_of_set = str(len(searching_set))
                    for counter,x in enumerate(searching_set):
                        print(str(counter)+'/'+length_of_set+' : '+x +'='+reform_term(x,obj_name=obj_name))
                        
                        
                        results = self.searcher_object.search_entry(reform_term(x,obj_name=obj_name),searching_object)[0]
                        
                        if query:
                            kept_results = set()
                            for page in results:
                                print(self.text_object.get_page(page))
                                print('_______________________________________________')
                                inp = input('RETURN to KEEP, BLANK+RETURN TO REJECT, Q to KEEP AND STOP QUERYING')
                                if inp == 'Q':
                                    query = False
                                    kept_results.add(page)
                                elif not inp:
                                    kept_results.add(page)
                                if not query:
                                    break
                            results = kept_results
                        self.index[obj_name][x] = set(results)

                    
                            
                                
        elif inp == '9':

            for counter, object_type in enumerate([self.project_object.names,
                                self.project_object.titles,
                                self.project_object.concepts]):

                heading = {0:'NAMES',
                           1:'TITLES',
                           2:'CONCEPTS'}[counter]

                print(DIVIDER)
                print(heading)
                print(DIVIDER)
                
                for counter2,term in enumerate(object_type['keep']):
                    print(str(counter2)+': '+term)
                
                print(DIVIDER)
                
                
            

##                for index_type in ['names','titles','concepts']:
##                    print(index_type)
##                    print('_______________________________')
##                    for counter, term in enumerate(self.index[index_type].keys()):
##
##                        print(str(counter)+': '+term+ ':' + ', '.join(sorted(self.index[index_type][term])))
##                    print()
##                    print()
                    
        elif inp == '12':

            result_list = []
            single_entry = ''
            last_first_element = ''
            def text_format (x):

                x = x.split(';;')[0]
                if '_' in x:
                    x = x.count('_')*'\t'+x.split('_')[-1]
                return x 

                

            all_entries = [x for x in list(self.index['names'].keys())+
                                    list(self.index['titles'].keys())+
                                    list(self.index['concepts'].keys())]
            type_list = ['N']*len(self.index['names'].keys())\
                        +['T']*len(self.index['titles'].keys())\
                        +['C']*len(self.index['concepts'].keys())

            index_entries = []
            for counter in range(len(all_entries)):
                index_entries.append((all_entries[counter],type_list[counter]))
            
                

            index_entries = sorted([(x[0],x[1]) for x in index_entries],
                                   key=lambda x: x[0].replace('<','').lower())
        
            
            
            for counter, full_entry in enumerate(index_entries):
                index_type = {'N':'names',
                              'T':'titles',
                              'C':'concepts'}[full_entry[1]]                    
                entry = full_entry[0]
                cross_reference = ''
                if '[' in entry and '[' in entry:
                    cross_reference = entry.split('[')[1].split(']')[0]
                    entry = entry.split('[')[0]+entry.split(']')[1]
                    
                first_element = entry.split('>')[0].split('_')[0].split('[')[0].split(';;')[0].replace('<','')
                
                if first_element != last_first_element:
                    result_list.append(single_entry[:-1])
                    single_entry = first_element+','
                    last_first_element = first_element
                else:
                    entry_copy = entry
                    second_element = entry_copy[len(first_element)+1:].split(';;')\
                                     [0].split('[')[0].replace('>','').replace('<','')
                    single_entry += second_element+",of:"
                    


                heading = text_format (entry)
                pages = self.index[index_type][entry]
                
                page_results = format_range(pages) +';'
                single_entry += page_results[0:-1]
                if cross_reference:
                    single_entry += '; see also '+cross_reference


            result_list.append(single_entry)
            single_entry = ''
            self.index_text = ('\n'.join(result_list))
            print(self.index_text)
            
                    
                         

        elif inp in ['10','11']:


            if inp == '10':
                file_type = 'keep'
            else:
                file_type = 'purge'
            def display (display_obj,heading=''):

                print(heading)
                print()
                for counter, x in enumerate(sorted(display_obj)):

                    print(counter,x)
                print('_______________________________')
                print()

            if self.project_object:

                display(self.project_object.names[file_type],'NAMES')
                display(self.project_object.titles[file_type],'TITLES')
                display(self.project_object.concepts[file_type],'CONCEPTS')

        elif inp in ['13']:

            show_pages()

            
        elif inp in ['14']:

            self.reverse_index()

        elif inp in ['15']:
    
            for page in self.reverse_table:
                print(page,':',','.join(self.reverse_table[page]))

        elif inp in ['16']:

            for index_type in self.index:

                print('REVIEWING '+index_type+'\n'+DIVIDER)
                for entry in self.index[index_type]:
                    inp = input('REVIEW OR (D)ELETE '+entry)
                    if inp == 'D':
                        del self.index[index_type][entry]
                        
                    elif inp in YESTERMS:
                        for page in sorted((self.index[index_type][entry])):
                            
                            show_text = self.text_object.get_page(page)
                            words_from_terms = entry
                            for char in string.punctuation:
                                words_from_terms = words_from_terms.replace(char,' ')
                            words_from_terms = [x for x in words_from_terms.split(' ') if x and x not in SMALL_WORDS]
                            for word in words_from_terms:
                                show_text = show_text.replace(word,'<<'+word+'>>').replace('<<<<','<<').replace('>>>>','>>')
                            show_text = show_text.replace('>> <<',' ').replace('>><<','')
                            print(DIVIDER+'\n'
                                  +'[['+page+']]'+'\n'
                                  +DIVIDER+'\n'
                                  +show_text+DIVIDER)
                            if input('REJECT?') in YESTERMS:
                                self.index[index_type][entry].remove(page)
                        inp = input('PAGES TO ADD?')
                        if inp:
                            pages = inp.split(',')
                            for p in pages:
                                if p in self.text_object.pages.keys():
                                    self.index[index_type][entry].add(page)
                        
        elif inp in ['17']:
            self.index_name = complete_file_name (self.project_name.replace('PROB','').replace('.pkl',''),first_ending='IND')
            name_inp = input('RETURN TO USE '+self.index_name+' AS FILENAME, OR ENTER NEW NAME? ')
            if len(name_inp) > 3:
                self.index_name =  complete_file_name (name_inp,first_ending='IND')
            
            if self.index_name and (input('SAVE TO '+self.index_name)in ['yes','y','Y','Yes',' ']):
                if self.project_object:
                    tempfile = open(directoryname+index_folder+self.index_name,'wb')
                    pickle.dump(self.index,tempfile)
                    tempfile.close()

        elif inp in ['18']:

            if input('LOAD INDEX? ') in YESTERMS:
                        inp = input('INDEX NAME? ')
                        self.index_name = complete_file_name (inp,first_ending='IND')
                        tempfile = open(directoryname+index_folder+self.index_name,'rb')
                        self.index = pickle.load(tempfile)
                        tempfile.close()

        elif inp in ['19']:
            if input('SAVE FINAL INDEX as TEXTFILE') in YESTERMS:
                filename = complete_file_name(self.project_name.replace('PROB','').replace('.pkl',''),
                                              first_ending='FIN',
                                              second_ending='.txt')
                while True:
                    if input('SAVE to '+filename+'? ') in YESTERMS:
                        break
                    else:
                        filename = complete_file_name(input('Filename? '),
                                                      first_ending='FIN',
                                                      second_ending='.txt')
                tempfile = open(directoryname+index_folder+filename,'w')
                tempfile.write(self.index_text)
                tempfile.close()
##        elif inp in ['25']:
##            if input('QUIT? ') in YESTERMS:
##                return False
        elif inp in ['23']:
            self.override = not self.override
            print('OVERRIDE ',{True:'ON',
                   False:'OFF'}[self.override])
        elif inp in ['25']:
            self.reverse_index()
            if input('Pages as indexes? ') in YESTERMS:
                page_as_index = True
            else:
                page_as_index = False
                
            def convert (x):

                if x.isnumeric():
                    return int(x)
                else:
                    return rom_to_int(x)-1000
                
            def uncovert (x):
                if x>=0:
                    return str(x)
                else:
                    return int_to_roman(x+1000)
                
                

            counter = 1
            for counter, page in enumerate(sorted([convert(x) for x in self.reverse_table.keys()])):
                page = uncovert(page)
                page_keys = self.reverse_table[page]
                if page.isnumeric():
                    if page_as_index:
                        page_index = 'b.'+str(page)
                    else:
                        page_keys.add('page@'+page)
                        page_index = 'c.'+str(counter)
                else:
                    if page_as_index:
                        page_index = 'a.'+str(rom_to_int(page))
                        
                    else:
                        page_index = 'c.'+str(counter)
                        page_keys.add('rpage@'+page)
                page_text = self.text_object.get_page(page).replace('.\n','%%%').replace('\n',' ').replace('%%%','\n')
                
                
                
                self.return_dict[page_index]={'keys':page_keys,
                                         'text':page_text}
            
##            for page in self.return_dict:
##                print(DIVIDER)
##                print(page)
##                print(', '.join(self.return_dict[page]['keys']))
##                print(DIVIDER)
##                print(self.return_dict[page]['text'])
##                input('?')
            if input ('Quit and return index? ') in YESTERMS:
                return False
            
            
            
        return True 
            
    def console (self):

        """To call up the console and initiate main loop"""
        
        
        while True:

            if self.override:
                try:
                    
                    if not self.input_term():
                        break
                    
                except:
                    pass
            else:
                if not self.input_term():
                        break
        if self.return_dict and input('Return index? ') in YESTERMS:
            return self.return_dict
        return {}
            
     

if __name__ == "__main__":

    my_indexes = Index_Maker()
    my_indexes.console()


        
    
            
        

        
        
