### Class for managing the automatic tutorial

from display import Display
from globalconstants import ENTERSCRIPT, FORMATTINGSCRIPT, SEARCHSCRIPT


display = Display()
class TutorialManager:

     """Basic class for managing tutorial scripts
     Turorials are loaded in to the dictionary under different headers;
     when a tutorial is added to an existing header, then it is appended
     to the list; Going through the tutorials removes them from the list
     """

     def __init__ (self):

          self.tutorials = {}
          self.activated = False

     def add (self,header,body):

          """To add a tutorial"""

          if header in self.tutorials:
               self.tutorials[header]['message'].append(body)
               self.tutorials[header]['status'] = True
          else:
               
               self.tutorials[header] = {'message':[body],
                                         'status':True}

     def show(self,header):

          """To show a tutorial"""
          
          if self.activated and header in self.tutorials and self.tutorials[header]['status'] and self.tutorials[header]['message']:

               if '/**/' in self.tutorials[header]['message'][0]:
                    title, body = 'TUTORIAL:  '+self.tutorials[header]['message'][0].split('/**/')[0],self.tutorials[header]['message'][0].split('/**/')[1]
               else:
                    title = 'TUTORIAL:  '+header+'!'
                    body = self.tutorials[header]['message'][0]
               if '┃' not in self.tutorials[header]['message'][0]:
                    display.noteprint((title,body),param_width=75,override=True)
               else:
                    print(body)
               entry = input('PLUS+RETURN for advance, PLUS+PLUS+RETURN to show next \n'
                             *(len(self.tutorials[header]['message'])>1)
                             +'SPACE+RETURN to stop showing this message, '
                             +'SPACE+SPACE+RETURN to quit tutorial, \n or MINUS+RETURN to SHOW TUTORIAL MENU  ')
               if entry == ' ':
                    self.tutorials[header]['status'] = False
               elif entry == '-':
                    self.all_tutorials()
               elif entry == '  ':
                    self.activated = False
               elif entry == '+':
                    self.tutorials[header]['message'] = self.tutorials[header]['message'][1:]
               elif entry == '++':
                    self.tutorials[header]['message'] = self.tutorials[header]['message'][1:]
                    self.show(header)
     def all_tutorials(self):

          
          
          while True:
               header_text = ''
               headers = list(reversed(sorted([h for h in list(self.tutorials.keys())
                                               if len(self.tutorials[h]['message'])>0],
                                              key=lambda x:len(self.tutorials[x]['message']))))
               for counter, x in enumerate(headers):
                    header_text += '('+str(counter+1)+') '+headers[counter]+'\n'
               display.noteprint(('TUTORIALS',header_text))
               x = input('ENTER THE NUMBER OF THE TUTORIAL TO BEGIN, Q TO QUIT, \n OR R TO RESTORE TUTORIALS ')
               if x.upper() == 'Q':
                    break
               elif x.upper() == 'R':
                    self.tutorials = {}
                    self.load()
                    display.noteprint(('TUTORIALS RESTORED',''))
               elif x.isnumeric() and 0<int(x)<len(headers)+1:
                    self.show(headers[int(x)-1])
          
               
               
     def start(self):

          """To start the tutorial"""
          
          self.activated = True
     def stop(self):

          """To stop the tutorial"""
          
          self.activated = False

     def load(self):

          """The load all the totorials into the dictionary"""
          
          self.add('INITIATE',
                   'Welcome to ARCADES /**/'\
                   +'To enter a note, type "enter"\n'\
                   +'To cycle through notes, press RETURN\n'\
                   +'To show all notes, type "all"\n'\
                   +'To search, type "search"\n'\
                   +'To see all commands, type "help"')

          self.add('INITIATE',"THE COMMAND PROMPT /**/"+\
                    "The command prompt displays essential"+
                   "information about the status of the notebook,"+
                   "including the name of the current notebook and project,"+
                   "the current index, the automatic prefix added to entered"+
                   " indexes, a <#> if the current note has been marked, "+
                   "and [++] or [+++] to indicate if the"+
                   " continuous entry mode is on."+
                   "\nThe format of the command prompt is as follows,"+
                   " with optional information underlined and in italics:\n"+
                   "NOTEBOOK/PROJECT: CURRENTINDEX #MARKED INDEXPREFIX CONMODE")

          
          self.add('INITIATE',
                   """
COMMAND SYNTAX /**/ 
     A basic command consists in one or more command phrases.

     If there are multiple command phrases, each command phrase is separated by a double SLASH.
     (1) defaultnotebook:4017.1.12 4017 +//delete:5//quit
     | Adds a new note, deletes note at index 5,
       and quits the notebook.

     To repeat a command N times, add **N at the end of the command, preceded by a space

       """)

          self.add('INITIATE',
                   """
VALUES_FOR_COMMANDS/**/
     Values can consist in 1) an integer 2) a string 3) a single index 4) multiple indexes.
     If values are essential to the execution of a command, ARCADES will query the user for values that have been omitted from the command phrase.
     A value, if not the last in the series, can be left empty. 
     Multiple indexes may be listed either through a range indicated by a DASH (e.g. 1.1-1.9.8;-1-50,-10--5),
     a succession of single values separated by commas, (e.g. 1,2,3.1,5,8), or a combination of an arbitrary number of ranges and single values separated by commas. (e.g., 1,4-6,9-10,11.1-14,19).
     Values need not be entered in ascending order, though in most instances the order of entry is of no consequence.""")

          
          self.add('INITIATE',
                   """
THE_COMMAND_PHRASE/**/
     The command phrase consists in a command and, optionally, predicate, in which case the command and the predicate are separated by a COLON. 
     The predicate consists in the following elements: values, limits, and modifiers.          
     These are combined as follows:
     COMMAND:VALUE1;VALUE2;VALUE3 MODIFIERS LIMITS
     The values are listed immediately after the COLON following the command. If there is more than one value, the values are separated by SEMICOLONS.
     A SPACE is placed at the end of the sequence of values. All the other elements are placed after the values, and are separated by SPACES.
""")


          
          self.add('KEYWORDS',
                   """
ENTERING_KEYWORDS/**/
     Enter a list of keywords separated by COMMAS.KEYWORDS can consists \n in a single word or phrase.
     TO ADD TAGS, use the slash (/) \ntogether with a list of terms (words or phrases) \nseparated by a PERIOD.
     For a sequence keywords:
     KEYWORD@INTERGERorFLOAT
     KEYWWORD@#DATE
     KEYWORD@_INDEX""")

          self.add('KEYWORDS',
                   """
TAGS/**/
     Keywords can be followed with one or more tags, serving as a further level of classification.
     The tags should follow a slash (/); multiple tags are separated by a period.
     So for example:

     Sloth/animal
     Penguin/bird.Arctic.flightless.monochrome
     Emu/bird.Australian.flightless.

     Searching for the tag “flightless” would retrieve notes with the tags “Penguin” and “Emu.”
     A given tag need only be associated once with a give keyword. Or, put another way, if you search for a tag it will retrieve all the notes classified with the keywords associated with it, and not just those notes in which the association has been made explicit. """)

          self.add('KEYWORDS',
                   """
KNOWLEDGEBASES/**/
     ARCADES includes two knowledgebases. The first allows for tags to be classified under higherorder concepts.
     A single tag can be classified under an arbitrary number of different concepts, and an arbitrary number of levels of classification are permitted, allowing for complex ontological trees to be superimposed atop the notes.
     While knowledge may be imputed, along with keywords and tags, when entering a note, it is also possible to manipulate the knowledgebase directly discreet commands or through a special console.

     Concepts to be learned are introduced with an EQUAL (=) following either a tag, or a subordinate concept.

     For example:
     Lupu/frog=amphibian=vertebrate=animal=living being=being

     ARCADES does not forbid circular assignments, such as, for example:
     Lupu/animal=creature, Girin/creature=animal.

     It will automatically stop rather than crash.

     The second knowledgebase is used for defining directed and non-directed relations – such as the relation “child of”, “parent of”, “teacher of”, or “friend of” – between keywords. 
""")
          self.add('KEYWORDS',
                   """
LINKING_NOTES/**/
     If the index of a note in the notebook is entered as a keyword, it automatically becomes a link, establishing a connection between the note in which it was entered as a keyword and the note to which it refers.
     Links are unidirectional; they point one note to another note. ARCADES keeps track of these indexes, and automatically changes them when the note to which they refer has been changed. """)

          self.add('KEYWORDS',
                   """
DEFAULT_KEYS/**/
     If you are entering a series of notes on the same topic, you may set default keywords which will be automatically added to the note.
     The default keywords are displayed before the command prompt.
     To add default keys, use addkeys; to add a single key, use "addkey", to delete the most recently added key, use "deletekey"; to clear all defaultkeys, use "clearkeys"; and to revise the default keys, deleting a selection and then adding new keys,
     use "deletedefaultkeys". The default keys are stored as a list, not a set: it is possible to have redundancies, though these will be eliminated when the keywords are added to a note, since the keywords of a note are stored as a set.""")
          

          self.add('KEYWORDS',
                   """
     The command "keysfortags" shows tags together with their keys.""")

          
          self.add('ESCAPE',
               """
ESCAPE_CODE/**/
PRESS / to go back to cycling through notes.""")
          

          self.add('CONESCAPE',
                   """
'CONESCAPE/**/
PRESS ;; to exit from CONCHILD or CONNEXT""")

          self.add('SEARCH',
                   SEARCHSCRIPT)

          self.add('FORMATTING',
                   FORMATTINGSCRIPT)

          self.add('FORMATTING',
                   """
FORMATTING INTO COLUMNS/**/
     ARCADES permits formatting into columns.
     A series of columns is initiated with “/COL/” and terminated with “/ENDCOL/”.
     Each line of text is divided up using an underline (_) to distinguish columns.
     Keep in mind that an EOL mark must be included at the end of each row.
     It is recommended, therefore, to enter columns in the poetry mode (see 2.3.2.1.2.1.2.), since thisautomatically adds an EOL after each entered line.""")

          self.add('FORMATTING',
                   """
SPLITTING A NOTE/**/
     An alternative---and perhaps easier---way of entering columns is to initiate the columns with “/SPLIT/”, terminate with “/ENDSPLIT/”, and separate the text of the individual columns with “/M/”.
     Notice that the formatting is a bit different than with the columns. Splits is recommended for larger sections of text.""")

          self.add('FORMATTING',
                   """
INSPECTING_A_NOTE/**/It is possible to inspect the entered text of a note to see how it appears without formatting.
     To do this, use the inspect command, followed by the index of the note to be inspected.""")

          self.add('FORMATTING',
                   """
COLUMNATING_AN_EXISTING_NOTE/**/
     The command "column" (alternative form: "col") is used to convert a regular note into a note with columns.
     It can also be used to remove columns.
     The columns command accepts two values, and the modifiers /$, /&, and /*.
     The first value is the collection of indexes to convert to columns, while the second value is the character that is to be converted into the underline (_) mark distinguishing columns across the line.
     The modifier /$ can be selected to undo columns while /& adds counters, and /* adds counters without converting to columns.

""")
          self.add('FORMATTING',
                   """
SIDENOTES/**/
     The command "sidenote" can be used to take a collection of indexes and merges them together as a series of columns.
     It accepts two values, and the single modifier /$.
     The first value indicates a collection of indexes, and the second value the width of the columns.
     The modifier /$ is used to add counters.
""")


          self.add('ENTERING',
                   ENTERSCRIPT)

          self.add('INITIATE',
                   """
INDEXES/**/
     Indexes consist in an integer followed by a sequence of natural numbers.

     For example: 1, 2, 1.1, 1.2, 2000, 2000.200.12, -1, -50.1.60, 0, 0.1.2

     The following commands initiate note entry:
     ent, enter, +
       | To enter a regular note in the
       | next available position.
     enternext, ++
       | To enter the sibling of the last note.
     ent, enter, + /$
       | To enter a sibling of the last note
     ent, enter, + /&
       | To enter a child of the last note
     enterchild, +++
       | To enter the child of the last note
     enterback, -
       | To enter a sibling of the
       | parent of the last note
""")

          self.add('INITIATE',
                   """
ABBREVIATED_INDEX_FORM/**/
     Very long indexes, with multiple repeated values, will appear, and can be entered, in an abbreviated form.
     Please observe, however, that the long form of the index is always used internally.
     1.1.1.1.1.1 ≈ 1^6
     1.1.1.2.1.1 ≈ 1^3.2.1^2
     7.7.7.7.7.7.7.6.6.6.6.6.6.5.5.5.5.5.5.4.4.4.4.3.3.3.3.2.2.
     ≈ 7^7.6^6.5^5.4^4.3^3.2^2.1
""")

          self.add('INITIATE',
                   """
ORDER_OF_INDEXES/**/
     ARCADES does not require that notes be assigned to sequential indexes.
     It is perfectly acceptable to have a notebook consisting of the indexes 1, 13, 1999, or, say, only of indexes with prime numbers.
     And it is also perfectly acceptable to have orphans – notes without a parent.
     Nevertheless, unless you opt to assign the index manually when entering new notes, ARCADES will automatically assign the index value.
     The basic entry function (+) will assign the new note either to the closest sibling of a “top-level” note, or to the closest mate of a note with size > 0. For example: 1 => 2; 2.1 => 3.
     The “next” entry function (++) will assign the new note to the soulsister, or closest available sibling, of the last note.
     For example: 1 => 2, 2.1 = 2.2, 3.3.1 => 3.3.2.
     The “child” entry function (+++) will assign the new note to the first child, or the closest child.
     1 => 1.1, 2.1 = 2.1.1. """)

          self.add('INITIATE',
                   """
MODIFYING_THE_DISPLAY_OF_NOTES/**/
     As you either progress through the indexes of the notebook, or enter in indexes directly as commands, ARCADES displays them, either alone, or together with the cluster of notes that belong to the tribe of the top level note.

     The behavior of the sequential display mode is determined with the following commands: "childrentoo", "fulltop", and "automulti".

     In its default “childrentoo” mode, ARCADES displays the current note together with the entire tribe of notes belonging to the top-level note with which it is associated.
     The binary "childrentoo" command can be used to have ARCADES no longer show the tribe together with the note.

     When the “childrentoo” mode is deactivated, then, if the “fulltop” mode is activated, ARCADES will only display the entire tribe for top-level notes.
     Other notes with be displayed alone.


     When the “automulti” mode is activated together with the “childrentoo” or “fulltop”-modes, then ARCADES will display the tribe as a tiled sheet. 


     """)

          self.add("INITIATE",
                   """
SHOWING_ALL_NOTES_IN_THE_NOTEBOOK/**/
     The "all" command can be used to display all the notes in the notebook.
     If your notebook contains many notes, it may take a bit of time to run the first time it is used, but it saves the results to a buffer which may be retrieved subsequently.

     The command "all", in addition to being restricted to
     a certain index range, accepts a single value and several modifiers.
     The optional value indicates the size of the indexes to be listed; all indexes must be less than this value.

     If no value is listed, then notes with indexes are all sizes will be displayed.

     Modifiers include: /& /? /=

     1) /& Excludes non top-level notes.
     2) /* Excludes square characters around notes –
          allowing format to be outputted in a form
          that can be copied into other programs.
     3) /? Suspends the automatic short mode
     4) /= Includes dates with the notes""")

          


          self.add('INITIATE',
                    """
FIELDS/**/
     Fields are used to divide the notebook into different sections.
     A field is assigned to a set of indexes. It is possible to assign a field either to 1) a range of consecutive top-level (size=0) indexes regardless whether they are present in the notebook.
     0r 2) a range of indexes, greater than p and less than q and of arbitrary size, that are actually present in the notebook.
     Or 3) to any set of indexes, whether or not they are present in the notebook. A given note at a given index can belong to one field at most.
     Consider the following examples:

     Suppose that the notebook contains notes at indexes 1,8,19,27.

     (1) addfield:SLOTH;1-100
          | Will add the field SLOTH to
          | all indexes that are present in
          | the notebook within range 1-100.

     (2) addfield:SLOTH; 1,2,3,4,5,33.1
          | Will add the field SLOTH to all indexes 1-5 and 33.1,
          |regardless of whether they are present in the notebook.
          |Fields can be overwritten, and deleted, with
          |these same principles applying.
          |Field names need not be in all-caps; they
          |can indeed include spaces and non-reserved special
          |characters.""")

     
          self.add('INITIATE',
                   """
DISPLAYING_NOTES_AS_A_SHEET/**/
     The “multi” mode fits notes together into a “sheet,” according to their width.

     The notes are placed in a stack, with the largest possible note that can fit in the free area withdrawn from the stack.
     The output of the multi display is stored under a user-defined name, and can also be saved as a text file.

     The syntax consists in four values, and three modifiers:
     multi:INDEX COLLECTION;DISPLAY STREAM;WIDTH;SAVE STREAM /* /? /=

     
     The first value indicates the indexes to be displayed; the second the name of the “stream” to which display will be outputted, and the third the width, in characters, of the display.

     The /$ modifier shows notes in a uniformly small size, as defined using the command smallsize.

     The /* modifier is used to activate the “vary”-mode, adjusting the size of the notes according to the length of the text string.

     The /? pauses the display after each line.

     The /= saves the output to a textfile, using either the name of the display stream or name entered as value 4.""")


          self.add('INITIATE',
                   """
REORGANIZING_THE_NOTEBOOK/**/
     Commands for manipulating the notebook may be divided into three categories:

     1) Those which only affect the relation of the note to the index.
     | These “index” commands include: "delete", "move", "copy", "clear", "purge", "rehome", "eliminateblanks".

     2) Those which change the “content” and “properties” of notes without changing indexes.
     | These “content” commands include: "correctkeys", "reform",
     
     3) Those which change both the “content” of notes - the keywords and text –as well as the relation of this content to indexes.
     | These “note” commands include: "revise", "mergemany", "conflate", "split", "sidenote"
     """)

          self.add('INITIATE',
                   """
DELETING_NOTES_/**/
     Entering "delete", or alternatively "del", with a collection of notes as a value, deletes these notes by moving them to a negative index positions.

     The "clear" command is used to delete all the notes from the notebook by moving them to negative index locations.

     Because it is rather dangerous to use, it queries you each at step to see if you want to continue.

     There is little reason for using "clear" except when working with very small notebooks

     The command "undel" is used to “undelete” the notes with negative indexes, moving them back into positive registers.


     The "compress" command compresses the notebook by moving all the note to contiguous index positions.

     The "rehome" command is similar to compress, but moves notes in such a way as to eliminate orphan notes.
     The rehome command accepts as a value a collection of notes.""")

          self.add('INITIATE',
                   """
MOVING_NOTES/**/
     The "move" command allows you not only to move individual notes from one index location to another, but also to move collections of indexes and even transform the hierarchical structure of the notebook itself.

     The syntax of the move command is as follows:

     move:INDEXESFROM;INDEXTO;[S/M/C];[yes/no] /$ /& /* /? /=

     The first value indicates the collection of indexes that will be moved; the second the destination to which they will be moved; the third
– either S, M or C indicated how the how the notes will be organized at the destination; and the fourth value whether the children of indexes will be included.

     The first of the three modifiers are to indicate the third value, while the fourth and fifth are used for the fourth value.
     Thus:

     (1) /$ ≈ (is equivalent to)
     S ≈ Subordinate the indexes under
     the destination index,
     preserving the hierarching structure
     of the source collection.

     (2) /& ≈ M ≈ Make the indexes
     “compact” (“compressed”) under
     the destination index, so that whatever
     hierarchical structure they have
     is eliminated. Whatever their structure
     in the source was, they will be turned
     into a series of siblings.

     (3) /* ≈ C ≈ Organize the indexes
     as a series of “children” in the destination range.

     (4) /? ≈ yes ≈ exclude “child”
     indexes from the source range.

     (5) /= ≈ no ≈ don’t exclude “child” indexes

     It is important to note that the behavior of S/M/C depends on whether the destination range is already occupied.
     If there is an index in the destination, then the new notes will be placed in a subordinating relation – either (S), which creates a “microcosmic representation” of the source range subordinated to destination index.
     Or (M), which flattens them into siblings, children of the same index.
     Or (C), which turns them into a chain of children.
     Observe, also, that ARCADES does not forbid you from moving the source range into itself, nor can this “crash” the system.

     This is because notes are moved individually, the interpretation of each “move” depends on the present state of the system after an individual move, and ARCADES will either refuse to execute a move (if the source index is empty) or will interpret it such that it can be done (if the destination is occupied).
     
     For this reason, though, it may be a bit tricky to foresee how a command will be executed when it moves indexes onto themselves.""")

          self.add('VARIABLES',
                   """
VARIABLES/**/Variables can be used to store the results of searches, lists of keys, and even text, and then feed these back into commands as values. """)
          self.add('VARIABLES',
                   """
DEFINING_VARIABLES/**/
     To define a variable, simple refeed the results of a command into a variable name.
     Variable names must be written in capital letters and not have any non-alphabetic characters.
     For example:
     (1) keys:1-10 =>SOMEKEYS
     | Feeds the keywords
     |for notes 1-10 into SOMEKEYS
     (2) show:1 => SOMETEXT
     |Feed the text for note 1
     |into SOMETEXT
     (3) ?:<Husserl> =>SOMEINDEXES
     |Feed search result
     |into SOMEINDEXES""")

          self.add('VARIABLES',
                   """
USING_VARIABLES/**/
     To retrieve the contents of a variable, simply include it in double curly brackets.
     For example:
     (1) ?:{{SOMEKEYS}}
          |Searches for SOMEKEYS
     (2) +:Husserl;{{SOMETEXT}}
          |Enters a new note with SOMETEXT as the note text.
     (3) show:{{SOMEINDEXES}}
          |Show the notes in SOMEINDEXES""")

          self.add('INITIATE',
                   """
COPYING_NOTES/**/
The "copy" command is identical to the move command, save that it does not delete the note from the source index.


The command "permdel" is used to permanently delete all the notes with negative indexes.

To see the notes with negative indexes – the temporarily deleted notes – use the command "showdel.""")

          self.add("INITIATE",
                   """
REVISING_NOTES/**/
     The command "revise" (alternate form: "rev") is used to add to an existing note.
     It can either add the text of ne existing note to another note, or call up the text inputter.

     The user can also define the text placed between the note, and whether the new text is placed before or after.

     The revise command accepts three values and the modifiers /$ /& /* /?.
     The first value is used to select the index or collection of indexes to be revised, the second value is the index of the note to be added, and the third value is the text to be inserted between notes.

     The /$ modifier is used to add the new text to the beginning rather than the end.
     The /& modifier adds the new text both the beginning and the end.
     The /* modifier selects /BREAK/ as the “breaker”
     The /? modifier selects /NEW/ as the “breaker” """)

          self.add("INITIATE",
                   """
MERGING_NOTES_TOGETHER/**/
     The command "mergemany" is used to take a collection of indexes, and join them together into a single note.
     It does not delete the indexes that is conflates, and hence it can be understood as a mode of copying.

     It accepts three values and the modifiers /$ and /&.

     The first value is the collection of indexes to be joined together.
     The second value is the index of the destination where the new note is to be placed.

     The third value is the manner in which the notes are to be joined together, and can be either(c)onflates or (e)mbedded.

     The modifier /$ is the equivalent to the value (c)onflate while the modifier /& is the equivalent to the value (e)mbed.
     If you use both modifiers, it will repeat the action twice in each of the two manners.

     The “embed” joins together displayed notes, together with brackets, whereas “conflate” merely combines the text of the notes and their keywords.
""")

          self.add("INITIATE",
                   """
MERGING_NOTES_WITH_CONFLATE/**/
     The command "conflate" is similar to "revise" and "mergmany."

     It joins a collection of notes together separated either by /BREAK/, /NEW/ or a user-defined term.

     It accepts four values and the modifiers /$, /&, /*, and /?.

     The values consist in
     (1) the collection of the indexes of the notes to be joined together.

     (2) the destination of the newly created note.

     3) (e)mpty, (b)reak, or (n)ew.

     4) a user defined “breaker”.

     The first three modifiers are equivalent, respectively, to (e)mpty, (b)reak, and (n)ew, while /? Is used to solicit a user-defined “breaker.”
""")
          
          
          

          self.add('SEARCH',
                   """
ADDING_QUALIFIERS_TO_SEARCH_TERMS/**/
     Qualifiers are attached to individual terms in order to add further restrictions on the query.

     The Qualifier Phrase enclosed within double quotation marks, and affixed directly after the individual search term, with no blank space.
     The term consists in one or more qualifiers separated by exclamation marks. 
                   
     Qualifiers may take either no value, a single integer value, a single string value, or a single range of value. The following are examples of valid search expressions with qualifiers:


     1) ?:frog“count=1”
     |Search for notes in which
     |the word “frog” appears once.
     2) ?:<toad>“depth=1/3”
     |Search for notes whose
     |index has a depth not less than
     | and not greater than 3
     3) ?:*ism”date=2020-1/2020-4!depth=4/5”
""")

          self.add('SEARCH',
                   """
REFEEDING_SEARCH_RESULTS/**/
     Any command which yields a list of indexes or range of indexes, or a list of searchable terms, can be refed into another command as follows:

     1) COMMAND1 =>COMMAND2:?
        | To refeed indexes, or index-ranges.
     2) COMMAND1 =>COMMAND2:??
        | To refeed search terms as a list
     3) COMMAND1 =>COMMAND?:???
        | To refeed search terms as a search phrase
     3) COMMAND1 =>COMMAND2:????
        | To refeed text""")

          
          self.add('SEARCH',
                   """
THE_SEARCH_LOG/**/
     The searchlog command is used to show all previous search results.

     The search log allows you to combine the results of previous searches.""")

          self.add('SEARCH',
                   """
STORING_SEARCH_RESULTS_WITH_VARIABLES/**/
     Variables can be used to store the results of searches, lists of keys, and even text, and then feed these back into commands as values.


     To define a variable, simple refeed the results of a command into a variable name.
     Variable names must be written in capital letters and not have any non-alphabetic characters.

     For example:
     (1) keys:1-10 =>SOMEKEYS
       | Feeds the keywords
       | for notes 1-10 into SOMEKEYS
     (2) show:1 => SOMETEXT
     | Feed the text for note 1 into SOMETEXT
     (3) ?:<Husserl> =>SOMEINDEXES
     |Feed search result into SOMEINDEXES

          
     To retrieve the contents of a variable, simply include it in double curly brackets.

     For example:

     (1) ?:{{SOMEKEYS}}
    | Searches for SOMEKEYS
     (2) +:Husserl;{{SOMETEXT}}
     | Enters a new note with SOMETEXT as the note text.
     (3) show:{{SOMEINDEXES}}
     |Show the notes in SOMEINDEXES""")

          self.add('SEARCH',
              """
THE_SLICE_QUALIFIER/**/
     The “slice”-qualifier can be used to restrict the search results to notes whose indexes are contained “within” the upper and lower slice.

     A slice consists in of values, separated by PERIODS.
     Every value may either by be empty, or consist in either an integer, for the value at the head of the slice, or a natural number.

     Or in other words: a slice is an index, with some, but not all, of the elements removed.
     
     Valid slices include: “1.2.3.4.5.6”, “…5…”,”-10.1.1.1.1.”

     A given Index is “within” a lower and upper bound iff each element of the index is not less than equally-ranked element of the lower bound and not greater than the equally-ranked element of the upper bound.
     If a bound is not given, whether because either the upper or lower bound has not been defined or because ranked-element is missing, then the condition is automatically satisfied.

     If the “must”-mode is selected, then the index must have elements of rank equal to all the rank of all the elements of the lower and upper bound. Or in other words, if an index is not as “deep” as the greatest depth of the upper or lower bound, then the index will not be “within” the slice.

     Examples of slices.
     1.1.1 is within “slice=1.1.1/2.2.2”
     3.3.3 is not within “slice=/.2”
     10.1^10 is within “slice=/.1.1.1.1.1.1.1.1.1.1.1”
     10.1^10.2 is not within “slice=/.1.1.1.1.1.1.1.1.1.1.1.1.1.1”
     10.1 is within “slice=10.1.1/12.1.1” in the “must”-mode.
     10.1 is not within “slice=10.1.1/12.1.1” if not in the “must”-mode
""")

          self.add('SEARCH',
              """
THE_COUNT_QUALIFIER/**/
     The following qualifier can be used to exclude notes where a single search term appear in the text less than or more than a certain number of instances.

     count=LESSTHAN/GREATERTHAN

     The qualifier “strict” can be used to count by whole words.
     The result is more correct, but it is also a bit slower, since it must iterate over the Cartesian product of the punctuation marks. """)
          self.add('SEARCH',
                   """
GLOBAL_SEARCHS/**/
     The command "globalsearch" can be used to search over all active notebook.
     An active notebook is a notebook that has been opened during the current session


     To search over a range of active notebooks, enclose a list of the notebooks, separated by commas, with curly braces and place it right before the search phrase.
     search:{HEIDEGGER,HUSSERL}being
     | Search for the term “being” inn the notebooks HEIDEGGER and HUSSERL

     """)
          
          self.add('INITIATE',
                   """
HISTOGRAMS_AND_CHRONOGRAMS/**/
     Histograms display a frequency chart for keywords or words in the text.

     ARCADES allows you to represent the keys in a collection of notes by date and time of composition or modification.
""")

          self.add('REPRESENTATIONS',
              """
HISTOGRAMS/**/
     Histograms display a frequency chart for keywords or words in the text. To produce a histogram, simply use the "histogram" command, with a collection of indexes as the value.

     The modifier /$ is used to choose between text words and keywords.""")

          self.add('REPRESENTATIONS',
              """

CHRONOGRAMS/**/
     ARCADES allows you to represent the keys in a collection of notes by date and time of composition or modification.

     The chronogram feature is very flexible, and sorts according to year, month, day, or even hour, in various combinations.
     It also allows you to choose between using the first date, the newest date, or all the dates associated with the notes in the index range, and also reveal or suppress the indexes associates with the keys.""")

          self.add('REPRESENTATIONS',
              """
INITIATING_A_CHRONOGRAM/**/
     To initiate a chronogram, use the "constdates" (alternative form: "constitutedates") command, which accepts three values and the modifiers /$, /&, /* and /?.
     The first value consists in a collection of indexes, the second value the determinant, and the third value in either f(irst), n(ewest), or a(ll). 
     The modifiers /$ and /& can be used to define the determinant, respectively, as ym (year+month) or ymd (year+month+day), in lieu of the second value.

     The modifier /* is used to show indexes, while /? Explicitly ask which dates are to be used, and thus can be substituted for a third value.

     Consider the following commands:
     (1) constdates:1-100;ymd*h;f /*
     Create a date dictionary for indexes 1 to 100, with ymd*h as the determinant, using the date when the note was first entered, and displaying indexes.

     (2) constdates:1-1000;ym /?
     Create a date dictionary for indexes 1 to 1000, using ym as a determinant, and querying whether to use the first, newest, or all dates.

     The determinant indicates what divisions of time (year=y, month=m, day=d, hour=h, minute=m, second=s, microsecond=x) will be used to organize the date dictionary.

     The maximum determinant is ymd*hmsx.
     Any subset of the maximum determinant, with the star included, is a valid determinant. 


     Chrongrams are stored in a dictionary using the determinant as key.
     You can use the command "showdatedict" to display an existing chronogram.
     This accepts the determinant to be displayed as a value, and the modifiers /$, /&, /*, /?, /=, which are used to add, respectively, year, month, day, hour, and minute.
     The minute can only be added after an hour.
""")

          self.add('REPRESENTATIONS',
                   """
ENTERING_THE_DETERMINANT_FOR_A_CHRONOGRAM/**/
     The determinant can always be entered explicitly when initiating a chronogram.
     If no determinant is indicated either through a value or a modifier, then ARCADES will use the default determinant.
     The default determinant is preset to “ym” – year and month – but it can be changed by using the "changedet" command.
     The current determinant can be displayed with "showdet". 
""")
          self.add('REPRESENTATIONS',
                   """
RETRIEVING_CHRONOGRAMS/**/
     Chronograms are stored in a dictionary using the determinant as key.
     You can use the command "showdatedict" to display an existing chronogram.
     This accepts the determinant to be displayed as a value, and the modifiers /$, /&, /*, /?, /=, which are used to add, respectively, year, month, day, hour, and minute.
     The minute can only be added after an hour.

     You can use the command "activedet" or "actdet" to display the determinants for which chronograms currently exist.
""")
          self.add('REPRESENTATIONS',
                   """
PURGING_KEYS_FROM_CHRONOGRAMS/**/
     Because the chronogram displays keys, it may be desirable not to have it show every single key, since otherwise it will become excessively large and, consequently, not very useful.
     ARCADES thus allows you to display a chonogram with selected keywords, or types of keywords, purged from it.

     This is done using the "showdatedictpurge" command, which takes two values and the modifiers /$ /& /* and /?.
     The first value is the determinant, which functions as with "showdatedict".
     The second value is the purge sequence.
     The modifier /? Is used to query for a purge sequence.
     The syntax of the purge sequence is explained below. Keep in mind, however, that if the purge sequence is entered through showdatedict, then the modifiers cannot be used.
""")
          self.add('REPRESENTATIONS',
                   """
SETTING_THE_PURGE_SEQUENCE/**/
     With the "setpurgekeys", it is possible to instruct ARCADES to purge specific categories of keys as well as certain individual keys. 
     The command "setpurgekeys" accepts one value—a purge instruction-- and all five modifiers.
     The purge instruction has the following syntax:
     SPEC|KEY1,KEY2,KEY3…
     SPEC consists in one or several of the following symbols, each of which is equivalent to a modifier:
     a[ll caps] | /$
     u[pper case] | /&
     l[lower case] | /*
     s[eqeunces] | /?
     n[umbers] | /=
     KEY is a valid search phrases, and yields all the applicable keywords.
     So for example: *a* would yield all the keywords containing “a” in the middle.


     The following related commands are also available:

     "clearpurekeys" | to clear all the purge keys.
     "showpurgekeys" | to show the purge keys


     
""")
          self.add('REPRESENTATIONS',
                   """
CLUSTERING/**/
     Clustering allows you to organize a collection of notes into groups with “connected” keywords.
     Use the "cluster" command to create clusters, entering the range of indexes as a value.
     Keywords are “connected” if they either belong to the same note, or are both “connected” to a third note, with this definition applied recursively to yield an exhaustive system of “connections” for every note.
     The relation of “connection” is reflective, symmetrical, transitive, and substitutive.
     The system of “connections” is called a cluster, and every note within a cluster is connected with every other note within it.

     The usefulness of clustering depends on the structure of the notebook, and the keywords used.
     If keywords are assigned too liberally, then the clusters will become so large as too be useless.
     A notebook that clusters nicely is “variegated”; a notebook that clusters poorly is “monolithic.”

     In order to make monolithic notebooks seem less monolithic, and hence more amenable to clustering, ARCADES allows you to 1) use only a certain number of the least frequent keys and 2) purge keys from the keysets.
     These two operations can be combined.
     The reason for favoring the least frequent keys over the most frequent is obvious: the least frequent keys are more likely to be have a specific “differential” value in relation to other keys in the notebook, and hence to be
     semantically meaningful. 
""")
          self.add('REPRESENTATIONS',
                   """
DEFINING_THE_PURGE_FUNCTION_FOR_CLUSTERIG/**/
     The purge function for clustering cannot be defined during a function call, but only by using the "cpara" command, which accepts one value – a subset of the string “acl,” according as you wish to purge all-cap words, capitalized words, or lower case words – and the modifiers /$, /&, and /*, which correspond, respectively, to these three different kinds of purges.
     Hence, to purge keywords that are in all caps, you could enter either:
     (1) cpara:a
     (2) cpara /$
""")
          self.add('REPRESENTATIONS',
                   """
ITERATING_OVER_CLUSTERS/**/
If you use the /$ modifier while initiating clustering, then ARCADES will create a series of iterators corresponding to the clusters, making it possible to advance from iterator to iterator – from cluster to cluster, in other words – resetting the iterator each time.
To advance to the next iterator, simply enter a semicolon (;). 
""")
          self.add('REPRESENTATIONS',
                   """
KILLING_CLUSTERS/**/
The killclusters command can be used to eliminate the clustered iterators.
""")
          
          self.add('INITIATE',
              """

PROJECTS/**/
     A “project” in ARCADES stores some basic information about the program-state and keeps track of the indexes of notes that have been added to the project.

     Finally, when a project has been activated and is in use, each new note will include, as sequence keyword, the name of the project together with a value indicating the order in which the note has been entered, with the initial value determined by the user.""")

          self.add('INITIATE',
              """
PROJECT_ATTRIBUTES/**/
     Projects are stored in a special dictionary, which is a permanent attribute of the notebook.
     The name of the project serves as the identifying key.

     For each project, the following attributes are kept track of and stored:

     1) The default keys, which are automatically included when the project is active.
     2) The current position in the notebook.
     3) The current entry mode,
     such as “connext” or “conchild”
     4) A list of all the indexes
     that have been added to the notebook.
     5) The date when the project began.
     6) The date that it was last modified.
     7) Whether it is currently open.""")

          self.add('INITIATE',
              """
COMMANDS_FOR_PROJECTS/**/
     Commands for using projects include: "newproject", "saveproject", "showprojects", "resumeproject", "loadproject", "endproject", "flipproject", "crrrentproject", "archiveproject", "unarchiveproject", "showarchivedrpojects", "deletearchivedrpoject", "loadproject", "dumpproject", "renameproject". """)

          self.add("INITIATE",
              """

NEWPROJECT/**/The command "newproject" is used to initiate a new project The name of the new project is entered as a value.

     If, however, a project with this name already exists, and the project name is alphabetic, not already ending with a number, then a 1 will be suffixed to the project name.
     If the project name already has a numerical suffix, then the existing numerical suffix will be increased by 1.

     So for example: HEIDEGGER > HEIDEGGER1 > HEIDEGGER2 > HEIDEGGER3""")

          self.add("INITIATE",
              """
SHOWPROJECTS/**/
     To display all the projects that are currently attached to the notebook, type "showprojects"

     To resume a project that already exists, type "resumeproject", with a single project or list of projects as a value.
     If a project is already active, this will be saved before a new project is activated.

     You will be asked if you wish to update the defaultkeys in the project.

     This command also accepts to modifiers:
     /$ and /&.

     Use the first of these to add a second projec to an existing project, and the second if you do not wish to automatically update the position and the entrymode.

     
""")

          self.add("INITIATE",
              """
QUITTING_PROJECTS/**/
     To quit the current project, enter "endproject" (alternative form: "quitproject").

     The command 'flipproject" takes the indexes of the current project and sends them to the flipbook, allowing you to iterate over them.

""")

          self.add("INITIATE",
              """
SWITCHING_BETWEEN_PROJECTS/**/
     ARCADES allows you to open several notebooks at once, switching back and forth between them. To switch, you use the "switch" command.

     The first time that you use it, it will exit the current notebook, and allow you to enter a new one.

     To do so, select (N) in the input menu.
     Once more than one notebook is active, future uses of switch will display the active notebooks, and allow you to switch to a new one, or remain in the old one, just by typing the number corresponding to it.
     When you quit a notebook, the notebook will be closed and you will be returned to the “switch” menu.
     Here it is possible to quit all the
     active notebooks, closing ARCADES.""")
     
          self.add('INITIATE',
              """
MOVING_NOTES_BETWEEN_NOTEBOOKS_WITH_THE_COPY_BUFFER/**/
     Each active notebook is a unique notebook-object.
     ARCADES, however, also allows you to store notes in a common register shared by all the notebooks.

     Enter "copyto", with a collection of indexes as a value, to copy notes into the temporary buffer.

     Enter "copyfrom", with a single value indicating the number of notes, or using the modifier /$ to indicate all the notes in the temporary buffer.

     The temporary buffer functions as a stack -- first in/first out – and notes are deleted as soon as they are “copied” out of it.""")

          self.add('ENTERING',
                   """
/ENTERING_MODES/**/
     If an index is entered as the first value, ARCADES will initiate the note inputter, adding a note at the first available index, or the first available child or sibling of the index that had been entered.
     If a key or list of keys is entered in the first value, ARCADES will add an empty note—a note with an empty text-string---together with theses keys.
     If a key or list of keys is entered in the first value, and a second value is also added, then ARCADES will add new note with the given keys and text. Use a vertical line (|) --- an EOL --- to mark the end of the line.
     Finally: if an index is entered in the first value, key(s) in the second value, and text in the third, ARCADES will add a new note with the given keys and text at the index, or first available index position, as per the rules above.""")

          self.add('ENTERING',
                   """
THE_PROSE_MODE/**/
     The prose mode does not automatically insert an EOL character with each new line.
     It is still possible to insert a manual EOL character using one vertical stroke(|), or by inserting one or more spaces at the beginning of the line of text.""")
          

     
          self.add('ENTERING',
              """
THE_POETRY_MODE/**/
     The poetry mode automatically inserts an EOL character at the end of each line, thus preserving the integrity of the verse.
     Whereas in the prose mode, the size of the note is arbitrary, and determined in advanced, the poetry mode sizes the note based on the longest line of text.
     It is possible to combine poetry and prose in the same note, but, so long as prose is selected once, then the size of the note will be determined “poetically” rather than “prosaically." """)

          self.add('ENTERING',
              """
THE_SPELLCHECKER/**/
     ARCADES includes a basic spell-checker.
     If there are misspelled words, the spelling corrector will be activated automatically. To deactivate or activate the spelling feature, use the binary command "spelling" """)

          self.add('ENTERING',
                   """
TERMINATING_INPUT/**/
     Two VERTICAL STROKES (|) placed at the end of the line will terminate the text input.
     It is also possible to terminate text input by pressing return a certain number of times in succession.
     Use the binary "returnquit" command to activate or deactivate this option, and use the set return quit command to set the number of returns needed to automatically quit.
     By combining automatic initiation of note entry with automatic termination of the text inputter, it is possible to enter a note using only the return key.""")

          

          self.add('ENTERING',
              """
EDITING_NOTES /**/
     IT is possible to edit, subsequent to entry, either the keys of a note, the text of the note, or both.
     The commands for initiating editing are:
     "editnote", "editnotekeys", "editnotetext."
     These are followed by an index or a collection of indexes.
     The command editnote accepts a single modifier /$, which is used to activate the “annotate” mode.
     Whereas editnote edits both the keywords and the text of a note, "editnotekeys" or "editnotetext" can be used to edit only the keys or only the text.""")

          self.add('ENTERING',
                   """
INCLUDING_SEQUENCE_KEYWORDS/**/
          The binary command "seqintext" can be used to include sequence keywords in the note of the text, uncluttering the keywords while at the same time allowing for clearer presentation of especially pertinent information.
          It can even be used to include the equivalent of a title in each note, show atthe the top of the text, simply by using title@TITLE as a keyword.

""")

          self.add('ENTERING',
                   """
INCLUDING_SEQUENCE_KEYWORDS/**/
     The sequence keywords are included in the text in the following order
     1) The main sequences, which can be user defined, but default to: title, author, date, datefrom, dateto, book, page, chapter, section.
     2) Projects.
     3) Other sequences""")

          self.add('ENTERING',
                   """
ADJUSTING THE FORMATTING OF SEQUENCES/**/
     ARCADES provides two commands that can be used to adjust the formating of sequences when displayed within the text of the note: "seqformone", which is used to adjust the character that appears after the first two sections, and "seqformtwo", which determines the character that separates off the sequence keywords from the rest of the notetext.
     Both of these accept one value, - the breaking characters -- and include a variety of options.
     If entered without a value, they will call up a selfexplanatory menu.
     The command mainsequences can be used to change the main sequences.
     It accepts a single value: a list of sequences separated by commas.
     It is possible to restore the defaults by entering ‘d’.
""")

          self.add('ENTERING',
                   """
METADATA/**/ Every note includes metadata: the size of the note expressed as a single integer indicating the width of the note, the name of the user who entered the note, and a list containing the timestamp of the creation of the note as well as every subsequent revision.
""")

          self.add('ENTERING',
                   """
METADATA_COMMANDS/**/
     ARCADES offers the following commands for changing and viewing metadata.


     The command "resize" (alternate forms: "size", "rs") can be used to change the default size of note.
     It accepts a singer integer value, which corresponds to the width in characters of the note.

     The command "changeuser" changes the active user as listed in the metadata of the note.

     The command "showmeta" shows the metadata for the note at the index given as its value.

     The command "showuser" displays the default name of the user which is included in the metadata when the note was entered.""")

          
          self.add('ENTERING',
                   """
GENERAL_MODIFIERS_FOR_ENTER_COMMANDS /**/
     All of the entering commands permit the following 2 modifiers: /* and /+.
     The first of these, /*, is used to repress the show function.
     The second of these, /?, is used to suppress the default keys.""")

          self.add('ENTERING',
                   """
INITIATING_ENTRY_WITH_A_LIST_OF_KEYWORDS /**/
     It is also possible to initiate entry of a note simply by listing more than one keyword, separated by a comma.""")

          self.add('ENTERING',
                   """
KEYWORD_QUERYING/**/
     If keywords have not been entered, ARCADES will query the user for keywords to add, either before, or after, or both.
     To activate or deactivate querying either before or after text input, use the binary commands "keysbefore" and "keysafter".
     It is also possible, in this way, to suspend keyword querying altogether.""")
     

          self.add('ENTERING',
                   """
INCLUDING KEYWORDS/**/
     If words or phrases included in the text are enclosed in curly brackets, then ARCADES will give you the option of adding them to the keywords associated with the note.""")
          
                   
          self.add('ENTERING',
                   """
INCLUDING_TEXT_AND_IMAGES/**/
     Text files can be inserted into the body of note by entering the name of the file in double curly brackets with the prefix AT (@) or STAR (*).
     Depending on whether the prefix is an AT or STAR, ARCADES will seek the file in the folder “/textfiles” or “/attachments.”
     For example:
     {{@textfile}}
     {{*attachment}}
     When the note is displayed, the text from the file will automatically be included.
     To enable or disable the automatic display of the attached text, use the binary command showtext. 2.3.2.1.2.2.3.

     Including a JPEG image.

     A jpeg (.jpg) file can be included in the body of the note by surrounding it with double curly brackets and using a CARET (^) as a prefix:
     {{^picture}}
     When the note is displayed, the jpeg file will be opened.
     It must be closed manually.
     To enable or disable the automatic display of images, use the binary command showimages.""")

          self.add('ENTERING',
                   """
ADVANCED_ENTRY_MODES/**/
     ARCADES also offers two advanced entry modes, which make it possible to avoid the separate keyword entry, and entering the entire note as a single text, with all the keywords and sequences extracted from this.""")

          self.add('ENTERING',
                   """
THE_FROM_TEXT_ENTRY_MODE/**/
     The "fromtext" command activates the fromtext mode, which automatically suspects the separate keyword prompt.
     The fromtext mode applies rules to parse the entered text, following the following rules.

     (1) The text is divided into segments, each of which is surrounded by LMARK and RMARK.

     (2) Each segment consists in an IDENTIFIER and a sequence of VALUES.

     (3) The IDENTIFIER is separated from the VALUES by MARK2.

     (4) Each value in the list of VALUES is separated by MARK2.

     (5) The followed reserved IDENTIFIERS are used:
     text | Used to indicate
          | the main text of a note
     keywords |Used for non-sequence
              |keywords, which may
              |include tags and knowledge.
     (6) All other VALUES will be interpreted as sequences. But if date is included in its name,then it will define a date sequence, and, likewise, is index is in its name, an index sequence.

     LMARK, RMARK, MARK1, MARK2 are preset to EOL, EOL, COLIN, and COMMA.
     It is possible, however, to define new presets. When EOL is used as a preset for LMARK/RMARK, then it is recommended that you enter the text in the poetry mode.""")

          self.add('ENTERING',
                   """
NEWCOVERTMODE/**/
     To create a new set of parsing presets, use "newconvertmode". This will ask you for the name of the new mode.
     To define the presets, use "convertdefinitions". To switch to an existing set of presets, use "switchconvertmode".
     To show all available presets, use "showallconvertmodes".
     When entering the divisor, you must add an UNDERLINE between the LMARK and the RMARK if the legnth of either term is greater than one character.""")

          self.add('ENTERING',
                   """
CONVERTBYLINE/**/
     The command "convertbyline" offers a simpler alternative, a hybrid between regular entry and converting entry.
     It extracts keywords and sequence keywords, following above the rules, during line entry, and hence can be combined with the regular mode of keyword entry.""")

          self.add('ENTERING',
                   """
ACTIVATING_THE_CONVERT_MODE/**/
     To activate a convert mode and apply it, simple include //MODENAME// in the body of the text, preferably at the head.""")


          

          

          self.add('ENTERING',
                   """
CONNEXT_AND_CONCHILD_ENTRY_MODES/**/
     Several different modes of note entry are available through the terminal.
     The most basic mode, described above, initiates either with an explicit command or with a list of keywords.
     The second mode – called the “con-mode,” automatically initiates a new note whenever RETURN is entered, if no other command or text proceeds it.
     This mode is activated by the "connext" or "conchild" command, and is deactivated by entering a double semicolon (;;).
     If you use the "connext" command, the next index will be a sibling of the current index.
     For example: 1=>2, 1.1=>1.2, 1.1.5=>1.1.6, The conchild command, in contrast, will produce a child of the current index; for example, 1=>1.1,1.1=>1.1.1,1.7.19=1.7.19.1.
     The third mode, the “quick” mode, allows you to directly enter a note in the form of the command, with the list of keywords coming before the COLON and the text of the note coming after.
     Neither the “quick” mode nor the “con” mode prevents you from entering regular commands.""")

          self.add('ENTERING',
                   """
UNDO_AND_REDO/**/
     ARCADES keeps track of actions involves entering, deleting, and moving notes.
     To reverse an action that has been performed, use the command "undo". To restore a command that has been undone, use "redo".
     The "undo" and "redo" commands are limited to actions that involve entering, moving, and deleting notes.""")

         

          self.add('WORKPAD',
                   """
THE_WORKPAD/**/
     The ARCADES workpad enables a more visually oriented mode of note display and note entry without departing from the text-based non-GUI operation of ARCADES.
     It was designed around the Python CURSES module, which is not included in the standard Windows distribution of Python.
     The workpad cannot be used if ARCADES is run from IDLE.
     Notes from the regular notebook can be sent to the workpad, and then placed on the window area, which can be scrolled vertically and horizontally, and manipulated in various ways.
     In addition, the workpad allows for drawing with Unicode characters, and typing directly on the workpad.
     Finally, new notes can be composed in the workpad, which are then added to back to the notebook on leaving the workpad mode.""")

          self.add('WORKPAD',
                   """
INITIATING_A_WORKPAD/**/
     To initiate a workpad, use the command "createworkpad". This command accepts, as an optional value, the name of the pad to be initiated.
     If no padname is given, it will activate the default workpad.""")
          self.add('WORKPAD',
                   """
ADDING_NOTES_TO_THE_WORKPAD/**/
     To add notes to the workpad buffer, use the command "addtopad", which accepts two values: the range of indexes of notes to be added, and the name of the pad you wish to use.
     If no padname is given, the notes will be added to the default pad.""")
          self.add('WORKPAD',
                   """
OPENING_THE_WORKPAD/**/
     The command "padshow" or "showpad" switches to the workpad.
     The command "showpad" accepts as a value the name of the pad that you wish to open.""")
          self.add('WORKPAD',
                   """
RENEWING_THE_WORKPAD/**/
     Use the command "renewpad", with the name of a workpad as an optional value, to empty out the stack of a workpad.""")
          self.add('WORKPAD',
                   """
CHANGING_THE_WORKPAD/**/
     Use the command switchpad:PADNAME to change the current workpad.
     Use the command currentpad to display the current workpad, and allpads to display all the workpads.
""")
          self.add('WORKPAD',
                   """
THE_WORDKPAD_DISPLAY/**/
     The top left of the workpad displays the number of notes in the workpad and in the buffer, and, directly below this, the coordinates of the left and topmost position of the window together with the total size of the workpad.
     This is expressed in the following format: Xleftmost/Xtotal : Ytopmost/Ytotal.
     Also displayed on the top ribbon is the index of note lying directly under the cursor, and the indexes of the first notes being displayed on the workpad.
     The left corner of the bottom ribbon displays the following information: the line drawing mode, the hex value of the foreground and background color, the drawing character, the drawing symmetry form, the speed, and the character display mode.
""")
     
          self.add('WORKPAD',
                   """
BASIC_OPERATION_OF_THE_WORKPAD/**/
     The basic operation of the workpad is determined by the mode which is selected by pressing F3.
     The mode is displayed at the bottom left side of the workpad, unless the regular mode has been selected. The available modes include:
     REGULAR
     | Use the arrow keys to move window
     TYPING
     | Type directly onto the workpad
     CURSOR
     | Use the arrow keys to move the cursor
     EXTENDING
     | Use the left and up arrows to enlarge the workpad
     CONTRACTING
     | Use the left and up arrows to contract the workpad
     MOVING OBJECTS
     | Use the arrows keys to move one or more selected objects
     MOVING OBJECTS MOVING SCREEN
     | Moves objects while also moving the window at the same time
     DRAWING
     | For line drawing""")

          self.add('WORKPAD',
                   """
PLACING_INDEXES_ON_THE_WORKPAD/**/
     To place all notes from the stack into the workpad, press F11.
     This will call up a menu, which will let you change the mode of the placement (square or peripheral) and the spacing.
     Pressing F11 a second time will complete the action.
     You can also place notes one by one from the stack at the cursor location by pressing INSERT, or return them to the stack by pressing DELETE.""")

          self.add('WORKPAD',
                   """
WORKPAD_COMMAND_MENU/**/
     When not in the drawing mode, press SHIFT F12 to call up the workpad command menu.
     In the drawing mode, the drawing command menu will be displayed.""")

          self.add('WORKPAD',
                   """
DRAWING_MODE/**/

     The drawing mode allows you to draw on the screen using Unicode characters.
     Several different line types are available, as well as other Unicode characters, and the line character changes to maintain continuity.
     Other features include a “symmetry” mode, which allows you to draw symmetrically repeating patterns, a fill-mode, and the capacity to select objects, and then stretch, contract, flip, cut, paste, and move them. 
""")

          self.add('WORKPAD',
                   """
THE_WORKPAD_NOTE_EDITOR/**/
     Press F2 to create a new note. The new note will be placed in the topmost corner.
     Use the arrow keys to adjust the size of the note.
     The cursor will appear in the top section of the note.
     Enter keywords, separated by spaces, and then press F1 to begin the main body of the note, and press F1 to conclude the note.
     A menu of note entry commands appears automatically.""")

          self.add('WORKPAD',
                   """
SAVING_WORKPADS_TO_SHEETSHELF/**/
     The sheetshelf allows you to save workpads and share them between different documents.

     To save the current workpad to the sheetshelf, use to command "tosheetshelf", which accepts as values the name of the pad which you want to save as well as the name that it should be saved as in the sheetshelf.
     The first value defaults to the current pad, and the second to the name of the pad.
     The name of the notebook is automatically added to the padname in the sheetshelf.

     The command "selectsheet" selects a sheet from the shelf, and activates it as the current pad.
     It accepts as a value the name of the pad that this will be opened as, defaulting to “default.”


     The command "closesheetshelf" closes the sheetshelf.

     When you exit the workpad, you will be given the option of updating the sheetshelf with the changes that have been made to the workpad.
""")
          self.add('NOTESCRIPT',
                   """
NOTE_AND_NOTESCRIPT/**/
     The most fundamental principle of ARCADES is the convertability of note and notescript.
     Every note, or collection of notes, can be exported as a user-readable notescript, and these can in turn be imported and converted back into notes.
     This not only makes it possible to exchange notes with other users, but also makes the process of notetaking independent from the software.
     It is possible, indeed, by marking up an existing text, to convert it into notes.
     And it is also possible to record notes using a simple text editor or word processor, or even to automate the generation of notes.
     Finally, the notescript codes can be included in the text of notes entered through the system, allowing, in effect, for the embedding of one note within another.""")

          self.add('NOTESCRIPT',
                   """
NOTESCRIPT_FORMATTING_CODES/**/
     When ARCADES reads a notescript, it extracts all the elements of the text that begin with a left arrow bracket (<) and ends with a right arrow bracket (>).
     These extracted elements constitute notephrases. Notephrases are interpreted according to the initial element immediately following the bracket.
     If the notephrase begins with DOLLAR ($), PLUS (+), DASH (-), then it modifies the keywords.Dollar, followed by a list of keys, resets the keywords.

     PLUS, followed by a list of keys, adds new keywords.
     DASH deletes the last keyword from the list of keywords.
     If the notephrase begins with AT+ INDEX + AT, a DOUBLE APOSTROPHE (“), a SINGLE APOSTROPHE (‘), a CARET (^), a SEMICOLON (;), or no special symbol, then it adds a note with the given keywords, and with the text following these special marks.
     AT+ INDEX + AT| Adds TEXT at INDEX
     SINGLE APOSTROPHE + TEXT | Adds TEXT at a sibling index.
     DOUBLE APOSTROPHE + TEXT | Adds TEXT at a child index.
     SEMICOLONE + TEXT | Adds TEXT at the previous letter.
     Finally, a note beginning with STAR (*), adds a complete note, with keywords and text.
     The keywords and the text are separated by a semicolon.""")

          self.add('NOTESCRIPT',
                   """
EMBEDDING_NOTESCRIPTS_IN_NOTES/**/
     A Notescript can be embedded in the text entered through the text inputter.
     While a reasonably long notescript can be entered this way, it is not recommended.
     This feature can also be used to input an impromptu note while composing another note.""")

          self.add('NOTESCRIPT',
                   """
LOADING_NOTESCRIPTS/**/
     For longer notescripts, it is recommended to use the "loadtext" command.
     If no file is entered after the colon, then it will call up the menu.
     The command loadtext accepts one value, and three modifies: /$, /&, and /*
     The value identifies the name of the file to be loaded, whereas the modifier /$ is used to suppress the inclusion of default keys, /& is used to include a project, and /* to only load the project and not the notes.
""")

          self.add('NOTESCRIPT',
                   """
OUTPUTTING_NOTESCRIPTS/**/
     The command "formout" generates and saves a notescript.
     It accepts four values: the collection of indexes to be converted, the filename, and Boolean values to indicate if the metadata and indexes are to be included.
     These last values can also be indicated, respectively, with the modifiers /$ and /&.
     You will also be asked if you wish to include the “projects” in output.""")
          

          self.add('LINK',
                   """
LINKING_NOTES/**/
     If the index of a note in the notebook is entered as a keyword, it automatically becomes a link, establishing a connection between the note in which it was entered as a keyword and the note to which it refers.
     Links are unidirectional; they point one note to another note.
     ARCADES keeps track of these indexes, and automatically changes them when the note to which they refer has been changed.""")

          self.add('LINK',
                   """
AUTOMATIC_LINKING/**/
     In addition to entering links manually, either when first composing the note or with subsequent editing, ARCADES also offers several tools for quickly linking notes together.
     These include some functions which apply to existing notes, and others which can be used when entering a series of notes for the first time.""")

          self.add('LINK',
                   """
COMMANDS_FOR_LINKING_NOTES /**/
     The command "link" takes a group of notes and links each note to all the other notes.
     If, for example, you were to link notes at indexes 1,2,3,4,5,6,8,9,10, then each of these notes would have 9 links, and hence 9 keywords, added to it.
     Because the number of additional keywords added to each note increases in direct proportion to the number of notes being linked, this function is limited to 10 notes.
     If you try to link more than this, it will yield an error.
     The command "chain" can be used to enchain a series of notes, linking each note to the next.
     For example:
     chain:1,2,3,5,6 |links 1 to 2, 2 to 3, 3 to 4, 4 to 5, 5 to 6.
     chain:1,6,2,5,3,4 |links 1 to 6, 6 to 2, 2 to 5, 5 to 3, 3 to 4
     chain:1-10 |links 1 to 2, 2 to 3, …
     The loop creates a chain, and then links the last note in the chain to the first.
     For example:
     loop:1,2,3,5,6 |links 1 to 2, …, 5 to 6, 6 to 1

     To remove links, you can delete links manually, or use unlink, which removes all the links from the range that has been entered.""")

          self.add('LINK',
                   """
AUTOMATICALLY_LINKING_DURING_ENTRY /**/
The command startlinking links all the notes that are subsequently entered. The command startlooping, likewise, initiates a loop. To terminate, use endlooping or endlinking.""")

          self.add('SEQUENCE',
                    """
SEQUENCES/**/
     ARCADES recognize sequences as a special class of keywords. A sequence combines a keyword with an instance of a sequence value – a member of a set of well-ordered values, such as strings, real numbers, dates, or even indexes. 
""")
          self.add('SEQUENCE',
                   """
BASIC_SYNTAX_FOR_SEQUENCES/**/
     A sequence-keyword consists in a keyword and a sequence-value, separated by AT (@) and with an optional type-designator placed before the sequence-value.
     The type-designator is used only if the sequence-value is a date or an index. Strings and real numbers are recognized automatically.
     Integers are recognized as real numbers, and represented as “floating point values.”
     For example:
     page@1, page@80, page@99.7
     Strings are also automatically recognized. String sequences can be used to associate alphabeticallysearchable labels—titles, names—with notes.
     While “Heidegger” or “Hegel” could be entered as simple keywords, you could also add them in as name@Heidegger, name@Hegel, or philosopher@Hegel.
     And then, in turn, you can search for notes with names starting with an “h”.
     To enter a date, use the at-symbol and POUND-symbol (“@#”), followed by YEAR, MONTH, and DAY, separated with hyphens.
     For example:
     date@#1970-01-07, date@#1770-03-20, date@#1970,date@#1950-01
     To enter an index, use the at-symbol followed by an underline (“@_”),
     For example:
     index@_1.1.1, index@_1.2.3, mynote@_13.13.13
""")
          self.add('SEQUENCE',
                   """
INITIATING_SEQUENCES/**/
     Sequences are initiated simply by entering a new sequence-keyword into the database either when composing a new note or editing the keywords of an existing notebook.
     As soon as a sequence is initiated, ARCADES starts recording all the sequence-values associated with that keyword.
     Please note that, while any keyword can be associated with any sequence type, once a certain keyword has been associated with a certain sequence type then only this will be recognized.
     If, for example, you enter date@1970-01-01 with the POUND missing, then it will be recognized as a string, not as a date.
     If you follow the correct syntax on subsequent notes, they will not be included in the sequence.
     The sequence will still appear as a key-word, and yet it will be accessible through the sequence-search function.""")

          self.add('SEQUENCE',
                   """
KEEPING_TRACK_OF_SEQUENCES /**/
     To view all of the sequences in the notebook, use the showsequence command.
     The showsequence command also offers the option of “correcting” sequences by deleting them, making it possible to reinitiate the sequence.
     This should be used sparingly---only if a mistake has been made initiating a sequence. """)

          self.add('SEQUENCE',
                   """
SEARCHING_FOR_SEQUENCES /**/
     It is possible to search over keyword-sequences, finding all the notes with values associated with a given keyword falling within a certain range.
     If you are searching for an index or date sequence, you should use POUND or UNDERLINE after the ATSIGN.
     The basic syntax for a sequence search is:
     <SEQUENCE@VALUEFROM/SEQUENCE@VALUE2>.
     This fetches all the sequence keys with values greater than equal to VALUEFROM and less than equal to VALUE2.
     To search for values greater than or less than, respectively, use <[ or ]>.
     For example:
     <[SEQUENCE@VALUEFROM/SEQUENCE@VALUE2]>.
     To retrieve a single sequence key, enclose the single sequence key in brackets, as follows:
     <[SEQUENCE@VALUE]>
     To find all values for a given sequence, you need enter <SEQUENCE@TYPEMARK>, where the TYPEMARK is one of the following:
     ^ | floating point sequence
     $ | string sequence
     # | date sequence
     _ | index sequence
     + | integer sequence """)

          self.add('DEFAULTKEYWORDS',
                    """
DEFAULT_KEYWORDS /**/
     If you are entering a series of notes on the same topic, you may set default keywords which will be automatically added to the note. The default keywords are displayed before the command prompt.
     To add default keys, use addkeys; to add a single key, use addkey, to delete the most recently added key, use deletekey.
     To clear all defaultkeys, use clearkeys; and to revise the default keys, deleting a selection and then adding new keys, use deletedefaultkeys.
     The default keys are stored as a list, not a set: it is possible to have redundancies, though these will be eliminated when the keywords are added to a note, since the keywords of a note are stored as a set.

""")
          self.add('DEFAULTKEYWORDS',
                   """
ADDING_NEW_DEFAULTKEYWORDS /**/
     The command newkeys can be used to load keywords stored as a “key macro” (See sect. 2.13.1.3) into the default keywords.
     It accepts one value, the name of the macro, and the modifier /$, which can be used to keep the existing default keywords.
""")
          self.add('DEFAULTKEYWORDS',
                   """
GRABING_KEYWORDS_FROM_A_NOTE /**/
     The command grabkeys can be used to load keywords stored in a single note or a collection of notes.
     It accepts one value, the collection of indexes of the notes to be loaded, and the modifiers /$, which excludes “all-cap” keywords, and the modifier /&, which excludes capitalized keywords.
""")

          self.add('DEFAULTKEYWORDS',
                   """
DEFAULT_KEYWORD_SEQUENCES /**/
     Sequence keywords can be used as default keywords. If you enter a keyword sequence with a determinate value, such as “book@5”, then the specific value will be included in every new note.
     If, however, the determinate value is replaced with a question mark (?), then ARCADES will ask for t0he value when the note is entered.
     If, when queried, a series of values are entered separated by commas, then ARCADES will create a separate sequence keyword for each value.
     If two values are separated by a dash or, in the case of dates, a slash, then two sequence keywords will be created, one ending with “from” and one with “to.” This feature is especially useful for bibliographic entries. 
""")

          self.add('DISPLAY',
                   """
DISPLAYING_KEYWORDS /**/
     The following binary commands can be used to determine how keys are presented when notes are displayed.
     (1) "showtags"
          |Includes tags when displaying keys
     (2) "orderkeys"
          |Arrange the keys by increasing frequency.""")

     

          self.add('DISPLAY',
                  """
MODIFYING_DISPLAY_OF_NOTES/**/     The following commands, each of which accepts a single integer greater than equal to zero as a value, can be used to modify the appearance of the note text.
     (1) "header"
     | adds lines to the head of the note text
     (2) "footer"
     | adds lines to the tail of the note text
     (3) "leftmargin"
     | adds spaces to the left margin of the note text
     There is also a single binary command, rectify, which equalizes the width of the head (containing the keywords) and the body (containing the text) of the note""")

          self.add('DISPLAY',
                   """
NOTE_IDENTATION/**/
     When displayed either individually or as part of a tribe, so long as the “automulti”-mode is suspended, notes are indented in order to indicate the size of their index.
     The degree of identation can be adjusted using the command indentmultiplier""")

          self.add('DISPLAY',
                   """
SHOWING_ALL_NOTES/**/
     The "all" command can be used to display all the notes in the notebook.
     If your notebook contains many notes, it may take a bit of time to run the first time it is used, but it saves the results to a buffer which may be retrieved subsequently.
     The command all, in addition to being restricted to a certain index range, accepts a single value and several modifiers.
     The optional value indicates the size of the indexes to be listed; all indexes must be less than this value.
     If no value is listed, then notes with indexes are all sizes will be displayed.
     Modifiers include: /& /? /=
     1) /& Excludes non top-level notes.
     2) /* Excludes square characters around notes – allowing format to be outputted in a form that can be copied into other programs.
     3) /? Suspends the automatic short mode
     4) /= Includes dates with the notes
""")
          self.add('DISPLAY',
                   """
     THE_ALL_AND_DISPLAY_BUFFERS/**/The “display”-buffer, to which the “regular”-mode outputs, can be presented by entering a double DOLLAR ($$).
     The “display”-buffer, to which the “regular”-mode outputs, can be presented by entering a single DOLLAR ($).
""")
          self.add('DISPLAY',
                   """
SCROLLING_THROUGH_THE_LIST_OF_NOTES/**/
     If many notes are listed, they will not be shown all at once, but will be presented through a menu that allows you to scroll back and forth between them.
     If you do want to list all notes, press A[ll], whereas to change the number of entries shown, press C[hange]; the arrow keys advance forward and backward, while double arrows go to the first or last page of entries.
     [Q]uit returns to the command prompt.

""")

          self.add('DISPLAY',
                   """
THE_SHOW_COMMAND/**/
     The "show" command can be used to show a smaller group of notes.
     It accepts one value: the collection of indexes to be shown.
""")
          self.add('DISPLAY',
                   """
DISPLAYING_A_SHEET_OF_NOTES/**/
     The “multi” mode fits notes together into a “sheet,” according to their width.
     The notes are placed in a stack, with the largest possible note that can fit in the free area withdrawn from the stack.
     The output of the multi display is stored under a user-defined name, and can also be saved as a text file.""")
          self.add('DISPLAY',
                   """
THE_MULTI_COMMAND/**/
     The syntax consists in four values, and three modifiers:
     multi:INDEX COLLECTION;DISPLAY STREAM;WIDTH;SAVE STREAM /* /? /=
     The first value indicates the indexes to be displayed; the second the name of the “stream” to which isplay will be outputted, and the third the width, in characters, of the display.
     The /$ modifier shows notes in a uniformly small size, as defined using the command smallsize.
     The /* modifier is used to activate the “vary”-mode, adjusting the size of the notes according to the length of the text string.
     The /? pauses the display after each line.
     The /= saves the output to a textfile, using either the name of the display stream or name entered as value 4.""")
          self.add('DISPLAY',
                   """
STREAMS/**/
     To list all the active streams, enters "streams".
     To display an active stream, enter "showstream:STREAM".
     The /? modifier can be used to pause.
     To delete an active stream: enter "deletestream:STREAM"
""")

          self.add('NOTEBOOK',
                   """
THE_NOTEBOOK/**/
     A notebook consists of a collection of notes with unique indexes.
     It is impossible to assign two different notes to the same index, but beyond this there are no restrictions on the indexes that are permitted.
     They could, for example, all have values between 1 and 2, or start with 20000.
     It is also not necessary that any of the notes be of size 0, or that parents exist for children, or older siblings for younger. 
""")

          self.add('NOTEBOOK',
                   """
ORGANIZING_THE_NOTEBOOK_WITH_FIELDS/**/
     Fields, explained above may be used to structure the notebook as a whole by dividing it up into different regions.
""")

          self.add('NOTEBOOK',
                   """
MARKED_NOTES/**/
     ARCADES keeps track of marked notes, and allows the indexes of marked notes to be used as the value of command.
     To mark an individual note at the current location, use the command left bracket ([]. To unmark an individual note, use the command right bracket (]).
     It is also possible to mark notes as a group by using the command "addmarks", unmark notes using "deletemarks", clear all the marks with "clearmarks", and, finally, marked to display all the indexes of marked notes.
""")
          self.add('NOTEBOOK',
                   """
SUSPENSION_OF_ITERATION/**/
     When the con-mode is not activated, ARCADES will move through the notes whenever you press RETURN.
     This function, however, is automatically suspended whenever you enter a note, either until you press RETURN, or enter a command, ten times in succession, or enter a backslash (/).
     There are two basic modes of moving through the notes: iteration and branching.
     Iteration involves moving according to a rule through the indexes contained within the scope of iteration.
     Branching involves moving to a note that is related to the current note.
     The flashmode allows you to flip through a stack of multi-sided flashcards.
""")
          self.add('NOTEBOOK',
                   """
ITERATION_BEHAVIOR/**/
     The behavior of ARCADES in the iteration mode depends on two things:
     1) The “rule” determining movement. (The iteration-rule)
     2) The content of the iterator-sequence. (The iteration-content)
     ARCADES defaults to the iteration mode, with the iteration-content comprising all positive-valued indexes, regardless of their size, and the iterator-rule consisting in moving to the note whose index is the “closest” index greater than the current index. 
""")
          self.add('NOTEBOOK',
                   """
THE_REGULAR_ITERATION_MODE/**/
     In the regular mode of iteration, ARCADES advances either backwards or forwards, and by either one index or more than one index.
     The behavior of the regular mode is thus determined by the direction and depth.
     The direction defaults to forward, moving to a greater index value, and the speed defaults to one, advancing to the first closest index.
     The tilt determines whether it advances to parents/children, older or young siblings, or is neutral, and defaults to the neutral mode.
     The fourth factor determining the behavior of the regular iteration mode is the depth, which defaults to 0. 
""")
          self.add('NOTEBOOK',
                   """
CHANGING_DIRECTION_DURING_ITERATION/**/
     The commands for changing direction are the left arrow bracket (<) to move backwards, and right arrow bracket (>) to move forwards.
""")
          self.add('NOTEBOOK',
                   """
ITERATOR_DEPTH/**/
     If the depth is 0, then the iterator iterates over notes with indexes of any size; if it is greater than 0, then it only iterates over notes whose indexes are less than the depth.
     The depth can be set directly with the command "depth". It can also be increased or decreased with "deeper" or "shallower".""")

          self.add('NOTEBOOK',
                   """
THE_RANDOM_MODE/**/
     In the random mode, ARCADES advances randomly (pseudo-randomly, that is) through the indexes in the iterator-sequence until it has passed through all of them.
     Use the "randomon" to activate the random mode, and "randomoff" to deactivate it.

""")
          self.add('NOTEBOOK',
                   """
DETERMINATION_OF_THE_ITERATOR_SEQUENCE/**/
     The iteration-sequence defaults to all the notes with positive values, but it is also possible to iterate over a subset of the notebook.
     This is done by redefining the flipbook; whenever the flipbook is redefined, then the iterator-sequence is automatically reset. 
""")
          self.add('NOTEBOOK',
                   """
FLIPOUT/**/
     The binary "flipout" command activates the flipout-mode. When then flipout-mode is activated, then the results of searches are sent to the flipbook, which is reset accordingly
""")
          self.add('NOTEBOOK',
                   """
SETTING_THE_FLIPBOOK_MANUALLY/**/
     The flipbook can also be manually set by using the "flipbook" command.
     The flipbook command can accept as a value either a collection of indexes, or a list of fields.
     If entered as a simple command, without any value, then flipbook resets the flipbook to all the positive indexes in the notebook. """)
          self.add('NOTEBOOK',
                   """
REFEEDING_INTO_THE_FLIPBOOK/**/
     It is possible to feed the results of other commands to the flipbook, provided that they yield a collection of indexes.
For example:
(1) marked =>flipbook:?
     | Feeds the marked notes into the flipbook.
     | Equivalent to flipbook:[?]
(2) search:VALUE=>flipbook:?
      | Feeds a search result into the flipbook.
      | Equivalent of “flipping out” a search
      | Also equivalent to flipbook.

""")
          self.add('NOTEBOOK',
                   """
DESCENDENTS/**/
     Because ARCADES allows for hierarchical structures, you may wish to reset the sequence-iterator not to a group of notes defined by a range of indexes, but to all the descendants of a given index.
     This can be achieved with the "descendants" command.
     When this command is used, it not only resets the flipbook, but it also indicates the value that has been entered after the command prompt.
     It will now be possible to enter this value, which all the indexes in the flipbook start with, simply by using a single period.
     To restore the sequence-iterator to all the indexes in the notebook, enter descendants without a value.

""")
          self.add('NOTEBOOK',
                   """
FLIPPROJECT_AND_CLUSTER/**/
There are two additional flipbook functions which will be discussed in the context of advanced features.
These include: flipproject (see section 2.9), which sends the indexes in the current project to the sequence-iterator, and the cluster function (see section 2.8.4.)

""")
          self.add('NOTEBOOK',
                   """
MANUAL_ITERATION/**/
     In the iterator-mode, ARCADES always advances to the “next” note according to the direction, speed, and rule, and the content of the iterator sequence itself.
     It is, however, also possible to navigate manually through the iterator-sequence with the following commands.
     (1) period
     | moves forward one index
     (2) comma
     | moves back one index
     (3) period*N | moves forward by N indexes
     e.g. ……. | moves forward by 7 indexes
     (4) comma*N | moves back N by indexes
     e.g. ,,,, | moves back by 4 indexes
     (5) first
     | goes to the first note in the iterator sequence
     (6) last
     | goes to the last note in the iterator sequence
     (7) hop:N
     | moves forward by N indexes
     e.g. hop:5 | moves forward by 5 indexes
""")
          self.add('NOTEBOOK',
                   """
BRANCHING_MODES/**/
     Those of us who grew up with personal computers in the 80s may remember a simple text-based game where you chase a monster through a labyrinth of caves connected to each other through passageways.
     This game, a simple application of graph-theory, indicates a powerful way of thinking of the organization of a notebook.
     Up until this point we’ve been considering a notebook primarillly as a collection of notes identified through indexes, where the relations of these notes to one another is entirely a function of the relation of their indexes.
     As different as the various modes of iteration are from one another, they all share this way of conceiving what a notebook is.
     The iteratorsequence is a collection of indexes, and moving through the notes means moving through the indexes.
     But it is also possible to think of notes as relating to other notes through their own content.
     This content includes every attribute of the note – its keywords, its text, its metadata, and also its index value.
     From such a perspective, indeed, the iterating mode may itself be seen as a special case of this second, and more general organizational logic.
     Because each note has only one index, and because all indexes form a well-ordered series, it becomes possible, by abstracting away from all other attributes of the note, to precisely define a collection of indexes and a rule (even if only the “rule” of randomness) governing the movement through them.
     But this is in turn limiting: not least of all, it restricts the organizing principle to what has been established, in advanced, by the user.
     Once you consider notes as related by their content, it then becomes possible to conceive of having a multitude of different affinities.
     These include affinities which are:
     1) based on keywords, including links and other keywords.
     2) based on common words in the text.
     3) based on the date of composition.
     The branching mode implements an organizational logic based on these different kinds of affinities.
     It allows you, in other words, to move from one note to another note chosen from among a set of the notes to which it has affinities according to a well-defined rule.
     We might indeed distinguish between affine notes and kindred notes.
     Kindred notes are related by their respective indexes– and indeed, as explained above, all notes within a notebook have some kind of kinship between them.
     Affine notes are related by their respective attributes.
     Strictly affine notes involve an affinity that is not simple kinship – that doesn’t involve just the index value.
     If notes are strictly affine, then their affinity remains the same even if they are moved to different locations.
     Hence, links, even though expressed through indexes, in fact involve a strict affinity, since the link is actually merely a “pointer” to the transposition table.

""")
          self.add('NOTEBOOK',
                   """
ACTIVATING_A_BRANCHING_MODE/**/
     To activate or deactivate the branching mode, use the binary "iteratemode" command.
     Use the commands "branchone", "branchtwo", and "branchthree" to select between the different branching modes
""")
          self.add('NOTEBOOK',
                   """
THE_THREE_BRANCHING_MODES/**/
     The first branching mode moves randomly to notes that have related keywords.
     The second branching mode moves randomly to related links.
     The third branching mode allows you to move by choice through links

""")
          self.add('NOTEBOOK',
                   """
FLASHCARDS/**/
     Unlike the previous two modes, the flashmode only works on a special type of note: a “flashcard” note.
     The flashmode, which is available only in the iteration mode, allows you to flip over the sides of such flashcard notes. 
""")
          self.add('NOTEBOOK',
                   """
CREATING_A_FLASHCARD/**/
     Flashcards are made by entering in an ordinary note, using /FC/ to separate the sides. If /FC/
     appears twice in the note, for example, then the note will have three sides.
     For example:
     <man /FC/ der Mensch /FC/ l’homme /FC/ il uomo>
     | Defines a 4 sided flashcard with the English, German, French, and Italian words for “man”

""")
          self.add('NOTEBOOK',
                   """
SELECTING_THE_FLASHCARD_MODE/**/
     The binary command "flashmode" is used to enter or exit the flashmode. In addition to this, you will also need to set the number of sides of the flashcard by using the command "setsides", which defaults to two.
     To adjust when the flashcards advance, and which card they start with, use "setflipat".
     When the flashmode is activated, ARCADES will advance through the sides of each note before moving on to the text note in the iterator.

     The flashmode operates within the iterator mode, and all the regular features of the iterator mode remain the same as before.
     The flashmode, indeed, does nothing more than add an additional requirement that must be fulfilled before the iterator advances.

""")
          self.add('NOTEBOOK',
                   """
     OTHER_FLASHCARD_COMMNADS/**/
     The use of the following commands do not require that the flashmode is activated.
(1) "noflash"
     | disables the display of flashcards
(2) "flashforward", "ff"
     | advances to the next side
(3) "flashback", "fb"
     | goes back to previous side
(4) "flashreset", "fr"
     | returns to the first side
(5) "flashto", "ft"
     | goes to a specific side
The numeration of sides begins with 0
""")

          self.add('NOTEBOOK',
                   """
ITERACTION_BETWEN_FLASHMODE_AND_ITERATION/**/
     The interaction between the iterator and note entry is subtle, and may take some getting used to.
     It is important to keep in mind, first of all, that while the iteration is confined to the notes whose indexes are included in the iterator-sequence, notes from throughout the notebook can be displayed, and accessed, and notes can be added anywhere.
     Ordinarily, the index position at which a new note will be added is determined by the iterator as it passes through the iterator sequence, but this is not always the case. 
""")
          self.add('NOTEBOOK',
                   """
ENTERING_AN_INDEX_AS_A_COMMAND/**/
     Any index can be entered as a command.
     If a note with the index is present in the notebook, then this note will be displayed.
     Doing this, however, will not affect either the position of the iterator, or the position at which new note will be added.

""")
          self.add('NOTEBOOK',
                   """
UPDATING_THE_ITERATOR_SEQUENCE/**/
     If you add new notes to the notebook, these will be automatically added to the iterator-sequence.
""")
          self.add('NOTEBOOK',
                   """
SKIP/**/
     By entering the command "skip:INDEX", you can skip to the note at INDEX.
     This INDEX will the become the position for entering a new note.

""")
          self.add('REFEEDING',
                   """
ADVANCED_REFEEDING_COMMANDS/**/
     So as to increase the usefulness of ARCADES’s ability to “refeed” the results of commands, a number of advanced commands are available.
     These allow one to load text files into ARCADES, save them back to the hard drive, or even upload a function written into Python and apply it to the text. 
""")
          self.add('REFEEDING',
                   """
LOAD/**/
     The command "load", which accepts a filename as a value, loads a text file and feeds it into the text command.
     If no value is entered, then it will call up the file menu.
""")
          self.add('REFEEDING',
                   """
SAVE/**/
     The "save" command saves a text file to the disk drive.
     It accepts three values: the text to be saved, the filename, and the folder, which defaults to ‘/textfiles.’
     The "save" command can be used both to save the text of a note, as well as formatted output, and hence can be combined with a variety of other commands, including "show", "multi", and also "explode". 
""")
          self.add('REFEEDING',
                   """
ECHO/**/
     The command "echo" simply prints the text in the value. It can be used with loadtext, and is also a useful way of inspecting the output sent to variables. 
""")
          self.add('REFEEDING',
                   """
USER_DEFINED_PYTHON_SCRIPTS/**/
     ARCADES allows you to apply user-defined Python scripts to process text.
     The script in question should be a function, named “generic,” that accepts a single string as its value and returns a single string, and it should be saved as a “.py’ file in the “/programs” folder.
     To apply the program to text, simply use the "run" command, which accepts two values: the name of the program, and the text itself to be processed.
     The text can be entered directly, but you can also use a variable or the quadruple question marks. 
""")
          self.add('REFEEDING',
                   """
INTERPRET/**/The command "interpret" can be used to interpret the text of a notescript given as the value.
""")
          self.add('REFEEDING',
                   """
RUNINTERPRT/**/
     The command "runinterpret" combines "loadtext" and "run": it interprets a text file after having applied a Python script to it.
     The command "runinterpret" accepts two values: the name of the file, in the directory “/programs”, of the program to be run, and the name of the text file to which it is to be applied.
""")
          self.add('REFEEDING',
                   """
EXPLODING_A_NOTE/**/
     The command "explode" yields an index, keyword list, and text from a single note, which in turn can be accessed with single, double, and quadruple question marks.

""")
          self.add('REFEEDING',
                   """
INVERTING_A_NOTE/**/
     The command invert takes a list of indexes and yields a list of all the indexes that are contained in the notebook yet not in the list.
""")
          self.add('REFEEDING',
                   """
REFEEDING_KEYS_INTO_ANOTHER_COMMAND/**/
     The command keys (alternative forms: key, k) can be used to refeed a collection of keys into another command.
     It accepts one value – the collection of indexes from which the keys are to be taken and the modifiers /$, /&, /*, /?.
     The modifier /$ generates a histogram from the keys, whereas the modifiers /&, /*, and /?, are used, respectively, to include “all-cap,” capitalized, and lower-case keywords.
     If neither of these three modifiers are invoked, then it will show all keywords.
     This generates a search phrase, which can be refed into another command by using double question marks (??).

""")
          self.add('REFEEDING',
                   """
REFEEDING_TAGS/**/
     The command tags (alternate forms: tag, t) displays the tags from a collection of indexes, given as its first value.
     This generates a search phrase, which can be refed into another command by using double question marks (??).

""")
          self.add('REFEEDING',
                   """
REFEEDING_TEXT/**/
     The command "text", which accepts three values and the modifiers /$, /&, and /*, is used to show the most relevant words in a text, determined according to either their frequency in the note, their scarcity in the notebook, or both.
     The first value is the collection of indexes, the second value is the number of words according to frequency in text, and third value is the number of words according to their scarcity in the notebook.
     The modifier /$ presents the intersection of both sets, while the modifier /& presents them by decreasing frequency in the notebook and /* by increasing frequency in the text of the selected notes.

""")
          self.add('MACROS',
                   """
MACRO_FUNCTIONS/**/
     ARCADES offers various different kind of simple macros, which can be used for entering commands, keywords, and text. These include:
     (1) codes | used to define special codes for text entry.
     (2) macros | used as shorthand in entering text.
     (3) keymacros | used in entering keywords.
     (4) command macros | used for entering commands.
     In addition to these macros functions, other features in ARCADES share similar functionality.
     These are:
     (5) key definitions | used to automatically assign keywords to text.
     (6) knowledge | the “knowledge base” for defining metatags.
     (7) spelling | words added to the spelling dictionaries.
""")
          self.add('MACROS',
                   """
BASIC_MACRO_FUNCTIONALITY/**/
     The following is an account of the basic functionality of codes, macros, key macros, and command macros.
     The treatment of the key definitions, knowledge base, and spelling dictionary will betreated separately
""")
          self.add('MACROS',
                   """
CODES/**/
     Codes are used for entering special characters, and especially those which have a reserved function in ARCADES, such as the left arrow (<) and right arrow (>).
     4 codes are predefined in ARCADES:
     (1) < = /060/ (2) > = /062/.
     (3) { =/123/ (4) } =/125/.
     The use of the slash is not inherent to a code. But it is recommended that you only define codes that are unlikely to appear in ordinary text.

""")
          self.add('MACROS',
                   """
MACROS/**/
     Macros are used to facilitate entry of commonly used terms. Codes are different from macros in several respects:
     1) There are no predefined macros.
     2) To be invoked, a macro must be preceded by an underline (_) .
     3) When defining codes, the “from” and “to” seem to be reversed.
     This last point is a bit tricky and confusing. The reason has to do with the fact that, in the case of codes, the code itself is the expansion of the symbol to which it correlates. 
""")
          self.add('MACROS',
                   """
KEYMACROS/**/
     Key macros are used specifically for facilitating the entry of a sequence of keywords.
     They offer an alternative to default keywords and projects.
     If you are simultaneously working on several different notetaking projects at once, it might make sense, instead of constantly switching between projects, to define a key macro.
     Once a key macro has been defined, it can be invoked, when entering keywords, by preceding it with a DOLLAR ($). 
""")
          self.add('MACROS',
                   """
COMMAND_MACROS/**/
     Command macros can be used either to redefine commands, or facilitate the entry of a string of commands.
     It is recommended, indeed, either only to use unusual terms for command macros or to precede them with some symbol, such as a DOLLAR.
""")
          self.add('MACROS',
                   """
SPECIAL_COMMAND_MACRO_CODES/**/
     ARCADES offers some special codes for entering more sophisticated command macros.
     To activate these, the entire command macro must be preceded by an AT.
     These include:
     (1) FIRST |the first index
     (2) LAST | the last index
     (3) FILE | the name of the current file
     (4) BACKUP | the current filename combined the current date
     (5) NOW | POUND + the current date
     It is also possible to include queries, simply by including the query phrase in square brackets.
""")
          self.add('MACROS',
                   """
BASIC_MACRO_COMMANDS/**/
     ARCADES offers four classes of commands for managing macros: change, default, record, clear.
     Each of these combines with the four types of macros to yield sixteen distinct commands:
     (1) changecodes.
     (2) changemacros.
     (3) changekeymacros.
     (4) changecommandmacros.
     (5) defaultcodes.
     (6) defaultmacros.
     (7) defautkeymacros.
     (8) defaultcommandmacros.
     (9) recordcodes.
     (10) recordmacros.
     (11) recordkeymacros.
     (12) recordcommandmacros.
     (13) clearcodes.
     (14) clearmacros.
     (15) clearkeymacros.
     (16) clearcommandmacros.
""")
          self.add('MACROS',
                   """
LOADING_MACROS_FROM_NOTES/**/
     In addition to entering macros through the console, it is also possible to load macros from notes contained within a notebook.
     These notes can, likewise, be easily transferred between notebooks (using formout and loadtext).
     The “default” commands all work in the same way.
     They search for all the notes in the notebook with a certain identifying keyword, and then interpret the text contained in these notes.

     The identifying keyword consists in two parts: an identifying key, and an optional suffix.

     The identifying key is simply the type of macro written out in all-caps.
     (1) codes | CODES.
     (2) macros | MACROS.
     (3) keymacros | KEYMACROS.
     (4) commandmacros | COMMANDMACROS.

     The suffix is Unicode-8 string that can be entered through the terminal, excluding special characters that would interfere with keyword entry such as SLASH (/), PERIOD (/), COMMA (,), or AT (@).
     Valid suffixes include:
     (1) | 1
     (2) | frog
     (3) | $
     (4) | This is a suffix

""")
          self.add('MACROS',
                   """
DEFAULT_NOTE_TEXT/**/
     The text of the default note consists simply in a list of “equations.”
     It is important to avoid spaces within the equation, since these will be interpreted as demarcating separate codes.
""")
          self.add('MACROS',
                   """
     While it is possible to clear all entries in a macro through the console, this does not actually destroy and reconstitute an object, as may be necessary if you make changes to the Python modules defining the objects (“abbreviations.py”, “keydefinitions.py”, “keymacrodefinitions.py”).
     To do this, you must use the “clear”-commands.
""")
          self.add('KNOWLEDGE',
                   """
CLEARING_MACROS/**/
     ARCADES offers two different ways of defining relations between search terms. The first is a
     simple classificatory knowledgebase, while the second allows for the definition of relational facts.

""")
          self.add('KNOWLEDGE',
                   """
THE_BASIC_KNOWLEDGEBASE/**/
     ARCADES includes a simple “knowledge base,” which can be used to define ontological facts and apply these in executing searches.
     An ontological fact consists in the knowledge that one kind of thing can be subsumed under another kind of thing. For example:
     (1) a “ontologist” is a “philosopher”
     (2) a “philosopher” is a “theorist”
     (3) a “theorist” is a “scientist”
     (4) a “scientist” is a “thinker”
     (5) a “thinker” is a “human being”
     (6) a “human being” is an “animal”
     (7) an “animal” is a “living being”
     (8) a “living being” is a “being”
     Given these definitions, it would then be possible to search for all “ontologists” by searching for “scientist” or “human being” or even “being.”
     And we might add these two further definitions:
     (9) an “oncologist” is a “medical doctor”
     (10) a “medical doctor” is a “scientist”
     Then “scientist” would search for both “ontologist” and “oncologist.”
     The lowest level classification (“ontologist”) is a “tag,” where the higher classifications are “metatags.”
     The reason for this distinction, which might seem arbitrary, is because the knowledge base
     and the tags are stored separately. The metatags can be thought of as a classificatory schemes supervening on the keys and tags, and is, indeed, much easier to change and manipulate.
     Knowledge can be easily forgotten without changing the notebook itself!
""")
          self.add('KNOWLEDGE',
                   """
ENTERING_KNOWLEDGE_WITH_KEYWORDS/**/
     It is possible to “teach” ARCADES an ontological fact when entering keywords with tags.
     Simply use EQUAL (=) after the tag, followed by the metatag.
     For example:
     (1) Heidegger/philosopher=thinker
     (2) Rilke/poet=author
""")
          self.add('KNOWLEDGE',
                   """
LEARNING_AND_FORGETTING/**/
     Ontologically facts can be defined directly through the commands "learn" and "forget".
     Both take two values: the lower-level classification and the higher-level classification.
     The command allknowledge presents all the ontological facts that ARCADES has been taught.
""")
          self.add('KNOWLEDGE',
                   """
     The “knowledge base” also has the following console commands, whose operation is completely analogous to the four macros: "changeknowledge", "defaultknowledge", "recordknowledge", "clearknowledge". 
     Knowledge is recorded using EQUAL (=).
""")
          self.add('KNOWLEDGE',
                   """
THE_GENERAL_KNOWLEDGEBASE/**/
The general knowledge base stores and analyzes knowledge expressed as nodes, with directed and nondirected relations between them, and with attributes attached to them.
This knowledge can be implemented in searches, making it possible, say, to search for all the descendants of Queen Elizabeth, or all the students of Martin Heidegger.
""")
          self.add('KNOWLEDGE',
                   """
PERMANENT_AND_TEMPORARY_KNOWLEDGFBASED/**/
     It is possible to use either a temporary knowledgebase, a knowledgebase attached to your notebook, or a knowledgebase common to all notebooks.
     Upon starting up ARCADES, you have the option of which to select
""")
          self.add('KNOWLEDGE',
                   """
DIFFERENT_KINDS_OF_RELATIONS/**/
     Knowledge consists in relations between nodes.
     Possible relations include directed, non-directed, reciprocal.
     It is also possible attach a “definition” to a node, and to define complex relations from simpler relations.
     Examples of directed relations are: parent, child.
     Examples of non-directed relations are: sibling, spouse.
     Examples of reciprocal relations are: parent – child
     Examples of complex relations are: grandparent, aunt
     The logical expressiveness of the knowledgebase is currently limited; it is not possible, for example, to give multiple definitions of a complex relation.
""")
          self.add('KNOWLEDGE',
                   """
THE_GENERALKNOWLEDGE_COMMAND/**/
     The simplest way to access the general knowledge base is with the command "generalknowledge" or "gk", which calls up a prompt, which can then be used to directly enter knowledge.
     Command syntax is as follows:
     NODE1,NODE2,NODE2… | Creates one or more nodes
     RELATIONNAME:RELATIONTYPE;CONTENT | Define a new relation

     RELATIONTYPE = DIRECTED,NONDIRECTED,RECIPROCAL,COMPLEX, ATTRIBUTE
     FROMNODE1,FROMNODE2…;RELATION1,RELATION2…;TONODE1,TONODE2…
     | Learn a relation between nodes.

     $ Shows all nodes.
     $$NODE;RELATION1,RELATION2 |Finds nodes related through relations in sequence.
     $$NODE;RELATION* |Find all nodes related by relation to the top node
     $$$ Shows all relations
     $$$$ Display the entire knowledgebase
""")
          self.add('KNOWLEDGE',
                   """
KNOWLEDGE_CALLS_IN_KEYWORDS/**/
     It is also possible to include calls to the knowledge base in the text of a note by surrounding them with double curly braces.

""")
          self.add('KNOWLEDGE',
                   """
KNOWLEDGE_CALLS_IN_THE_KEYWORD_LIST/**/
     A call can be entered as a keyword, either within the text by surrounding with single curly brackets or in the list of keywords.
     IN THIS CASE THE NODE is ALSO ENTERED AS A KEYWORD.
     Here the call syntax is different, and more limited.
     No lists are possible.
     QUESTION MARK is used before the call and between the relation and the content.
     Nodes can be defined, and relations between nodes established, but relations cannot be created.
""")
          self.add('KNOWLEDGE',
                   """
SEARCHING_OVER_RELATIONS/**/
     It is possible to search over the relations of a node. The syntax is ?NODE?RELATION.
     To search for keywords, enclose with <>
""")
          self.add('KNOWLEDGE',
                   """
THE_KNOWLEDGE_CONSOLE/**/
Use the command "changegeneralknowledge" to access the general knowledge console, which offers a variety of options for directly interacting with the knowledge database. 
""")
          self.add('KNOWLEDGE',
                   """
SWITCHING_THE_KNOWLEDGEBAS/**/
Use "switchgeneralknowledge" to switch between the temporary knowledgebase, the common knowledgebase, and the knowledge base attached to the notebook.
""")
          self.add('KEYDEFINITIONS',
                   """
KEY_DEFINITIONS/**/
     ARCADES allows you to load text by paragraph, converting each paragraph into a note, while automatically assigning keywords to each note based on the words that appear in the text. 
""")
          self.add('KEYDEFINITIONS',
                   """
LOADING_RAW_TEXT/**/
     Loading raw text into ARCADES can be initiated through two different commands:
     "loadbyparagraph" and "splitload."
     They differ in only one respect: loadbyparagraph splits up the text using the paragraph mark (“/n”), whereas splitload splits on a user-defined string.
     The command splitbyparagraph accepts one value – the name of the file to be loaded – and the modifiers /$, /&, /*.
     The first modifier is used to suppress the “key” function, which calls up existing keys.
     The “key” function is automatically suppressed if there are more than 50 keys in the notebook.
     The second modifier is used to invoke automatic key definitions. The third modifier is used to repress querying the user to add notes and continue.
     The command "splitload" is similar, except that it accepts, as a second value, the character string used to split the text into paragraphs.
""")
          self.add('KEYDEFINITIONS',
                   """
SETTING_AND_CHANGING_KEY_DEFINITIONS/**/
     The commands "changekeydefinitions", "defaultkeydefinitions", "recordkeydefinitions", and "clearkeydefinitions" can be used to define and change key definitions.
     The formatting of default key definitions is as follows: KEY:DEFINITION1,DEFINITION2,DEFINITION3…
     The “definitions” are the words in the text corresponding to a given key.

""")
          self.add('SPELLING',
                   """
THE_SPELLCHECKER/**/
     ARCADES includes a basic spellchecker, with support for English, French, Spanish, and German.
     The spellingchecker includes the capacity to learn new words, and keeps separate dictionaries for all dictionaries.
     New words can be added during text entry, through a “Console”, or by loading in new words from notes.
""")
          self.add('SPELLING',
                   """
ACTIVATING_SPELLCHECK/**/
     Use the spelling command to toggle the spellchecker on or off.
""")
          self.add('SPELLING',
                   """
SELECTING_THE_LANGUAGE/**/
     The spellchecker allows you to choose between English, French, Spanish, and German.
     To do so, use the language command with “en”, “es”, “fr”, “de” as a value.
""")
          self.add('SPELLING',
                   """
BASIC_SPELLCHECKING_OPERATION/**/
     If the spellchecker is activated, then ARCADES, following text entry, ultimately checks for misspelled words.
     It checks using the dictionary of the language that has been selected, although it automatically switches to German if an excessive number of errors in the other language are present.
""")
          self.add('SPELLING',
                   """
THE_SPELLCHECKING_CONSOLE/**/
     To call up the console, use the command spelldictionary. The console allows you to add new words, delete words, change the language, and display the words that have been added.
""")
          self.add('SPELLING',
                   """
DEFAULT_SPELLING/**/
     The defaultspelling command operates analogously to the “default”-commands for macros, key definitions, and the knowledge base.
     There are only two differences.
     (1) The suffix must contain the language-abbreviation (“en”, “es”, “de”, “fr”) in addition to the optional specifier.
     (2) The text consists simply in a list of words to be added to the spelling dictionary for the language indicated.
         
""")
          self.add('MISCELLANEOUS',
                   """
SETTINGS/**/
     The command "showsettings" can be used to show all the string, integer, and Boolean values stored as persistent properties.
     Most, but not all, of these properties can be manually adjusted.

""")
          self.add('MISCELLANEOUS',
                    """
MISCELLANEOUS_COMMANDS/**/

     BINARY COMMANDS

     (1) usesequence | disables use of sequences
     (2) boxconfigs | displays configuration in a “boxy” way.
     (3) autobackup | disables automatic backup
     (4) curtail | eliminates lines at beginning of note
     (5) showdate | shows dates when displaying note
     (6) showshow | displays all notes in short form
     (7) carryoverkeys | carries over keys from parents to children
     (8) carryall | carries over keys from all parents, or first two parents
     (9) negresults | includes negative indexes in search results

     INTEGER COMMANDS

     (10) trim | sets the length of all keywords when displaying notes as list
     (11) setlongmax | sets the maximum number of notes shown in “long” mode
     (12) smallsize | sets the small size of notes for multidisplay
""")
          self.add('MISCELLANEOUS',
                   """
CONFIGURATIONS/**/
     The commands "showconfigurations" can be used to show the non-persistent attributes of the notebook.

     The commands "saveconfigurations" and "loadconfigurations" can be used to save and load configurations.
     Both accept a single value: the identifier of the configurations. The configurations are save as a .pkl file, with “_config.pkl” automatically added to the identifier to yield the filename.

""")
          self.add('MISCELLANEOUS',
                   """
MENUS/**/
     The command "bigmenu" displays a large menu showing all the commands, while menu calls up a toplevel menu from which the lower-level menus can be selected.
     Both menus can be used to enter commands.
     The bigmenu is so large that it is nearly impossible to get it to display properly without a special monito         
          
     The command help shows the commands, together with information about them, as a series of tables, allow the user to move back and forth between them.
""")
          self.add('MISCELLANEOUS',
                   """
SCIENTIFIC_CALCULATOR/**/
     ARCADES includes a simple scientific calculator, which can be activated with the command "calculate".
""")
          self.add('MISCELLANEOUS',
                   """
TRUTH_TABLE_GERNATOR/**/
     The command "truthtable" can be used to generate truth table from a logical phrase.
     The logical phrase can be entered as a value, or via the prompt. 
""")
          
if __name__ == "__main__":
     tutor = TutorialManager()

     tutor.start()

     tutor.load()
     tutor.all_tutorials()

     while True:
          x= input('?')
          if x:
               tutor.show(x)
          else:
               break
     tutor.stop()
          
