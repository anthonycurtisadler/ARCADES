"""Module constituting the commandscript
pylint rated 10.0/10
"""

MENU_DICTIONARY = {}
HELP_DICTIONARY = {}

COMMANDSCRIPT = []

HEADERS = ['COMMANDS',
           'DEFAULTKEYS',
           'NAVIGATION',
           'DISPLAY',
           'SEARCHING',
           'ORGANIZING NOTES',
           'DEFAULTS',
           'INPUT/OUTPUT',
           'ADVANCED',
           'HYPERLINKS',
           'DEFAULT',
           'ADVANCED DISPLAY ONE',
           'ADVANCED DISPLAY TWO',
           'KNOWLEDGE BASE & SYSTEM']

PERIOD = '.'
BLANK = ' '
EMPTYCHAR = ''



def make_command_dict (text):

    """ Creates the HELP DICTIOARY from the text of COMMMANDS
    Splits text into lines.
    Skips over line if equal to '||'
    Splits line into phrases divided by '|'
    First phrase = COMMAND
    Second phrase = PARAMETER
    Third phrase = DESCRIPTION/INSTRUCTION    

    """

    started = True 
    command_text = ''
    parameter_text = ''
    instruction_text = ''
    for line in text.split('\n'):

        if line != '||':

            phrases = line.split('|')+['','','']
            command,parameters,instruction = phrases[0].strip(),phrases[1].strip(),phrases[2].strip()

            if command:
                
                if not started:
                    for com_temp in command_text.split(','):
                        HELP_DICTIONARY[com_temp.strip()] = (parameter_text.replace('\n\n','\n'),
                                                             instruction_text.replace('\n\n','\n'))
                command_text = command
                
                parameter_text = parameters + ' '
                instruction_text = instruction + ' '
                started = False
                

            else:
                parameter_text += parameters + ' '
                instruction_text += instruction + ' '
            
            
                
    for com_temp in command_text.split(','):
        if com_temp.strip() not in HELP_DICTIONARY:
            HELP_DICTIONARY[com_temp.strip()] = (parameter_text,instruction_text)
                  

 

COMMANDS = """
||
COMMAND|PARAMETERS|FUNCTION
||
|BASIC NOTE ENTRY|
||
// divides multiple commands | |
{{int}}| |for feeding back search results
[?] | |for feeding back marked indexes
[/] | |for last entered or displayed note
||
| #yr-mo-dy |To enter dates in ranges, use POUND 
ent, enter, +    |key(s);text..  {$ to suppress show}..		|enter a new note
                 |/= suppress default keys
                 | |Indexes, entered as keys, serve as hyperlinks
                 |SEQUENCE@INTEGER |For entering a sequence key
                 |SEQUENCE@#1770-03-20
                 |SEQUENCE@_INDEX  

ent, enter, +    |index                                         |enter a note at index
enternext, ++| |Enter a 'next' note 1.1>1.2
enterchild, +++| |Enter a 'child' note 1>1.1
enterback, -| |Enter a note at.. previous level 1.1.1>1.2
conent | |Enter a series of notes
conchild | |Enter a series of children
connext | |Enter a series of nextnotes
;; |To quit connext and conchild modes 
delete,del,d|index or indexrange			    	|delete note(s)
/|To quit entering mode and continue |
|cycling through notes |
|MODIFYING NOTES|
editnote|indexrange.. /$ annotate		    	|edit note(s) keys and text
editnotekeys|indexrange                                 |edit note(s) keys
editnotetext|indexrange                                 |edit note(s) text 
revise,rev|indexrange;index to merge;break mark|revise a note..
| /$ in back /&.. front and back /*BREAK /?Newu

undo|undo						|undo last action
redo|redo						|redo last action
"""

DEFAULTKEYS = """
|MARKING NOTES|
marked | |show all marked keys
[ | |mark current key
] | |unmark current key
addmarks |indexranges |mark notes in range
deletemarks |indexranges|unmark notes in range
clearmarks | |unmark all notes 
|DEFAULT KEYS|
addkeys,ak|key,key...;keymacroname /$ to save macro |add new default keys
addkey|key |add one key to default keys
newkeys|keymacro.. /$ keep old|change to new keys from keymacro
changekeys|keys;keymacroname /$ to save macro |changes to new default keys
deletekey,dk| |delete last default key
deletedefaultkeys| |delete default keys
clearkeys| |clear all default keys 
grabkeys|indexrange.. /$ no all caps.. /& no first caps     |
"""

NAVIGATION = """
skip|index                                          |skip to index
hop|int                                            |jump ahead
first| |go to the first index
last| |go to the last index
[.*int]| |hops ahead by int
[,*int]| |hops back by int
>| |direction forward
<| |direction back
'| |move to the next/previousnotes
"| |move to the child/parent notes
=| |return to ordinary mode

||
||"""

DISPLAY = """
||
123[return]        |displays the next note				|displays note with INDEX 123
* ||Shows notes related to the current note
all, $		|levels to show.. /$ suppress quick mode  |show all notes
 |/&no children /* no brackets |
 | /? suppress short show |
 | /= showdates %indexrange | 
show, s		|indexrange;levels to show |
 | /&no children |show some notes
 | /* no brackets |
 | /? suppress short show |
 | /= show dates |
inc | |incremental show
indexes, ind, i	| |show indexes
keys, key, k	|/$ histiogram.. |show keys
                |/& all caps..  | =>COMMAND:?? 
                |/* upperkeys..  | to feed back results
                |/? lowerkeys  |
                
tags, tag, t	| |show tags
text            |index range;# of words1;# of words2;gets important words in the text
                |/$ for intersection of words
                |/& by decreasing frequency in notebase
                |/$ by increasing frequency in note itself
keysfortags     | |show keys for tags
defaultkeys, dfk | |show default keys
showdel		| |show soft-deleted notes
keystags	| |show tags and their keys


||"""
SEARCHING = """| |
search, ?	|search phrase  %indexrange..			|keysearch..
                |use a straight slash for OR.. |.. =>COMMAND:?.. 
                |use an amperstand for AND.. |to feed results into
                |parentheses are allowed.. |another command
                |ALL CAPS for case insensitive.. |
                |<keyword>.. |
                |#tag.. |
                |##metatag..  /$ show.. /&dates.. |
                |/? show indexes  |
                |* wildcard |
                |<SEQUENCE@FROM> | to search for sequences
                |<SEQUENCE@TO> | ADD # and _ as appropriate
                |<SEQUENCE@FROM/SEQUENCE@TO>
                |{NOTEBOOK1,NOTEBOOK2} |To search over another notebook
globalsearch    |searchphrase;notebooks |To search over other notebooks
                |/$ don't query
terms,???       |return foundterms 
textsearch, ??	|search phrase %indexrange			|textsearch
constdates,     |indexrange;f(irst) n(ewest) a(all)..             |make date chart
                |/$ ym.. /& ymd.. /* show indexes..                   |
                |/? to query which dates                        |
constitutedates |                                               |
activedet,      |                                               |show active determinants      
actdet          |                                               |
showdatedict    |/$year.. /&month.. /*day.. /&hour..                    |display date chart   
ahowdatedictpurge |/$ ym .& ymd /* add hour  |
                  |/? ask for purge parameter |
                  |determinant;purge parameter |
                  |SPEC.TERM1-TERM2-TERM3... |
                  |SPECS = a ALLCAPS |
                  |         u UPPER |
                  |        l LOWER  |
                           
cleardatedict   |/$year.. /&month.. /*day.. /&hour..                    |clear date chart 
changedet       |determinant                                    |change determinant
showdet         |                                               |show determinants 
setpurgekeys    |/$ allcaps.. /& upper.. /& lower..                   |set keys to pyrfe when showing date  
                |spec[=aul].terms                               |
clearpurgekeys  |                                               |clear purge keys 
showpurgekeys   |                                               |show purge keys 
searchlog       |                                               |show the search log
clearlog,       |                                               |clear the search log 
clearsearchlog  |                                               |

||"""

ORGANIZING = """||
mergemany, mm	|indexrange;indexrange;C-E..                      |Combine many formatted notes within a single note
                | /$ Conflate..
                | /& Embed
conflate	|indexrange;e - b - m;destinationindex;BREAKMARK  |conflate many notes into a single note
                | e(mptychar)                           |
                | b(reak)                               |
                | n(ew note)
                | /$ emptychar /& break /* new  /? BREAKMARK |
move             |indexrange;indexrange;S or M or C;Yes/no..  |move to notes from.. sourcerange to destinationrange
|S=Subordinate /$..|Preserves hierarchical.. structure when subordinating
|M=Make Compact /&..|Collapses hierarchical.. structure
|Children /*|Each note is a child of the last
copy            |See Above |copy from source.. to destination
copyto          |indexrange|copy notes into buffer
copyfrom        |integer.. /$ to copy all |copy notes from.. buffer into notebook
ndel|undel 						|undelete soft-deleted notes
permdel		|     {$ to suppress query}			|perminately delete soft-deleted notes
clear		|     {$ to suppress query}			|soft-delete all notes
addfield	|fieldname;indexrange				|define a new field
                |/$ for a prerange                              |
deletefield	|fieldname;range				|delete a field
compress		|					|remove gaps between notes
|ADVANCED FORMATTING |
split           |index;columns;width;breaking mark              |splits a note into columns
sidenote        |indexrange;total width.. /$ add counters         |side-by-side notes 
||
||"""


SETTING = """||
|FLIPBOOK|
flipout, f	|						|automatically channel search results into flipbook
showflip,       |                                               |show flip book
showflipbook    |                                               |
flipbook|indexrange or fields or index |define the flipbook ---
|DISPLAY|
shortshow	|						|display notes in short format
resize, size, sz	|integer					|set the default size for notes
showtags	|						|show tags attached to keys when displaying notes
setlongmax	|integer					|set the maximum number of notes
| |that can be displayed long-form
curtail         |                                               |eliminate EOL at beginning and end of note
header          |integer                                        |blank lines at top of note
footer          |integer                                        |blank lines at foot of note
leftmargin      |                                               |
orderkeys       |                                               |arrange keys by increasing frequency
rectify         |                                               |equalize the width of columns
cpara		|keys to purge;(a)allcap (c)aps (l)ower 	|cluster settings (exclude ALL CAPS;capitalized word;lower case)
                |/$ all caps /& caps /* lower case              |
|LIMITLIST|
limitlist	|indexrange or F or R				|define an automatic limiting range;
|F for flipbook; R to reset|
showlimitlist| |show limitlist
resetlimitlist, resetl| |reset limit list
|NOTE ENTRY|
quickenter	|						|enable quick-entry mode
autobackup	|						|suspend automatic backup of notes

changeuser	|username					|changes username saved in metadata
boxconfigs      |                                               |show configurations in boxed notes
spelling        |                                               |turn on or off spelling correction
enterhelp       |                                               |turn on or off note entry helpscript
formathelp  |                                               |turn on or off formatting helpscript
keysbefore||ask for keys before entering note
keyafter||ask for keys after entering note
carryoverkeys||carry over keys for child and nextnotes
carryall||carry over keys from all parents
returnquit| |Exit note entry mode after pressing successive returns
setreturnquit| |Set number of returns for returnquit
||"""

INPUT = """||
loadtext, lt	|filename.. \= suppress default keys		|load and parse a NOTESCRIPTle embedded note
formout		|indexrange;filename;include indexes;include metadata |save NOTESCRIPT
                |/$ include indexes /& onclude metadata 
loadbyparagraph |/$ don't apply keywords.. /& apply definitions   |load text, divide by paragraph, and apply keywords
|/* suppress queries|
splitload       |string                                         |Load text, divide by splitterm, and apply keywords
|$ don't apply keywords.. /& apply definitions..|
|/* suppress queries|

||"""

ADVANCED = """||
cluster         |int..  /$ turn clusters into iterators         |organize notes into clusters. Parameter indicates how many
killclusters    |                                               |destroy cluster iterators
descendents     |iterate over clusters of note descendents
| |keywords, according to increasing.. frequency, will be used
;(semicolon)|switch to next cluster-iterator|
| |the notes that are cycled through
eliminateblanks|						|eliminate blank keys
eliminatekeys|keys						|globally removes keys
correctkeys|indexrange..  /$ keys+tags |corrects keys
refresh|						|reconstitute word.. concordance used for searching
reconstitutesequences| |reconstitute sequences
reform|range|applying reformating to range of notes!

saveconfigurations| |save configurations
loadconfigurations| |load configurations
dumpprojects | |save a backup textfile of projects
loadprojects | |load a backup textfile of projects
clearprojects | |clear existing projects 
||
"""
HYPERLINKS = """
|HYPERLINKS|
link |indexrange |links together notes
chain |indexrange |enchains notes
loop |indexrange |loops notes
unlink |indexrange |removes hyperlinks
iteratemode | |toggles between iteratemode and hypermovemode
hyperone | |hypermovemode one --
||randomly jumps between notes with common keys
hypertwo | |hypermovemode two --
||randomly jumps between hyperlinked notes
hyperthree| |hypermovemode three --
||allows you to navigate between hyperlinked notes
startlinking| |Start automatically linking notes
startlooping| |Start automatically looping notes
endlooping,endlinking| |End looping or linking notes
showsequences| |show sequences
showsequence|sequencename |show a single sequence
 |/$ correct sequence 
invert | |Gives opposite of indexes 

"""

DEFAULTS = """||
changecodes| |change abbreviations. Use to define special codes (TO) 
changemacros| |change macros. Implemented with _ before macro
changekeymacros| |change key macros. Implemented wiht $ before macro
changecommandmacros| |change commandmacros
changekeydefinitions| |change definitions
| |Used to automatically assign keys with loadbyparagraph
changeknowledge| |change knowledgebase
changegeneralknowledge| |change general knowledge
||
defaultcodes| |load codes embedded with kw CODES
defaultmacros| |load macros embedded with kw MACROS
defaultkeymacros| |load keymacros embedded with kw KEYMACROS
defaultcommandmacros| |load commandmacros embedded with kw COMMANDMACROS
defaultkeydefinitions| |load keydefinitions embedded with kw KEYDEFINITIONS
defaultknowledge| |load knowledge embedded with kw KNOWLEDGE
||
recordcodes| |record codes into a note
recordmacros | |record macros into a note
recordkeymacros| |record keymacros into a note.
recordcommandmacros| |record commandmacros into a note
recordkeydefinitions| |record keydefinitions into a note.
recordknowledge     | |
||
clearcodes | |reset abbreviation object
clearmacros| |reset macros
clearkeymacros| |reset keymacros
cleardefinitions | |reset definition object
clearcommandmacros | |reset commandmacro object
clearkeydefinitions | |reset keydefinition object
clearknowledge | |reset knowledgebase
||
showspelling |language.. /$  en.. /& gr.. /* fr.. /? es |show words added to spelling dictionary
spelldictionary| |call up spelling dictionary console
defaultspelling|language.. /$  en.. /& gr.. /* fr.. /? es |load added words from note 

| |NOT RECOMMENDED for large ranges"""


ADVANCEDDISPLAYONE = """||
multi|streamname;width;savename.. |display notes packed into columns, channeled to a stream,
     |/$ smallsize /* vary.. /? pause.. /= save |
| |with option to vary
| |width according to legnth of text
smallsize | |set small size for multidisplay
streams| |shows active display streams
showstream|stream /? pause |display an active display stream
deletestream|streamname {$ to suppress query}		|delete a display stream
updatetags||updates the tags
histiogram|/$ for keys                                  |generate a histiogram of words
showuser	| |show the user
negativeresults,| |include negative results with searches
negresults,nr | |
fields		| |show defined fields
showmeta	|index|show metadata
depth           |integer |set the number of children to display
deeper          | |go one level deeper
shallower       | |go one level shallower
allchildren     | |show all children
childrentoo     | |include children when showing notes
shortshow, ss || show notes in an abridged form
fulltop         | |show all descendents of top-level notes        
randomon        | |turn on random mode
randomoff       | |turn off random mode
indentmultiplier ||Adjust the indentation for displaying
||chilren 
||
usesequence | |uses sequences for keeping track of indexes
itshow | |show all indexes rather than greatest and
| |smallest when resetting the iterator
|FLASHCARDS|
noflash | |don't show flashcards as flashcards
flashmode | |flip through flashcards
setsides | | set the number of sides for flashcards
setflipat | | set the side at which the side flips
flexflip| | automatically adjust to
 | |number of sides of flashcards
flashforward, ff | |advanced to the next side 
flashback, fb | | go back to the previous side 
flashreset, fr | | reset to the first side 
flastto, ft | | advance to given side
"""
ADVANCEDDISPLAYTWO = """
sortbydate | |display notes sorted by date 
showimages | | enable display of embedded images
showtext | | enable display of embedded text
seqintext | | include sequences in the main text
fromtext | | extract keywords and sequences from text
convertbyline | | extract keywords and sequences by line
nodiagnostics | | disable diagnostic tracking
updateuser | | update user over a range of notes 
updatesize | | update size over a range of notes 
run | |
interpret | |
diagnosticnote | |
dictionaryload ||
seqformone | |define seqformone for seqintext
seqformtwo | |definte seqformtwo for seqintext
mainsequences | |define mainsequence for seqintext
convertdefinition | |define parsing information for fromtext
newconvertmode | |add a new convert mode
switchconvertmode | |switch to a new convert mode
showallconvertmodes | |show all convert modes
createworkpad |padname |create a new work pad
addtopad |range,padname |add notes to pad
||add notes to pad, and display 
padshow |range,padname |create pad if needed
emptypadstack |padname| clears notes from pad
renewpad |clears an existing pad 
sheet|range,display stream,width,save stream, Xmax*Ymax |display as sheet
| /$ query size  /* vary
rsheet, resumesheet | resumes existing sheet
closesheetshelf |close the sheet shelf
tosheetshelf|frompad,topad|add a pad to the shelf for storage
selectsheet |resume a pad in the sheetshelf 

||
||"""

KNOWLEDGE = """
|SPECIES-GENUS KNOWLEDGE|
learn|string(species);string(genus)|teach the notebook an ontological fact
forgetstring(species);string(genus)| |unteach the notebook an ontological fact
allknowledge| |show what the notebook knows
|GENERAL KNOWLEDGE|
dumpknowledge,dumpgeneralknowledge |
showknowledge |
loadknowledge,loadgeneralknowledge|filename |load knowledge from textfile
cleargeneralknowledge|
reconstitutegeneralknowledge |
general,generalknowledge,gk|query|interprety a knowledge query
(*)KNOWLEDGE PHRASE(*) |ALTERNATE FORM OF ABOVE
switchgeneralknowledge| 
||
|PROJECT MANAGEMENT|
newproject|projectname |Start a new project
saveproject|projectname |Save a project
loadproject,resumeproject |Resume a saved project
showprojects||Show all available projects
currentproject||Show information about current project
flipproject| |Iterate over indexes of current project
|SYSTEM|
||
menu (single space)| |calls up small menu 
bigmenu (double space)| |Calls up big menu
help|						|
showsettings| |Show settings
switch|notebase |switches to a new notebase without quiting
quit|  {$ to suppress query}			|save and quit
test| execute test script 

"""
COMMANDSCRIPT.append(COMMANDS.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(DEFAULTKEYS.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(NAVIGATION.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(DISPLAY.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(SEARCHING.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(ORGANIZING.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(SETTING.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(INPUT.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(ADVANCED.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(HYPERLINKS.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(DEFAULTS.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(ADVANCEDDISPLAYONE.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(ADVANCEDDISPLAYTWO.replace(PERIOD+PERIOD,EMPTYCHAR))
COMMANDSCRIPT.append(KNOWLEDGE.replace(PERIOD+PERIOD,EMPTYCHAR))

COMMAND_TEXT = COMMANDS+DEFAULTKEYS+NAVIGATION+DISPLAY+SEARCHING\
               +ORGANIZING+SETTING+INPUT+ADVANCED+HYPERLINKS\
               +DEFAULTS+ADVANCEDDISPLAYONE+ADVANCEDDISPLAYTWO+KNOWLEDGE
make_command_dict(COMMAND_TEXT.replace('\t', ''))


MENU_DICTIONARY[0] = (HEADERS[0], COMMANDS.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[1] = (HEADERS[1], DEFAULTKEYS.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[2] = (HEADERS[2], NAVIGATION.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[3] = (HEADERS[3], DISPLAY.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[4] = (HEADERS[4], SEARCHING.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[5] = (HEADERS[5], ORGANIZING.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[6] = (HEADERS[6], SETTING.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[7] = (HEADERS[7], INPUT.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[8] = (HEADERS[8], ADVANCED.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[9] = (HEADERS[9], HYPERLINKS.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[10] = (HEADERS[10], DEFAULTS.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[11] = (HEADERS[11], ADVANCEDDISPLAYONE.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[12] = (HEADERS[12], ADVANCEDDISPLAYTWO.replace(PERIOD+PERIOD,EMPTYCHAR))
MENU_DICTIONARY[13] = (HEADERS[13], KNOWLEDGE.replace(PERIOD+PERIOD,EMPTYCHAR))



##del COMMAND_DICTIONARY['COMMAND']




##
##for key in HELP_DICTIONARY:
##    print(key+' ///' +str(HELP_DICTIONARY[key]))


