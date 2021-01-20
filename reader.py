###READER###

import pdfplumber


import os, string, simple_parser_mod as parser, sqlite3

from indexer import Reader, Searcher
from stack import Stack
from indexdisplay import IndexDisplay

from numbertools  import format_range, rom_to_int,\
     int_to_roman,de_range,de_range_numeric,abbreviate_range,convert_range

from indexconfiguration import SMALL_WORDS, BREAK_PHRASE, DIVIDER, ROWS_IN_PAGE
from itertools import cycle
from globalconstants import BOX_CHAR





def box (x):

    
    

    if isinstance(x,str):
        box_list = x.split('\n')
    else:
        box_list = list(x)
    max_len = max([len(l) for l in box_list])

    for index in range(len(box_list)):

        box_list[index] = BOX_CHAR['v']+box_list[index]+(max_len-len(box_list[index]))*' '+BOX_CHAR['v']
        

    top = BOX_CHAR['lu']+BOX_CHAR['h']*max_len+BOX_CHAR['ru']
    
    bottom = BOX_CHAR['ll']+BOX_CHAR['h']*max_len+BOX_CHAR['rl']
    
    return '\n'.join([top]+box_list+[bottom])

    
    
        

def sort_all_pages (all_pages):
    
        roman_pages = [int_to_roman(x)
                               for x in sorted([rom_to_int(x) for x in all_pages
                                                if not x.isnumeric()])]
        arabic_pages = [str(x) for x in sorted([int(x) for x in all_pages
                                                        if x.isnumeric()])]
        all_pages = roman_pages + arabic_pages
        return all_pages

def get_if(x,left=None,right=None,get_all=False):

    """Extracts the segment from a text surrounded by left and right.
    Returns extract, text"""

    if not get_all:

        if left and right:
            if left in x and right in x:
                return x.split(left)[1].split(right)[0].strip(),\
                       x.split(left)[0]+right.join(x.split(right)[1:])
            
            return '',x.strip()
    all_found = []
    if left and right:
        counter = 0
        while  counter < 10 and left in x and right in x:
            counter += 1 
            found, x = get_if(x,left,right,get_all=False)
            all_found.append(found)
        return list(set(all_found)), x
    return [],''




class Database:

    def __init__ (self,db_name='standard_database.db'):

        self.connection = sqlite3.connect('indexer'+'/'+db_name)
        self.cursor = self.connection.cursor()
        
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS books (
        book TEXT NOT NULL UNIQUE );
        """)

        self.cursor.executescript("""

        CREATE TABLE IF NOT EXISTS text (
        
        book TEXT NOT NULL,
        text TEXT NOT NULL DEFAULT '',
        UNIQUE (book)
        FOREIGN KEY (book) REFERENCES books (book) ON DELETE CASCADE
        );""")

        self.cursor.executescript("""

        CREATE TABLE IF NOT EXISTS pages (

        book TEXT NOT NULL,
        page TEXT NOT NULL,
        from_here INTEGER NOT NULL,
        to_there INTEGER NOT NULL,
        UNIQUE (book,page)
        FOREIGN KEY (book) REFERENCES books (book) ON DELETE CASCADE
        );""")

        self.cursor.executescript("""

        CREATE TABLE IF NOT EXISTS sentences (

        book TEXT NOT NULL,
        sentence INTEGER NOT NULL,
        from_here INTEGER NOT NULL,
        to_there INTEGER NOT NULL,
        UNIQUE (book,sentence)
        FOREIGN KEY (book) REFERENCES books (book) ON DELETE CASCADE
        );""")

        self.cursor.executescript ("""
        CREATE TABLE IF NOT EXISTS words (

        book TEXT NOT NULL,
        word TEXT NOT NULL,
        page TEXT NOT NULL,
        UNIQUE (book,word,page)
        FOREIGN KEY (book) REFERENCES books (book) ON DELETE CASCADE
        FOREIGN KEY (book, page) REFERENCES pages (book,page) ON DELETE CASCADE
        );""")

        self.cursor.executescript ("""
        CREATE TABLE IF NOT EXISTS words_sentences (

        book TEXT NOT NULL,
        word TEXT NOT NULL,
        sentence INTEGER NOT NULL,
        UNIQUE (book,word,sentence)
        FOREIGN KEY (book) REFERENCES books (book) ON DELETE CASCADE
        FOREIGN KEY (book, sentence) REFERENCES sentences (book,sentence) ON DELETE CASCADE
        );""")

        self.cursor.executescript ("""
        CREATE TABLE IF NOT EXISTS pages_for_sentences (

        book TEXT NOT NULL,
        sentence INTEGER NOT NULL,
        page TEXT NOT NULL,
        UNIQUE (book,sentence,page)
        FOREIGN KEY (book) REFERENCES books (book) ON DELETE CASCADE
        FOREIGN KEY (book, sentence) REFERENCES sentences (book,sentence) ON DELETE CASCADE
        FOREIGN KEY (book, page) REFERENCES pages (book,page) ON DELETE CASCADE
        );""")


        self.cursor.executescript ("""
        CREATE TABLE IF NOT EXISTS bookmarks (

        book TEXT NOT NULL,
        page TEXT NOT NULL,
        bookmark TEXT,
        UNIQUE (book,page)
        FOREIGN KEY (book) REFERENCES books (book) ON DELETE CASCADE
        );""")

        self.cursor.executescript ("""
        CREATE TABLE IF NOT EXISTS comments (

        book TEXT NOT NULL,
        page TEXT NOT NULL,
        comment TEXT,
        UNIQUE (book,page)
        FOREIGN KEY (book) REFERENCES books (book) ON DELETE CASCADE
        );""")


        


        

    def change (self,
                table_name=None,
                 entry_name_one=None,
                 entry_name_two=None,
                 entry_name_three=None,
                 one=None,
                 two=None,
                 three=None,
                 delete=False):


        if table_name and entry_name_one:

            if entry_name_one and one:

                if not two:

                    if not delete:

                        self.cursor.execute ("INSERT OR REPLACE INTO "
                                                   +table_name+'('+entry_name_one+') VALUES (?);',
                                                   (one,))

                    else:
                        self.cursor.execute("DELETE FROM "
                              +table_name+" WHERE "+entry_name_one+"=?;",
                              (one,))
                        
                elif entry_name_two and two:

                    if not three:

                        if not delete:

                            self.cursor.execute ("INSERT OR REPLACE INTO "
                                                       +table_name+'('+entry_name_one
                                                       +','+entry_name_two+') VALUES (?,?);',
                                                       (one,two,))
                            
                        else:

                            self.cursor.execute("DELETE FROM "
                              +table_name+" WHERE "+entry_name_one+"=? "+entry_name_two+"=?;",
                              (one,two,))
                                                   
                                            
                
                    elif three and entry_name_three:

                        if not delete:

                            self.cursor.execute ("INSERT OR REPLACE INTO "
                                                       +table_name+'('+entry_name_one
                                                       +','+entry_name_two
                                                       +','+entry_name_three+') VALUES (?,?,?);',
                                                       (one,two,three))
                        else:

                            
    
                            self.cursor.execute("DELETE FROM "
                              +table_name+" WHERE "+entry_name_one+"=? "+entry_name_two+"=?"
                                                +entry_name_three+"=?;",
                              (one,two,three,))
    def add_book (self,book_name):

        self.change(table_name='books',entry_name_one='book',one=book_name)
        self.connection.commit()
        
    def delete_book (self,book_name):

        self.change(table_name='books',entry_name_one='book',one=book_name,delete=True)
        self.connection.commit()

    def get_books (self):

        self.cursor.execute("SELECT * FROM "+
                            "books;")
        
        return [x[0] for x in self.cursor.fetchall()]

    def add_text(self,book_name,text):

        self.change(table_name='text',
                    entry_name_one='book',
                    entry_name_two='text',
                    one=book_name,
                    two=text)
        self.connection.commit()
    def get_text (self,book_name):

        self.cursor.execute("SELECT * FROM text WHERE book=?;",(book_name,))
        return self.cursor.fetchone()[1]

    def add_page (self,
                  book=None,
                  page=None,
                  from_here=None,
                  to_there=None):

        is_str = lambda x:isinstance(x,str)
        is_int = lambda x:isinstance(x,int)

        if book and page and from_here and to_there and is_str(page) and is_int(from_here) and is_int(to_there):

            self.cursor.execute ("INSERT OR REPLACE INTO pages (book,page,from_here,to_there) VALUES (?,?,?,?)",
                                 (book,page,from_here,to_there,))
            self.connection.commit()

    def add_sentence (self,
                  book=None,
                  sentence=None,
                  from_here=None,
                  to_there=None):

        is_str = lambda x:isinstance(x,str)
        is_int = lambda x:isinstance(x,int)

        if book and sentence and from_here and to_there and isinstance(sentence,int) and isinstance(from_here,int) and isinstance(to_there,int):

            self.cursor.execute ("INSERT OR REPLACE INTO sentences (book,sentence,from_here,to_there) VALUES (?,?,?,?)",
                                 (book,sentence,from_here,to_there,))
            self.connection.commit()

    def get_pages (self,book_name):

        self.cursor.execute("SELECT * FROM pages WHERE book=?;",(book_name,))
        return [x[1] for x in self.cursor.fetchall()]

    def get_page_range (self,book_name,page):
        self.cursor.execute("SELECT * FROM pages WHERE book=? AND page=?;",(book_name,page,))
        x = self.cursor.fetchone()
        if x:
            return (x[2],x[3],)
        else:
            return (0,0)

    def get_books_for_word (self,word):

        self.cursor.execute("SELECT * FROM words WHERE  word=?;",(word,))
        x = self.cursor.fetchall()
        return {y[0] for y in x}
        

    def get_pages_for_word (self,book_name,word):

        self.cursor.execute("SELECT * FROM words WHERE book=? AND word=?;",(book_name,word))
        x = self.cursor.fetchall()
        return {y[2] for y in x}

    def get_sentences_for_word (self,book_name,word):

        self.cursor.execute("SELECT * FROM words_sentences WHERE book=? AND word=?;",(book_name,word))
        x = self.cursor.fetchall()
        return {y[2] for y in x}

    def get_all_words (self):

        self.cursor.execute("SELECT * FROM words")
        x = self.cursor.fetchall()
        return set(y[1] for y in x)
        

    def add_word (self,
                  book=None,
                  word=None,
                  page=None):

        is_str = lambda x:isinstance(x,str)

        if is_str(book) and is_str(word) and is_str(page):

            self.change(table_name='words',
                        entry_name_one='book',
                        entry_name_two='word',
                        entry_name_three='page',
                        one=book,
                        two=word,
                        three=page)
            self.connection.commit()

    def add_word_sentence (self,
                  book=None,
                  word=None,
                  sentence=None):

        is_str = lambda x:isinstance(x,str)

        if is_str(book) and is_str(word) and isinstance(sentence,int):

            self.change(table_name='words_sentences',
                        entry_name_one='book',
                        entry_name_two='word',
                        entry_name_three='sentence',
                        one=book,
                        two=word,
                        three=sentence)
            self.connection.commit()

    def get_words (self,
                   book=None):

        if isinstance(book,str):

            self.cursor.execute("SELECT * FROM words WHERE book=?",(book,))
            return set([x[1] for x in self.cursor.fetchall()])

    def get_words_left_center_right (self,
                                     left='',
                                     center='',
                                     right=''):

        if isinstance(left,str) or isinstance(right,str) or isinstance(center,str):
            

            if left:

                self.cursor.execute("SELECT * FROM words WHERE word LIKE '?%'".replace('?',left))

            elif center:

                self.cursor.execute("SELECT * FROM words WHERE word LIKE '%?%'".replace('?',center))

            elif right:

                self.cursor.execute("SELECT * FROM words WHERE word LIKE '%?'".replace('?',right))

            result = self.cursor.fetchall()
            result = [x[1] for x in result]

            return list(set(result))

    def word_exists (self,
                     book,
                     word):
        
        self.cursor.execute("SELECT * FROM words WHERE book=? AND word=?",(book,word,))
        x = self.cursor.fetchone()
        if x:
            return True
        return False
    
    def get_sentences (self,
                   book=None):

        is_str = lambda x:isinstance(x,str)
        if is_str(book):

            self.cursor.execute("SELECT * FROM sentences WHERE book=?",(book,))
            return set([x[1] for x in self.cursor.fetchall()])

    def add_bookmark (self,
                      book='',
                      page=''):

        if book and page:
            

            self.cursor.execute ("INSERT OR REPLACE INTO bookmarks (book,page,bookmark) VALUES (?,?,?)",
                                 (book,page,'TRUE'))
        self.connection.commit()
        
    def delete_bookmark (self,
                      book='',
                      page=''):

        if book and page:
            

            self.cursor.execute ("DELETE FROM bookmarks WHERE book=? AND page=?",
                                 (book,page,))
        self.connection.commit()
    def bookmark_exists (self,
                         book='',
                         page=''):

        self.cursor.execute("SELECT * FROM bookmarks WHERE book=? AND page=?",(book,page,))
        x = self.cursor.fetchone()
        if x:
            return True
        return False

    def get_bookmarks (self,
                         book='',
                         page=''):

        self.cursor.execute("SELECT * FROM bookmarks WHERE book=?",(book,))
        x = self.cursor.fetchall()
        return [y[1] for y in x]

    def add_comment (self,
                      book='',
                      page='',
                      comment=''):

        if book and page and comment:
            

            self.cursor.execute ("INSERT OR REPLACE INTO comments (book,page,comment) VALUES (?,?,?)",
                                 (book,page,comment))
    
        self.connection.commit()
        
    def delete_comment (self,
                      book='',
                      page=''):

        if book and page:
            

            self.cursor.execute ("DELETE FROM comments WHERE book=? AND page=?",
                                 (book,page,))
        self.connection.commit()
    def comment_exists (self,
                         book='',
                         page=''):

        self.cursor.execute("SELECT * FROM comments WHERE book=? AND page=?",(book,page,))
        x = self.cursor.fetchone()
        if x:
            return True
        return False

    def get_comment (self,
                         book='',
                         page=''):

        self.cursor.execute("SELECT * FROM comments WHERE book=? AND page=?",(book,page))
        x = self.cursor.fetchone()
        if x:
            return x[-1]
        
        

        
        
def get_files_in_directory():

        allfiles = os.listdir('pdfs'+os.altsep)
        return [x for x in allfiles if x.endswith('.pdf')]


def type_input(prompt='',must_be=['Y','N',' '],truncate=True,upper=True,return_empty=True, alert=True):

    """For inputting limited to a selection of single letter values"""
    
    while True:
        x = input(prompt)
        if x and truncate:
            x = x[0]
        if x and upper:
            x = x.upper()
            
        if x in must_be or (not x and return_empty):
            return x
        elif alert:
            print('VALUE MUST BE '+','.join(must_be).replace(' ','BLANK')+',RETURN'*return_empty)
        

def yes_no_input(prompt=''):

    """For yes or no inputs"""

    return type_input(prompt) in [' ','Y']


class Displayer:

        def __init__ (self,database_object=None,text_object=None):

            self.database_object = database_object
            self.text_object = text_object
            


        def show_pages (self,page_list=None,terms=None,show_all=False,abridge=False,text_title='',notes=None):

            

            """Shows pages in the index"""

            


            if terms:
                indexed_terms = terms
            else:
                indexed_terms = set()

            return_pages = set()
            rejected = set()
            finished_page_stack = Stack()
            classifier_stack = Stack()

            if page_list:
                page_list_saved = list(page_list)
            else:
                page_list_saved = None
            px = self.database_object.get_pages(text_title)
            all_pages = sort_all_pages(px)

            page_list = [pl for pl in page_list if pl in all_pages]
            

               
            if not page_list:
                page_at = 0
            else:
                page_at = all_pages.index(page_list[0])
            max_len = len(all_pages)

            def bracket(text,terms):

                """Surrounds all terms in text with brackets..."""
                return_set = set()

                for word in terms:
                    if word in text:
                        text = text.replace(word,'<<'+word+'>>')\
                               .replace('<<<<','<<').replace('>>>>','>>')

                        return_set.add(word)
                        
                    
                text = text.replace('>> <<',' ').replace('>><<','')
                return text,return_set
            def side_marks (text,BM=''):

                """Adds sidemarks indicating found elements"""

                
                
                returnlines = []            

                for section in text.split(BREAK_PHRASE):

                    returnlines.append('')
                    
                    
                    lines = section.split('\n')
                    max_line_length = max([len(x) for x in lines])
                    for line in lines:
                        fragments,dummy = get_if(line,'<<','>>',True)
                        if '<<' in line:
                            line = BM+'  ===>>> ' + line + (max_line_length-len(line))*' '+'    <<'+','.join(fragments)+'>>'
                        else:
                            line = BM+'         ' + line
                        returnlines.append(line)
                return '\n'.join(returnlines)



            def convert (x):

                return x

##                """In x is the index of a sentence,
##                it returns the corresponding page index"""
##
##                if not sentences:
##                    return x
##                return self.text_object.sentence_dict[x][2]

            def get_dehyphenated (terms):

                return terms 
##
##                """Returns words that are found in the text with the hyphen removed"""
##                to_add = []
##                for x in terms:
##                    if x in self.text_object.dehyphenated:
##                        to_add.append(self.text_object.dehyphenated[x])
##                if isinstance(terms,list):
##                    return terms+to_add
##                return terms.union(set(to_add))

               

            BM = ''
            if page_list:
                page_iterator = cycle(sort_all_pages(page_list))
                go_on = True
                counter = 10
                while go_on:

                   
                    show_text = self.text_object.get_page(page_at,text_title)                    
                    
                    words_from_terms = ' '.join(indexed_terms).replace('.','')
                    
                    for char in string.punctuation:
                        words_from_terms = words_from_terms.replace(char,' ')
                    words_from_terms = [x for x in words_from_terms.split(' ')
                                        if x and x not in SMALL_WORDS and len(x)>4]

                    
                    if not words_from_terms and terms:
                        words_from_terms = terms
                     

                    words_from_terms = get_dehyphenated(words_from_terms)
                    
                    show_text,found_word_set = bracket(show_text,words_from_terms)
                    if page_at in self.database_object.get_bookmarks(text_title):
                            BM = '##'
                    else:
                            BM =  '  '
                    show_text = side_marks (show_text,BM)
                    if abridge:
                        show_text = abridge_page(show_text)
                    if len(show_text.split('\n'))<ROWS_IN_PAGE:
                        show_text += '\n'*(ROWS_IN_PAGE-len(show_text.split('\n')))
                    
                    display = IndexDisplay(columns=2,automatic=False,column_size=[(0,0),(20,40)])

                    


                    
                    print(DIVIDER+str(page_at)+'\n'+DIVIDER)
                    display.load(show_text,0)
                    
                    comment = self.database_object.get_comment(text_title,page_at)
                    if comment:
                        display.load(comment,1)
                    print(box(display.show()))
                    
                    
                    print('\n\n\n')
                    short_prompt = '< PAGE R B [] {} + Q >'
                    prompt = box("""RETURN FOR NEXT
<    MOVE     >
ENTER A NEW RANGE
A SINGLE PAGE
(R)eset 
(B)ookmarks
[ to BOOKMARK
] to UNBOOKMARK
{ to COMMENT
} to UNCOMMENT 
+ TO ADD NOTE   
(Q)uit""")
                    
                    if counter >0:
                        inp = input(prompt)
                    else:
                        inp = input(short_prompt)

                    if counter >0:

                        counter -= 1
                    
                    
                    
                    if not inp:
                        page_at = next(page_iterator)
                                    
                    else:
                        if inp[0] == '>':
                            for xx in range(0,len(inp)):
                                page_at = next(page_iterator)
                        elif inp[0] == '<':
                            for xx in range(0,len(page_list)-len(inp)):
                                page_at = next(page_iterator)
                        elif inp == 'Q':
                            go_on = False
                        elif inp == 'R':
                            page_iterator = cycle(sort_all_pages(page_list))
                        elif inp == 'B':
                            bookmarks = self.database_object.get_bookmarks(text_title,page_at)
                            print(bookmarks)
                            bookmarks = sort_all_pages(bookmarks)
                            page_iterator = cycle(bookmarks)
                            
                            print('ITERATING OVER ',','.join(format_range(bookmarks)))
                          
                        
                        elif inp[0] == '[':
                            self.database_object.add_bookmark(text_title,page_at)

                        elif inp[0] == ']':
                            self.database_object.delete_bookmark(text_title,page_at)
                        elif inp[0] == '{':
                            existing_comment = self.database_object.get_comment(text_title,page_at)
                            if existing_comment:
                                inp2 = input('REPLACE or ADD or RETURN to QUIT')
                                if inp2:
                                    newcomment = input ('?')
                                    if inp2 == 'R':
                                        existing_comment = newcomment
                                    else:
                                        existing_comment + '\n' + newcomment
                                    self.database_object.add_comment(text_title,page_at,existing_comment.replace('|','\n'))
                            else:
                                newcomment = input ('?')
                                self.database_object.add_comment(text_title,page_at,newcomment.replace('|','\n'))
                        elif inp[0] == '}':
                            if input('ARE YOU SURE?') in ['Yes',' ','y','Y']:
                                self.database_object.delete_comment(text_title,page_at)
                        elif inp[0] == '+':
                            keys = {'page@'+page_at,'text@'+text_title.replace('.pdf','').replace('.','_')}
                            text = show_text
                            if self.database_object.comment_exists(text_title, page_at):
                                text += '/BREAK/'+self.database_object.get_comment(text_title, page_at)
                            notes.add((keys,text,))
                            
                        elif  '-' not in inp:
                            if inp in page_list:
                                while page_at != inp:
                                    page_at = next(page_iterator)
                        else:
                            new_list = [x for x in sort_all_pages(de_range(inp)) if x in page_list]
                            print('ITERATING OVER ',','.join(format_range(new_list)))
                            page_iterator = cycle(new_list)                     
                        
            return notes              
                            

class Console:

        
        


        def __init__ (self):

                self.all_books = []
                self.search_over = []
                self.notes = Stack()
                self.search_results = {}

        def get_page_range_local (self,book):

            return format_range(sort_all_pages(self.DB.get_pages(book)))

        def show_directory (self):

                all_files = get_files_in_directory()
                existing_files = self.DB.get_books()

                print_list = []
                for counter,x in enumerate(all_files):

                    print_list.append(str(counter)+':'+x+'<LOADED>'*((x[:-4] in existing_files)
                                                                     or x in existing_files)+self.get_page_range_local(x))
                print(box('\n'.join(print_list)))
                return all_files 
        
        def load (self,files_to_load):

                for pdf_filename in files_to_load:
        
                    self.text_object.load(filename=pdf_filename,
                                          text_title=pdf_filename)
                    print(pdf_filename,'LOADED')
            
        def select_files_to_load (self,all_files=None):

             
            

            all_files = self.show_directory()
            while True:
                choose = input(box('? WHICH FILES DO YOU WANT TO LOAD? GIVE A RANGE OF NUMBERS?  '))
                if not choose:
                    break
                try:
                    choose=[x for x in de_range_numeric(choose)]
                except:
                    print(box('INVALID ENTRY!'))
                if choose:
                    break
            files_to_load = []

            
            if choose:
                above = yes_no_input('?Find pages above?  ')
                below = not above or yes_no_input('?Find pages below?  ')
                self.text_object.above = above
                self.text_object.below = below 
            for x in choose:
                files_to_load.append(all_files[x])
            print('TO LOAD:','\n'.join(files_to_load))
            self.load(files_to_load)

        def display_search(self,r):

            r_dict = {}

            ID = IndexDisplay(columns=4,automatic=True,column_size = ((0,3),(10,30),(20,60),(10,30)))

            for counter, t in enumerate(r[0]):
                if t in r[1]:
                        row = []
                        row.append(str(counter))
                        row.append(t)
                        row.append(', '.join(sort_all_pages(r[0][t])))
                        row.append(', '.join(sorted(r[1][t],key=lambda x:x.upper())))
                        ID.load_multiple_columns(row)
        
                  
                        r_dict[counter]=t
            ID.load_multi()
            print(box((ID.show())))
            return r_dict

        def display_search_dict (self,entry_dict=None):
            ID = IndexDisplay (columns=4,automatic=True,column_size=((0,3),(10,30),(30,50),(40,60)))

            
            

            for counter,r in enumerate(entry_dict):
                row = []
                
                row.append(str(counter))
                row.append(entry_dict[r][0])
                result_summary = ''
                
                for x in entry_dict[r][1][0]:
                    
                    if not entry_dict[r][1][0][x]:
                        result_summary += '0'
                    elif 0<len(entry_dict[r][1][0][x])<10:
                        result_summary += str(len(entry_dict[r][1][0][x]))
                    else:
                        result_summary += 'X'
                found_terms = set()
                row.append(result_summary)
                for x in entry_dict[r][1][1]:
                    found_terms = found_terms.union(entry_dict[r][1][1][x])
                row.append(', '.join(found_terms))
                
                
                    
                
                ID.load_multiple_columns(row)
            ID.load_multi()
            print(box((ID.show())))
            while True:
                inp = input((box('SHOW SEARCH?')))
                if inp.isnumeric() and 0<=int(inp)<len(entry_dict):
                    self.display_search (entry_dict[int(inp)][1])
                if not inp:
                    break


        def get_search (self):

            go_on = True
            search_over = [t for t in self.DB.get_books()]
            all_books = [x for x in self.DB.get_books()]

            while go_on:

                    def show_list(l):
                        print_list = []

                        for counter,x in enumerate(l):
                                print_list.append(str(counter)+' : '+x)
                        return '\n'.join(print_list)
                    
                            

                    print(box(show_list(search_over)))
                    inp = input(box('RETURN to SEARCH; X to CHANGE SEARCH DOMAIN; Q TO QUIT   '))
                    print()
                    if not inp:
                    

                            to_search = input('?')
                            if to_search.startswith('$'):
                                    to_search = to_search[1:]
                                    sentence_search = True
                            else:
                                    sentence_search = False

                             
                            
                            r = self.searcher_object.search_entry(to_search,database_object=self.DB,text_title=search_over,sentence_search=sentence_search)
                            r_dict = self.display_search(r)

                            ID = IndexDisplay(columns=4,automatic=True,column_size = ((0,3),(10,30),(20,60),(10,30)))
                            

                            inp2 = input(box('SHOW? SPACE FOR ALL, RETURN FOR NONE   '))
                            print()

                            self.search_results[len(self.search_results.keys())] = (to_search,r)
                            
                            to_show = []
                            if inp2 == ' ':
                                    to_show = [t for t in r[1]]
                            elif inp2:                   
                                    to_show = [search_over[x] for x in de_range_numeric(inp2) if search_over[x] in r[0]]
                                    
                            for t in to_show:
                                    print('__________________________________________')
                                    print(t)
                                    print('__________________________________________')
                                    self.DS.show_pages(page_list=sort_all_pages(r[0][t]),terms=set(r[1][t]),show_all=False,abridge=False,text_title=t)
                    elif inp[0].upper() == 'X':

                            print('CURRENT DOMAIN')
                            show_list(search_over)
                            print()
                            print('ALL BOOKS')
                            show_list(all_books)
                            print()
                            inp2 = input(box('DEFINE NEW DOMAIN! SPACE FOR ALL, RETURN FOR NONE    '))
                            print()
                            
                            search_over = []
                            if inp2 == ' ':
                                    search_over = [t for t in all_books]
                            elif inp2:
                                    
                                    search_over = [all_books[x] for x in de_range_numeric(inp2) if 0<=x<len(all_books)]
                                                                                                           
                    elif inp[0].upper() == 'Q':
                        go_on = False

        def browse (self):

            all_books = [x for x in self.DB.get_books()]
            
            while True:
                print_list = []
                for counter,x in enumerate(all_books):
                    
                    print_list.append(str(counter)+':'+x+self.get_page_range_local(x))
                print(box('\n'.join(print_list)))
                inp = input ('Number of text to BROWSE, or (Q)uit ')   
                if inp.isnumeric() and 0<=int(inp)<len(all_books):
                    notes = self.DS.show_pages(page_list=sort_all_pages(self.DB.get_pages(all_books[int(inp)])),show_all=False,abridge=False,text_title=all_books[int(inp)],notes=self.notes)
                if inp and inp.upper()[0] == 'Q':
                    break

        def main_menu (self):

            go_on = True
            while go_on:

                print(box("""L(oad)into SEARCHER
S(earch) 
B(rowse)
H(elp)
V(iew) search log
Q(uit) """))

                inp = input('? ')
                if inp:
                    inp = inp.upper()[0]
                if inp == 'L':
                    self.select_files_to_load()
                elif inp == 'S':
                    self.get_search()
                elif inp == 'B':
                    self.browse()
                elif inp == 'V':
                    self.display_search_dict(self.search_results)
                elif inp == 'Q':
                    go_on = False

        
        def run(self):
            self.DB = Database()

            self.text_object = Reader(database_object=self.DB,
                                      in_italics=False,
                                      in_quotes=False,
                                      in_parens=False,
                                      in_caps=False,
                                      all_sentences=True,
                                      above=None,
                                      below=None)


            self.DS = Displayer (database_object=self.DB,text_object=self.text_object)

            self.searcher_object = Searcher ()
            
            self.main_menu()
            return self.notes
        
if __name__ == "__main__":
    
    C = Console()
    C.run()
        















        


                                 

            

        

    
        
    
       
        
        
