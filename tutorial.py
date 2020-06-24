### Class for managing the automatic tutorial

from display import Display
from globalconstants import ENTERSCRIPT, FORMATTINGSCRIPT, SEARCHSCRIPT


display = Display()
class TutorialManager:

     def __init__ (self):

          self.tutorials = {}
          self.activated = False

     def add (self,header,body):

          if header in self.tutorials:
               self.tutorials[header]['message'].append(body)
          else:
               
               self.tutorials[header] = {'message':[body],
                                         'status':True}

     def show(self,header):
          if self.activated and header in self.tutorials and self.tutorials[header]['status'] and self.tutorials[header]['message']:
               if '┃' not in self.tutorials[header]['message'][0]:
                    display.noteprint(('TUTORIAL for '+header+'!',self.tutorials[header]['message'][0]),param_width=75,override=True)
               else:
                    print(self.tutorials[header]['message'][0])
               entry = input('PLUS+RETURN for advance, \n PLUS+PLUS+RETURN to advance immediately \n'
                             *(len(self.tutorials[header]['message'])>1)
                             +'SPACE+RETURN to stop showing this message,\n'
                             +'or SPACE+SPACE+RETURN to quit tutorial')
               if entry == ' ':
                    self.tutorials[header]['status'] = False
               elif entry == '  ':
                    self.activated = False
               elif entry == '+':
                    self.tutorials[header]['message'] = self.tutorials[header]['message'][1:]
               elif entry == '++':
                    self.tutorials[header]['message'] = self.tutorials[header]['message'][1:]
                    self.show(header)
     def start(self):
          self.activated = True
     def stop(self):
          self.activated = False

     def load(self):
          self.add('INITIATE',
                   'Welcome to ARCADES\n'\
                   +'To enter a note, type "enter"\n'\
                   +'To cycle through notes, press RETURN\n'\
                   +'To show all notes, type "all"\n'\
                   +'To search, type "search"\n'\
                   +'To see all commands, type "help"')
          

          self.add('KEYWORDS',
                   'Enter a list of keywords separated by COMMAS\n'\
                   +'KEYWORDS can consists \n in a single word or phrase\n\n'\
                   +'TO ADD TAGS, use the slash (/) \ntogether with a list'\
                   +'of terms (words or phrases) \nseparated by a PERIOD\n'\
                   +'For a sequence keywords:\n'\
                   +'    KEYWORD@INTERGERorFLOAT\n'\
                   +'    KEYWWORD@#DATE\n'\
                   +'    KEYWORD@_INDEX')

          self.add('KEYWORDS',
                   """
Keywords can be followed with one or more tags,
serving as a further level of classification. The
tags should follow a slash (/); multiple tags
are separated by a period.
So for example:

     Sloth/animal
     Penguin/bird.Arctic.flightless.monochrome
     Emu/bird.Australian.flightless.

Searching for the tag “flightless” would retrieve
notes with the tags “Penguin” and “Emu.”
A given tag need only be associated once
with a give keyword. Or, put another way,
if you search for
a tag it will retrieve all the notes classified with
the keywords associated with it, and not just those
notes in which the association has been made explicit. """)

          self.add('KEYWORDS',
                   """
ARCADES includes two knowledgebases. The first allows for tags
to be classified under higherorder concepts. A single tag
can be classified under an arbitrary number of different
concepts, and an arbitrary number of levels of classification
are permitted, allowing for complex ontological trees to be
superimposed atop the notes. While knowledge may be imputed,
along with keywords and tags, when entering a note,
it is also possible to manipulate the knowledgebase directly discreet
commands or through a special console.

Concepts to be learned are introduced with an EQUAL (=)
following either a tag, or a subordinate concept.

For example:
     Lupu/frog=amphibian=vertebrate=animal=living being=being

ARCADES does not forbid circular assignments, such as, for example:
     Lupu/animal=creature, Girin/creature=animal.

It will automatically stop rather than crash.

The second knowledgebase is used for defining directed
and non-directed relations – such as the relation “child of”,
“parent of”, “teacher of”, or “friend of” – between keywords. 
""")
          self.add('KEYWORDS',
                   """
If the index of a note in the notebook is entered
as a keyword, it automatically becomes a link,
establishing a connection between the note in which
it was entered as a keyword and the note to
which it refers. Links are unidirectional; they point
one note to another note. ARCADES keeps track of these indexes,
and automatically changes them when the note to which they refer has been
changed. """)

          self.add('KEYWORDS',
                   """
If you are entering a series of notes on the same topic,
you may set default keywords which will be automatically
added to the note. The default keywords are displayed
before the command prompt.
To add default keys, use addkeys; to add a single key,
use addkey, to delete the most recently added key, use "deletekey";
to clear all defaultkeys, use "clearkeys"; and to revise
the default keys, deleting a selection and then adding new keys,
use "deletedefaultkeys". The default keys are stored as a list, not a
set: it is possible to have redundancies, though
these will be eliminated when the keywords are added
to a note, since the keywords of a note are stored as a set.""")
          

          self.add('ESCAPE',
                   'PRESS / to go back to cycling through notes\n')

          self.add('CONESCAPE',
                   'PRESS ;; to exit from CONCHILD or CONNEXT')
          self.add('SEARCH',
                   SEARCHSCRIPT)
          self.add('FORMATTING',
                   FORMATTINGSCRIPT)
          self.add('ENTERING',
                   ENTERSCRIPT)
          self.add('INITIATE',
                   """
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
ARCADES does not require that notes be assigned
to sequential indexes. It is perfectly acceptable
to have a notebook consisting of the indexes
1, 13, 1999, or, say, only of indexes with prime
numbers. And it is also perfectly acceptable
to have orphans – notes without a parent.
Nevertheless, unless you opt to assign the index
manually when entering new notes, ARCADES will
automatically assign the index value. The basic entry
function (+) will assign the new note either to
the closest sibling of a “top-level” note, or to
the closest mate of a note with size > 0. For example:
1 => 2; 2.1 => 3. The “next” entry function (++)
will assign the new note to the soulsister, or
closest available sibling, of the last note.
For example: 1 => 2, 2.1 = 2.2, 3.3.1 => 3.3.2.
The “child” entry function (+++) will assign the
new note to the first child, or the closest child.
1 => 1.1, 2.1 = 2.1.1. """)

          self.add('INITIATE',
                   """
As you either progress through the indexes of the notebook,
or enter in indexes directly as commands, ARCADES displays
them, either alone, or together with the cluster of notes
that belong to the tribe of the top level note.

The behavior of the sequential display mode is determined
with the following commands:
     "childrentoo", "fulltop", and "automulti.

In its default “childrentoo” mode, ARCADES displays
the current note together with the entire tribe of notes
belonging to the top-level note with which it is associated.
The binary "childrentoo" command can be used to have
ARCADES no longer show the tribe together with the note.

When the “childrentoo” mode is deactivated, then,
if the “fulltop” mode is activated, ARCADES
will only display the entire tribe for top-level notes.
Other notes with be displayed alone.

When the “automulti” mode is activated together with the
“childrentoo” or “fulltop”-modes, then
Norescription will display the tribe as a tiled sheet. 


     """)

          self.add("INITIATE",
                   """
The all command can be used to display all the notes in the notebook.
If your notebook contains many notes, it may take a bit of time
to run the first time it is used, but it saves the results to a buffer
which may be retrieved subsequently.

The command all, in addition to being restricted to
a certain index range, accepts a single value and several modifiers.
The optional value indicates the size of the indexes to be listed;
all indexes must be less than this value.

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
Fields are used to divide the notebook into different sections.
A field is assigned to a set of indexes. It is possible to
assign a field either to 1) a range of consecutive top-level
(size=0) indexes regardless whether they are present in
the notebook or 2) a range of indexes, greater than p and
less than q and of arbitrary size, that are actually present in the
notebook, or 3) to any set of indexes, whether or not they
are present in the notebook. A given note at a given index can belong to one field at most.
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
The “multi” mode fits notes together into
a “sheet,” according to their width.

The notes are placed in a stack, with the largest possible note
that can fit in the free area withdrawn from the stack. The
output of the multi display is stored under a user-defined name,
and can also be saved as a text file.

The syntax consists in four values, and three modifiers:
     multi:INDEX COLLECTION;DISPLAY STREAM;WIDTH;SAVE STREAM /* /? /=

     
The first value indicates the indexes to be displayed;
the second the name of the “stream” to which display
will be outputted, and the third the width, in characters,
of the display.

The /$ modifier shows notes in a uniformly small size,
as defined using the command smallsize.

The /* modifier is used to activate the “vary”-mode,
adjusting the size of the notes according to the
length of the text string.

The /? pauses the display after each line.

The /= saves the output to a textfile, using either
the name of the display stream or name entered as
value 4.""")


          self.add('INIITIATE',
                   """
Commands for manipulating the notebook may
be divided into three categories:

1) Those which only affect the relation
of the note to the index.
     | These “index” commands include:
     "delete", "move", "copy", "clear", "purge", "rehome",
     "eliminateblanks".

2) Those which change the “content” and “properties”
of notes without changing indexes.
     | These “content” commands include:
     "correctkeys", "reform",
     
3) Those which change both the “content” of notes
– the keywords and text –as well as the relation
of this content to indexes.
     | These “note” commands include:
     "revise", "mergemany", "conflate", "split", "sidenote"
     """)

          self.add('INITIATE',
                   """
Entering "delete", or alternatively "del",
with a collection of notes as a value,
deletes these notes by moving them
to a negative index positions.

The "clear" command is used to delete
all the notes from the notebook by moving
them to negative index locations.

Because it is rather dangerous to use,
it queries you each at step to see if you want to continue.

There is little reason for using clear
except when working with very small notebooks

The command "undel" is used to “undelete”
the notes with negative indexes, moving them back into
positive registers.

The "compress" command compresses the
notebook by moving all the notes
to contiguous index positions.

The "rehome" command is similar to compress,
but moves notes in such a way as to eliminate orphan
notes. The rehome command accepts as a value
a collection of notes.""")

          self.add('INITIATE',
                   """
The "move" command allows you not only to move
individual notes from one index location to
another, but also to move collections of indexes
and even transform the hierarchical structure of the
notebook itself.

The syntax of the move command is as follows:

     move:INDEXESFROM;INDEXTO;[S/M/C];[yes/no] /$ /& /* /? /=

The first value indicates the collection of indexes
that will be moved; the second the destination to
which they will be moved; the third –
either S, M or C indicated how the how the notes will be
organized at the destination; and the fourth value
whether the children of indexes will be included.

The first of the three modifiers are to indicate the third value,
while the fourth and fifth are used for
the fourth value.
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

It is important to note that the behavior of
S/M/C depends on whether the destination range is
already occupied. If there is an index in the destination,
then the new notes will be placed in a
subordinating relation – either (S), which creates a
“microcosmic representation” of the source range
subordinated to destination index, or (M), which
flattens them into siblings, children of the same
index; or (C), which turns them into a chain of children.
Observe, also, that ARCADES does not forbid
you from moving the source range into itself, nor
can this “crash” the system.

This is because notes are moved individually,
the interpretation of each “move” depends
on the present state of the system after an individual move,
and ARCADES will either refuse to execute a move
(if the source index is empty) or will interpret
it such that it can be done (if the destination is occupied).

For this reason, though, it may be a bit tricky to foresee how a
command will be executed when it moves indexes onto themselves.""")

          self.add('INITIATE',
                   """
The "copy" command is identical to the move command,
save that it does not delete the note from
the source index.

The command "permdel" is used to permanently
delete all the notes with negative indexes.

To see the notes with negative indexes –
the temporarily deleted notes –
use the command "showdel.""")

          self.add("INITIATE",
                   """
The command "revise"
(alternate form: "rev")
is used to add to an existing note.
It can either add the text of ne existing note to
another note, or call up the text inputter.

The user can also define the
text placed between the note, and whether
the new text is placed before or after.

The revise command accepts three values
and the modifiers /$ /& /* /?. The first value is used to
select the index or collection of indexes to be revised,
the second value is the index of the note to be added,
and the third value is the text to be inserted between notes.

The /$ modifier is used to add the new text to the beginning rather than the end.
The /& modifier adds the new text both the beginning and the end.
The /* modifier selects /BREAK/ as the “breaker”
The /? modifier selects /NEW/ as the “breaker” """)

          self.add("INITIATE",
                   """
The command "mergemany" is used to take
a collection of indexes, and join them together
into a single note. It does not delete the indexes
that is conflates, and hence it can be understood as
a mode of copying.

It accepts three values and the modifiers /$ and /&.

The first value is the collection of indexes
to be joined together. The second value
is the index of the destination where the
new note is to be placed.

The third value is the manner in which the notes are
to be joined together, and can be either
(c)onflate or (e)mbed.

The modifier /$ is the equivalent to
the value (c)onflate while
the modifier /& is the equivalent
to the value (e)mbed. If you use both
modifiers, it will repeat the action
twice in each of the two manners.

The “embed” joins together displayed notes,
together with brackets, whereas “conflate” merely
combines the text of the notes and their keywords.
""")

          self.add("INITIATE",
                   """
The command "conflate" is similar to
revise and mergmany. It joins a collection of notes together
separated either by /BREAK/, /NEW/ or a user-defined term.

It accepts four values and the modifiers /$, /&, /*, and /?.

The values consist in
     (1) the collection of the indexes
     of the notes to be joined together

     (2) the destination of the newly created note

     3) (e)mpty, (b)reak, or (n)ew, and

     4) a user defined “breaker”. The first three modifiers
     are equivalent, respectively, to
     (e)mpty, (b)reak, and (n)ew, while /? Is used
     to solicit a user-defined “breaker.”
""")
          
          
          

          self.add('SEARCH',
                   """
Qualifiers are attached to individual terms
in order to add further restrictions on the query.

The Qualifier Phrase enclosed within double
quotation marks, and affixed directly after
the individual search term, with no blank space.
The term consists in one or more qualifiers separated by
exclamation marks. 
                   
Qualifiers may take either no value, a single
integer value, a single string value,
or a single range of value. The following are examples of
valid search expressions with qualifiers:


1) ?:frog“count=1”
        | Search for notes in which
        | the word “frog” appears once.
2) ?:<toad>“depth=1/3”
        | Search for notes whose
        | index has a depth not less than
        | and not greater than 3
3) ?:*ism”date=2020-1/2020-4!depth=4/5”
""")

          self.add('SEARCH',
                   """
Any command which yields a list of indexes
or range of indexes, or a list of searchable
terms, can be refed into another command as follows:

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
The searchlog command is used to show
all previous search results.

The search log allows you to combine the
results of previous searches.""")

          self.add('SEARCH',
                   """
Variables can be used to store
the results of searches, lists of keys,
and even text, and then feed these
back into commands as values.

To define a variable, simple refeed the
results of a command into a variable name.
Variable names must be written in capital
letters and not have any non-alphabetic characters.

For example:
(1) keys:1-10 =>SOMEKEYS
          | Feeds the keywords
          | for notes 1-10 into SOMEKEYS
(2) show:1 => SOMETEXT
          | Feed the text for note 1 into SOMETEXT
(3) ?:<Husserl> =>SOMEINDEXES
          |Feed search result into SOMEINDEXES

          
To retrieve the contents of a variable,
simply include it in double curly brackets.

For example:

(1) ?:{{SOMEKEYS}}
          | Searches for SOMEKEYS
(2) +:Husserl;{{SOMETEXT}}
          | Enters a new note with SOMETEXT as the note text.
(3) show:{{SOMEINDEXES}}
          |Show the notes in SOMEINDEXES""")

          self.add('SEARCH',
              """
The “slice”-qualifier can be used to restrict
the search results to notes whose indexes are contained
“within” the upper and lower slice.

A slice consists in of values, separated by PERIODS.
Every value may either by be empty, or consist
in either an integer, for the value at the head
of the slice, or a natural number.

Or in other words: a slice is an index, with some, but not all, of the elements
removed.

Valid slices include: “1.2.3.4.5.6”, “…5…”,”-10.1.1.1.1.”

A given Index is “within” a lower and upper bound
iff each element of the index is not less than
equally-ranked element of the lower bound and
not greater than the equally-ranked element of the upper bound.
If a bound is not given, whether because either
the upper or lower bound has not been defined or
because ranked-element is missing, then the condition
is automatically satisfied.

If the “must”-mode is selected, then the index must
have elements of rank equal to all the rank of all the
elements of the lower and upper bound. Or in other words,
if an index is not as “deep” as the greatest depth
of the upper or lower bound, then the index will not be “within” the slice.

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
The following qualifier can be used to
exclude notes where a single search term appear in the text
less than or more than a certain number of instances.

     count=LESSTHAN/GREATERTHAN

The qualifier “strict” can be used to count by whole words.
The result is more correct, but it is also a bit slower,
since it must iterate over the Cartesian product of the punctuation marks. """)

          self.add('INITIATE',
              """
Histograms display a frequency chart for keywords
or words in the text. To produce a histogram,
simply use the "histogram" command, with a collection
of indexes as the value.

The modifier /$ is used to choose
between text words and keywords.""")

          self.add('INITIATE',
              """
Notesccription allows you to represent the
keys in a collection of notes by date and time of
composition or modification.

The chronogram feature is very flexible, and sorts according to year,
month, day, or even hour, in various combinations.
It also allows you to choose between using the
first date, the newest date, or all the dates
associated with the notes in the index range, and also
reveal or suppress the indexes associates with the keys.""")

          self.add('INITIATE',
              """
To initiate a chronogram, use the "constdates"
(alternative form: "constitutedates") command,
which accepts three values and
the modifiers /$, /&, /* and /?.

The first value consists in a collection of
indexes, the second value the determinant,
and the third value in either f(irst), n(ewest), or a(ll). 


The modifiers /$ and /& can be used to
define the determinant, respectively, as ym (year+month)
or ymd (year+month+day), in lieu of the second value.

The modifier /* is used to show indexes,
while /? Explicitly ask which dates are to be used,
and thus can be substituted for a third value.

Consider the following commands:
     (1) constdates:1-100;ymd*h;f /*
     Create a date dictionary for indexes 1 to 100,
     with ymd*h as the determinant, using the date
     when the note was first entered, and displaying indexes.

     (2) constdates:1-1000;ym /?
     Create a date dictionary for indexes 1 to 1000,
     using ym as a determinant, and
     querying whether to use the first, newest, or all dates.

The determinant indicates what divisions of time
(year=y, month=m, day=d, hour=h, minute=m,
second=s, microsecond=x) will be used to
organize the date dictionary.

The maximum determinant is ymd*hmsx.
Any subset of the maximum determinant, with the star
included, is a valid determinant. 


Chrongrams are stored in a dictionary using the
determinant as key. You can use the command
showdatedict to display an existing chronogram.
This accepts the determinant to be displayed as a
value, and the modifiers /$, /&, /*, /?, /=,
which are used to add, respectively, year, month, day,
hour, and minute. The minute can only be added after an hour.
     """)
     

          self.add('INITIATE',
              """

A “project” in ARCADES stores some basic information
about the program-state and keeps track of the
indexes of notes that have been added to the project.

Finally, when a project has been
activated and is in use, each new note will include,
as sequence keyword, the name of the project
together with a value indicating the order
in which the note has been entered, with the initial value
determined by the user.""")

          self.add('INITIATE',
              """
Projects are stored in a special dictionary,
which is a permanent attribute of the notebook.
The name of the project serves as the identifying key.

For each project, the following attributes are kept track
of and stored:

     1) The default keys, which are
     automatically included when the project is active.
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
Commands for using projects include:
"newproject", "saveproject", "showprojects", "resumeproject",
"loadproject", "endproject", "flipproject", "crrrentproject",
"archiveproject", "unarchiveproject",
"showarchivedrpojects", "deletearchivedrpoject",
"loadproject", "dumpproject", "renameproject". """)

          self.add("INITIATE",
              """
The command "newproject" is used to initiate
a new project The name of the new project is entered as
a value.

If, however, a project with this name already exists,
and the project name is alphabetic, not
already ending with a number, then a 1 will be suffixed
to the project name. If the project name
already has a numerical suffix, then the
existing numerical suffix will be increased by 1.

So for example: HEIDEGGER > HEIDEGGER1 > HEIDEGGER2 > HEIDEGGER3""")

          self.add("INITIATE",
              """
To display all the projects that are currently
attached to the notebook, type "showprojects"

To resume a project that already exists, type "resumeproject",
with a single project or list of projects as
a value. If a project is already active, this
will be saved before a new project is activated.

You will be asked if you wish to update the defaultkeys
in the project.

This command also accepts to modifiers:
     /$ and /&.

Use the first of these to add a second project
to an existing project, and the second if you do not wish
to automatically update the position and the entrymode.
     
""")

          self.add("INITIATE",
              """
To quit the current project, enter "endproject"
(alternative form: "quitproject").

The command 'flipproject" takes the
indexes of the current project and
sends them to the flipbook,
allowing you to iterate over them.

""")

          self.add("INITIATE",
              """
ARCADES allows you to open several notebooks at once,
switching back and forth between them.
To switch, you use the "switch" command.

The first time that you use it, it will exit the current
notebook, and allow you to enter a new one.

To do so, select (N) in the input menu. Once more than
one notebook is active, future uses of switch
will display the active notebooks, and allow you to
switch to a new one, or remain in the old one,
just by typing the number corresponding to it.
When you quit a notebook, the notebook will be
closed and you will be returned to the “switch”-
menu. Here it is possible to quit all the
active notebooks, closing ARCADES.""")
     
          self.add('INITIATE',
              """
Each active notebook is a unique notebook-object.
ARCADES, however, also allows you to store
notes in a common register shared by all the notebooks.

Enter "copyto", with a collection of indexes as a value,
to copy notes into the temporary buffer.

Enter "copyfrom", with a single value indicating
the number of notes, or using the modifier /$ to
indicate all the notes in the temporary buffer.

The temporary buffer functions as a stack
-- first in/first out – and notes are
deleted as soon as they are “copied” out of it.""")
     
     
          self.add('ENTERING',
              """
The poetry mode automatically inserts an EOL
character at the end of each line, thus preserving the
integrity of the verse. Whereas in the prose mode,
the size of the note is arbitrary, and determined
in advanced, the poetry mode sizes the note based
on the longest line of text. It is possible to
combine poetry and prose in the same note, but,
so long as prose is selected once, then the size of
the note will be determined “poetically” rather
than “prosaically." """)

          self.add('ENTERING',
              """
ARCADES includes a basic spell-checker,
If there are misspelled words, the spelling corrector
will be activated automatically. To deactivate
or activate the spelling feature, use the
binary command "spelling" """)

          self.add('ENTERING',
              """
t it is possible to edit, subsequent to entry,
either the keys of a note, the text of the note, or both.
The commands for initiating editing are:
     "editnote", "editnotekeys", "editnotetext."
These are followed by an index or a collection of indexes.
The command editnote accepts a single modifier /$, which is
used to activate the “annotate” mode.
Whereas editnote edits both the keywords and the text of a
note, editnotekeys or editnotetext can be used
to edit only the keys or only the text.""")
              
              

if __name__ == "__main__":
     tutor = TutorialManager()

     tutor.start()

     tutor.load()

     while True:
          x= input('?')
          if x:
               tutor.show(x)
          else:
               break
     tutor.stop()
          
