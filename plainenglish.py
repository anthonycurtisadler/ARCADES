### contains queries, labels, alerts for plain English language, as well as the commands.
### and various input terms.
### NOTE that the names of the commands cannot be changed since 

from globalconstants import DASH, PLUS, CARET,\
     VERTLINE, EOL, DOLLAR, POUND, SEMICOLON, QUESTIONMARK
import commandscript


def make_commands(text):

     text = text.lower()
     return (text[0], text, text.capitalize(), text[0].upper())


ADDTERMS = make_commands('add')

DELETETERMS = make_commands('delete')

SHOWTERMS = make_commands('show')

QUITTERMS = make_commands('quit')

CLEARTERMS = make_commands('clear')

QUITALLTERMS = ('a','all','A','All',
                'ALL','Quitall','QUITALL',
                'quitall')

LEARNTERMS = make_commands('learn')

UNLEARNTERMS = make_commands('unnlearn')

BREAKTERMS = make_commands('break')

NEWTERMS = make_commands('new')

YESTERMS = ['yes',
            'Yes',
            'yeah',
            'sure',
            'whatever',
            'ja',
            'jawohl']

NOTERMS = ['no',
           'No',
           'no way',
           'absolutely no',
           'god no',
           'heaven forbid']

class Queries:

     def __init__(self):
          self.SELECTING_NOTEBOOK ="""Name or index of notebook,
                                   (N)ew to open a new notebook,
                                   or quit(A)ll to close all notebooks"""

          self.SELECT_OPEN_NOTEBOOK ="""Name or index of notebook,
                                      (N)ew to open a new notebook,
                                        or(Q)uit to quit the current notebook,
                                        Quit(A)ll to quit all notebooks."""

         
          self.SELECT_NOTEBOOK_HEADING = '/C/ SELECT NOTEBOOK'
          self.CHARACTERS_TO_CONVERT = 'Character to convert? '
          self.RANGE_FROM = 'Range from? '
          self.RANGE_TO = 'Range to? '
          self.INDEX_TO_MERGE = 'Index to merge? '
          self.DESTINATION = 'Destination? '
          self.SOURCE_TO_FROM = 'Source from / to? '
          self.STRICT_RANGE_TO_FROM = 'Strict range from/to? '
          self.RANGE_TO_FROM = 'Range from / to? '
          self.EDIT_OPTIONS = 'ENTER new text, or RETURN to keep,'+\
                              'or '+DASH+' to DELETE, or '\
                              +PLUS+' to insert new line before,'\
                              + ' or '+DASH+DASH+ ' to delete all subsequent lines '\
                              +' or '+CARET+' to replace! And '\
                              +VERTLINE+'to add an EOL mark.'\
                              +EOL+DOLLAR+'To append before or'\
                              +POUND+' to append after! '
          self.ENTER_KEYWORDS = 'Enter the keywords that you wish to keep! '
          self.SELECT_FILE ='Enter the number of'\
                             +' file to open, or name of new file, or'\
                             +EOL+'(B)ack to return to initial directory! '
          self.OPEN_CONFIRM = 'Are you sure you want to open: '
          self.AUTOKEYS_KEEP = 'Numbers of autokeys to keep,'\
                               +'to delete (start list with $)'\
                               +'or ALL to delete all autokeys ?'                 
          self.DELETE_CONF_BEG = 'Are you sure you want to delete? '
          self.DELETE_CONF_END = ' from the entire notebase. This cannot be undone! '
          self.REVISE_DELETE_BEG = 'Revise '
          self.REVISE_DELETE_END = ' to ____ ? ... or delete? '
          self.RESUME_ABORTED_NOTE = 'Resume aborted note? '
          self.KEYS = 'Keys? '
          self.NEW_KEY_LIST = '<yes> to keep all, '\
                              +'<no> to discard all, '\
                              +'or enter a selected range? '
          self.ENTER_SEARCH_TERM ='Enter composite search term, '\
                                   +' e.g [1]%[2]!- Begin '\
                                   +'with $ to show notes! '
          self.ADDITIONAL_KEYS = 'Additional keys '\
                                 +'to apply to'\
                                 +' inputed paragraphs? '
          self.INCLUDE = 'Include? '
          self.KEYWORDS_TO_ADD = 'enter keywords to add? '
          self.CONTINUE = 'Continue? '
          self.DELETE_FROM_TO = 'Delete from/to? '
          self.CHILD_DEPTH = 'Depth of children to display? '
          self.DEMARC_MARK = 'Demarcating mark? '
          self.CHILD_KILL = 'Child to kill? '
          self.LEVELS_TO_SHOW = 'Levels to show? '
          self.SUB_OR_MAKE_CHILDREN = '[S]ubordinate, '\
                                      +' [M]ake compact or [C]hildren? '
          self.NO_CHILDREN = 'No children? '
          self.ADD_TO_AUTOKEYS = 'Add to autokeys? '
          self.COPY_HOW_MANY = 'Copy how many? '
          self.LEVELS_TO_SHOW = 'Levels to show? '
          self.SEARCH_PHRASE = 'Search phrase? '
          self.CONFLATE_EMBED = '[C]onflate or [E]mbed? '
          self.WIDTH = 'Width? '
          self.INDEX = 'Index? '
          self.INDEX_OR_RANGE = 'Index or Indexrange? '
          self.COLUMNS = 'Columns? '
          self.BREAKER = 'Breaker? '
          self.BREAK_MARK = 'Break mark? '
          self.SURE = 'Are you sure? '
          self.FIELDNAME = 'Fieldname? '
          self.READ_ONLY = 'Read only? '
          self.OPEN_DIFFERENT = 'Open a different notebook or QUIT? '
          self.BETA_MODE = 'Do you wish to use '\
                           +'NOTESCRIPTION in the betamode? '
          
          self.START_COMMAND = 'SPACE to SKIP, '\
                               +'TRIPPLESPACE for COMPACT MODE'
          self.LANGUAGE_SUFFIX = 'Language + suffix'
          self.LANGUAGE = 'Language? '
          self.DISPLAY_STREAM = 'Display stream? '
          self.DETERMINANT = 'Determinant ymd*hsx? '

          self.PURGE_WHAT = ' purge a(llcaps) u(pper) l(ower).TERMS ? '
          self.SUFFIX = 'Suffix? '
          self.LEARN_WHAT = 'Learn that what? '
          self.IS_WHAT = ' is a what? '
          self.WHICH_COMMAND = 'Which command? '
          self.MENU_ONE = '[, >,<, ] (Q)uit '
          self.KEYS_TO_ELIMINATE = 'Keys to eliminate? '
          self.INCLUDE_META = 'Include metadata? '
          self.SHOW_INDEXES = 'Show indexes? '
          self.JUMP_AHEAD_BY = 'Jump ahead how much? '
          self.OLD_USER = 'Old user? '
          self.NEW_USER = 'New user? '
          self.UNLEARN_BEG = 'Unlearn that what? '
          self.UNLEARN_END = ' is a what? '
          self.NEW_LIMIT_LIST = 'New limit list? '\
                                +' Enter range, F for flipbook,'\
                                +'or R to reset! '
          self.FROM = 'From? '
          self.TO = 'To? '
          self.SAVE_TO = 'SAve to? '
          self.LONG_MAX = 'Maximum number of notes displayed in longform? '
          self.KEY_COUNT = 'Keycount? '
          self.EMPTY_BREAK_NEW = '(e)mpty,(b)reak,(n)ewnote? '
          self.SPECS = 'Specs . terms to purge? '
          self.SET_KEY_TRIM = 'Set trim for displaying keywords? '
          self.SET_TEXT_TRIM = 'Set trim for displaying text? '
          self.NEW_NOTE_SIZE = 'New note size? '

          self.OPEN_AS_NEW = 'Open as new file? '
          self.FIRST_NEWEST_ALL =  'f(irst) (n)ewest (a)ll (i)ndex? '
          self.DETERMINANT2 = 'Determinant? '
          self.NAME_FOR = 'Name for '
          self.UNDO_UP_TO = 'Undo up to? '
          self.TOTO = ' to '
          self.ALSO_ABORT = ' or ABORT to abort'
          self.OTHERS_TO_PURGE = 'Other keywords to purge? '
          self.EXCLUDE_ALL_CAPS = 'Exclude all-cap keywords?  '
          self.EXCLUDE_CAPITALIZED = 'Exclude capitalized keywords? '
          self.WHAT_TO_PURGE = 'purge (c)apitalized, (a)ll caps, (l)ower case'
          self.RETURN_QUIT = ' Exit noteentry after how many returns?'
          self.CLUSTER = 'Cluster? '
          self.KEY_MACRO_NAME = 'Key macro name? '
          self.KEY = 'Key? '
          self.PROJECT_NAME = 'Project name? '
          self.INDENT_MULTIPLIER = 'Indent multiplier? '
          self.SMALL_SIZE = 'Small size? '
          self.CLEAR_DEFAULT_KEYS = 'Clear default keys? '
          self.SIDE = 'Go to side? '
          self.SIDES = 'Number of sides? '
          self.TEXT_TO_SAVE = 'TEXT to save? '
          self.SAVE_TO_FILE = 'File to save to? '
          self.FOLDER = 'In folder? '
          self.TEXT_TO_PRINT = 'TEXT to print '
          self.FLIP_AT = 'Flip at? '
          self.SHOW_ALL_NOTES = 'Do you want to show all the notes in the notebook? '
          self.DIVIDE_PICKLE = "Do you want to divide "\
                               +" the pickle file?" +\
                               " (Y)yes to divide (D)on't ask again? "
          self.LANGUAGE = 'Language? '
          self.LANGUAGE_SELECT = 'es(panol) fr(ench) en(glish) de(utsch)? '
          self.FUNCTION_NAME = 'Function name? ' 
          self.TEXT_TO_CONVERT = 'Text to convert? '
          self.TEXT_TO_INTERPRET = 'Text to interpret? '
          self.INCLUDE_PROJECTS = 'Include projects? '
          self.SEQ_FORM_ONE = 'Formatting after each sequence? (s) for space,' + EOL + \
                              '(l) for EOL, (c) for COMMA and SPACE, ' + EOL + \
                              '(b) for break, (n) for new or OTHER TEXT '
          self.SEQ_FORM_TWO = 'Formatting after all sequence? (e) for emptychar, '+ EOL + \
                              '(l) for EOL, (b)reak, (n)ew or OTHER TEXT '
          self.MAIN_SEQUENCES = 'Main sequences? Enter as a list separated by commas or (d)efaults! '
          
          
          
     
class Alerts:
    def __init__(self):
         
          self.ATTENTION = '/C/ ATTENTION'
          self.SELECTED = '/C/ SELECTED'
          self.CONSTITUTING_WORD_DICT = '/C/ CONSTITUTING WORD DICTIONARY!'
          self.WAIT = '/C/ PLEASE WAIT!'
          self.EDITING = '/C/EDITING NOTE'
          self.ON = 'ON'
          self.OFF = 'OFF'
          self.LEARNED_BEG = 'I learned that '
          self.LEARNED_MIDDLE = ' is a(n) '
          self.NOTE_ADDED = 'Note added at'
          self.CHANGE = 'Change'
          self.TO = 'to'
          self.REHOMED = 'SUCCESSFULLY REHOMED!'
          self.ITERATOR_RESET = 'ITERATOR RESET'
          self.KEYS_FOR_DATES = 'KEYS FOR DATES'
          self.APPEARS_BEG = ' APPEARS'
          self.APPEARS_END = ' TIMES. FREQUENCY='
          self.FAILED_CONF_LOAD = '/C/ FAILED TO LOAD CONFIGURATION FILE'
          self.CREATING_NEW_CONF = '/C/ CREATING NEW CONFIGURATION FILE'
          self.NEW_PICKLE = '/C/ NEW PICKLE FILE'
          self.ENTER_DOCUMENTATION = '/C/ ENTER documentation '\
                                     +'TO LOAD INSTRUCTIONS'
          self.IS_INCONSISTENT = '/C/ NOTEBOOK IS INCONSISTENT'
          self.STILL_INCONSISTENT = '/C/ STILL INCONSISTENT'
          self.IS_CONSISTENT = '/C/ NOTEBOOK IS CONSISTENT'
          self.TOO_MANY_INDEXES = '/C/ TOO MANY INDEXES!'
          self.IS_CLOSING = '/C/ IS CLOSING!'
          self.OPENING = '/C/ WILL BE OPENED AS '
          self.ALREADY_OPEN = ' IS ALREADY OPEN!'
          self.DELETE_FROM_TO = '/C/ DELETE FROM / TO'
          self.EXLUDE_ALL_CAPS = 'Exclude all-cap keywords?  '
          self.EXCLUDE_CAPITALIZED = 'Exclude capitalized keywords? '
          self.NOT_YET_CLUSTERED = '/C/ NOT YET CLUSTERED'
          self.FLIP_CHANGED = 'FLIPBOOK changed to '

          self.SAVING = '/C/ SAVING '
          self.WORD_DICT_CONSTITUTED =  '/C/ WORD DICTIONARY CONSTITUTED'
          self.NOT_REGULAR = '/C/ NOT REGULAR'
          self.ADDED = '/C/ ADDED'
          self.MOVING_FROM = '/C/ MOVING FROM '
          self.COPIED_TO_TEMP = ' COPIED TO TEMPORARY BUFFER!'
          self.NOTE = 'NOTE '
          self.MOVED_TO = ' MOVED TO '
          self.COPIED_TO = ' COPIED TO '
          self.MOVING_TO  = 'MOVING TO '
          self.COPYING_TO = 'COPYING to '
          self.OLD = '/C/ Old '
          self.KEYS = 'Keys? '
          self.FIELDS = '   Fields?'
          self.LOADING_FILE = '/c/ LOADING FILE'
          self.REVISE_DELETE_END = ' Enter new term, RETURN to keep, or (d)elete!' 
          self.ALREADY_IN_USE = '/C/ ALREADY IN USE'
          self.STILL_CHANGED = 'Still change? '
          self.INDEX = 'INDEX '
          self.NOT_FOUND_IN_NOTEBASE = ' NOT FOUND IN NOTEBOOK!'
          self.NO_DICTIONARY_OBJECT = '/C/ NO DICTIONARY OBJECT'
          self.NEW_SEQUENCE = 'NEW SEQUENCE DICTIONARY CREATED OF TYPE '
          self.OVERWRITTEN = 'OVERWRITTEN. NEW SEQUENCE DICTIONARY CREATED OF TYPE '  
          self.RECONSTITUTING_INDEXES = 'RECONSTITING INDEX SEQUENCE '
          self.WAS_DELETED = ' HAS BEEN DELETED!'
          self.DELETE = 'DELETE '
          self.FAILED = 'FAILED '
          self.SAVED = ' SAVED! '
          self.TOO_LARGE = 'TOO LARGE '
          
          
class Labels:
     def __init__(self):

          self.ENTRYCOMMANDS = '/C/ENTRYCOMMANDS'
          self.SEARCHES = '/C/ SEARCHES'
          self.CLUSTER = '/C/ CLUSTER'
          self.CONFIGURATIONS = '/C/ CONFIGURATIONS'
          self.ALL_COMMANDS = '/C/ ALL COMMANDS'
          self.ALWAYS_NEXT = '/C/ ALWAYS NEXT'
          self.ALWAYS_CHILD = '/C/ ALWAYS CHILD'
          self.MARKED = '/C/ MARKED'
          self.DEPTH = '/C/ DEPTH'
          self.DEFAULT_KEYS = '/C/ DEFAULT KEYS'
          self.GRABBED_KEYS = '/C/GRABBED KEYS'
          self.RESULT_FOR = 'RESULT FOR '
          self.INDEXES = '/C/ INDEXES'
          self.KEYS = '/C/ KEYS'
          self.ITERATOR_SHOW = '/C/ SHOW INDEXES WITH ITERATOR RESET'

          self.CAPKEYS = '/C/ CAPKEYS'
          self.PROPER_NAMES = '/C/ PROPER NAMES'
          self.OTHER_KEYS = '/C/ OTHER KEYS'
          self.SHOW_TOP = '/C/ SHOW THE TOP NOTE WITH CHILDRED'
          self.TAGS = '/C/ TAGS'
          self.PURGEKEYS = '/C/ PURGEKEY SETTINGS'
          self.FIELD = '/C/ FIELDS'
          self.FILE_ERROR = '/C/ FILE ERROR!'
          self.CONSTITUTING_KEY_FREQ = ' /C/CONSTITUTING KEY'\
                                       +' FREQUENCY DICTIONAR!'

          self.WELCOME_HEAD = '/C/ WELCOME'
          self.WELCOME_BODY = '/C/ WELCOME TO NOTESCRIPTION!'
          self.MAX_DEPTH = '/C/ MAXIMUM INDEX DEPTH'
          self.LIMIT_LIST_RESET = '/C/ LIMIT LIST RESET'
          self.LIMIT_LIST = '/C/ LIMIT LIST'
          self.FORMATTING_HELP = '/C/ FORMATTING HELP'
          self.STREAMS = '/C/ STREAM'
          self.DETERMINANT = '/C/ DETERMINANTS'
          self.HEADER = '/C/ HEADER'
          self.FOOTER = '/C/ FOOTER'
          self.LEFT_MARG ='/C/ LEFTMARGIN'
          self.AUTOBACKUP = '/C/ AUTOBACKUP'
          self.RECTIFY = '/C/ RECTIFY'
          self.AUTOMULTI ='/C/ AUTOMULTI DISPLAY'
          self.QUICK_ENTER = '/C/ QUICK ENTER'
          self.METADATA = '/C/ METADATA FOR NOTE #'
          self.CURTAIL = '/C/ CURTAIL'
          self.LIMIT_LIST_CHANGED = '/C/ LIMIT LIST CHANGED TO'
          self.SHOW_CONFIG_BOX = '/C/ SHOW CONFIGURATION IN BOXES'
          self.PURGE_KEYS = '/C/ PURGEKEY SETTINGS'
          self.KEY_TRIM = '/C/ KEY TRIM'
          self.TEXT_TRIM = '/C/ TEXT TRIM'
          self.SIZE ='/C/ SIZE'
          self.FLIPOUT = '/C/ FLIPOUT'
          self.SHORTSHOW = '/C/ SHORTSHOW'

          self.ITERATOR_SHOW = '/C/ SHOW INDEXES WITH ITERATOR RESET '
          self.NONE = '/C/ NONE '
          self.COMMAND_EQ = '/C/ COMMAND = '
          self.CONCORDANCE = '/C/ CONCORDANCE '
          self.TO_UNDO = '/C/ TO UNDO '
          self.DELETED = '/C/ DELETED NOTES '
          self.CONFIG_SAVED = '/C/ CONFIGURATION SAVED '
          self.VARIABLES = '/C/ VARIABLES '
          self.KEYS_BEFORE = '/C/ KEYS BEFORE '
          self.KEYS_AFTER = '/C/ KEYS AFTER '
          self.CARRY_OVER_KEYS = '/C/ CARRY OVER KEYS '
          self.CARRY_ALL = '/C/ CARRY OVER ALL PARENTS '
          self.SETTINGS = '/C/ SETTINGS '
          self.RETURN_QUIT_ON = '/C/ RETURNQUIT '
          self.CLUSTERS = '/C/ CLUSTERS '
          self.PROJECT_DISPLAY = '# |PROJECTNAME| INDEX |  KEYS '
          self.NEGATIVE_RESULTS = '/C/ SHOW NEGATIVE RESULTS '
          self.INDENT_MULTIPLIER = '/C/ INDENT MULTIPLIER '
          self.ITERATOR = '/C/ ITERATOR '
          self.MUST_BE_BETWEEN = '/C/ MUST BE BETWEEN '
          self.AND = ' AND '
          self.SMALL_SIZE = '/C/ SMALL SIZE '
          self.LONG_MAX = '/C/ LONGMAX '
          self.SIDE = '/C/ SIDE '
          self.SIDES = '/C/ SIDES '
          self.FLIP_AT = '/C/ FLIP AT '
          self.TAG_DEFAULT = '/C/ TAG DEFAULT '
          self.USE_SEQUENCE = '/C/ USE SEQUENCE '
          self.NO_FLASH = "/C/ DON'T SHOW FLASH CARDS "
          self.CHECK_SPELLING = '/C/ SPELL CHECK '
          self.FLASHMODE = '/C/ FLASHMODE '
          self.SHOW_DATE = '/C/ SHOW DATE '
          self.SORT_BY_DATE= '/C/ SORT BY DATE '
          self.ORDER_KEYS = '/C/ ORDER KEYS ' 
          self.ENTER_HELP= '/C/ ENTERHELP '
          self.CHILDREN_TOO = '/C/ CHILDREN TOO '
          self.SHOW_IMAGES = '/C/ SHOW IMAGES '
          self.SHOW_TEXTFILES = '/C/ SHOW TEXTFILES '
          self.DELETE_WHEN_EDITING = '/C/ DELETE WHEN EDITING '
          self.VARIABLE_SIZE = '/C/ VARIABLE SIZE '
          self.SEQUENCE_IN_TEXT = '/C/ SEQUENCE IN TEXT '
          self.MAIN_SEQUENCES = '/C/ MAIN SEQUENCES '
          self.SEQ_FORM_ONE = '/C/ FIRST SEQUENCE FORM '
          self.SEQ_FORM_TWO = '/C/ SECOND SEQUENCE FORM '
          self.FROM_TEXT = '/C/ KEYWORDS FROM TEXT'
          

          
class Spelling:
     def __init__(self):
          self.INPUT_MENU = 'Press RETURN to keep,'\
                            +'DOUBLESPACE to quit,'\
                            +'SPACE+RETURN to add,'\
                            +'enter new spelling, '\
                            +'[start with a space to ADD],'\
                            +'or a number from the following list'
          self.SMALL_INPUT_MENU = 'Press RETURN to keep,'\
                                  +'SPACE+RETURN to add,'\
                                  +'DOUBLESPACE to quit, '\
                                  +'enter new spelling '\
                                  '[start with a space to ADD]'
                                
          self.IS_MISPELLED = 'is mispelled'
          self.SPELLING_DICTIONARY = '/C/SPELLING DICTIONARY'
          self.WORDS_TO_DELETE = 'A(dd) new word\nD(elete)'\
                                 +'\nL(oad)words from text'\
                                 +'\nS(how) words\nC(hange) language'\
                                 +'\n(E)rase\n(Q)uit'
          self.TEXT_TO_ADD = 'Text to add?'
          self.ARE_YOU_SURE = 'Are you sure?'
          self.THERE_ARE = 'There are '
          self.MISSPELLED = ' misspelled words!'
          self.SKIP_CORRECTIONS = 'Press SPACE+RETURN to skip corrections'
          self.WORD_TO_ADD =  'New word to add?'
          self.WORD_TO_DELETE = 'Words to delete?'
          self.LANGUAGE_SELECT = 'es(panol) fr(ench) en(glish) de(utsch)?'
             


class DefaultConsoles:
     def __init__(self):
          self.KEY_DEF = 'KEYWORDS : DEFINITIONS'
          self.ADD_MENU = 'A)dd'
          self.DELETE_MENU = 'D)elete'
          self.SHOW_MENU = 'S)how'
          self.CLEAR_MENU= 'C)lear'
          self.QUIT_MENU = 'Q)uit'
          self.LEARN_MENU = '(L)earn'
          self.UNLEARN_MENU = '(U)nlearn'
          self.KEYMACRO = 'Keymacro'
          self.KEYS = 'Keys?'
          self.DEFINITIONS = 'Definitions?'
          self.DELETE  = 'Delete?'
          self.CLEAR = 'Are you sure you want to clear?'
          self.ADD = 'Add| '
          self.DELETING = 'DELETING'
          self.FROM_THIS = 'From this (short)? '
          self.TO_THIS = 'to this(long) ? '
          self.I_KNOW = 'I know that '
          self.IS_WHAT_IT_IS = ' is what it is'
          self.IS_AN = ' is a(n) '
          self.LEARN_THAT_THIS = 'Learn that this?'
          self.IS_WHAT = 'is what?'
          self.UNLEARN_THAT_THIS = 'Unlearn that this?'
          self.ARE_YOU_SURE = 'Are you sure you want to clear?'

labels = Labels ()
          
binary_settings =    {'showtags':('self.tagdefault',labels.TAG_DEFAULT),
                      'usesequence':('self.usesequence',labels.USE_SEQUENCE),
                      'boxconfigs':('self.box_configs', labels.SHOW_CONFIG_BOX),
                      'autobackup':('self.autobackup', labels.AUTOBACKUP),
                      'curtail':("self.default_dict['curtail']",labels.CURTAIL),
                      'itshow':("self.default_dict['setitflag']",labels.ITERATOR_SHOW),
                      'noflash':("self.no_flash",labels.NO_FLASH),
                      'spelling':("self.check_spelling",labels.CHECK_SPELLING),
                      'flashmode':("self.flipmode",labels.FLASHMODE),
                      'showdate':("self.default_dict['showdate']",labels.SHOW_DATE),
                      'sortbydate':("self.default_dict['sortbydate']",labels.SORT_BY_DATE),
                      'orderkeys':("self.default_dict['orderkeys']",labels.ORDER_KEYS),
                      'enterhelp':("self.default_dict['enterhelp']",labels.ENTER_HELP),
                      'childrentoo':("self.children_too",labels.CHILDREN_TOO),
                      'flipout':("self.flipout",labels.FLIPOUT),
                      'shortshow':("self.shortshow",labels.SHORTSHOW),
                      'fulltop':("self.show_full_top",labels.SHOW_TOP),
                      'rectify':("self.rectify",labels.RECTIFY),
                      'formathelp':("self.default_dict['formattinghelp']",labels.FORMATTING_HELP),
                      'automulti':("self.auto_multi",labels.AUTOMULTI),
                      'quickenter':("self.quickenter",labels.QUICK_ENTER),
                      'keysbefore':("self.default_dict['keysbefore']",labels.KEYS_BEFORE),
                      'keysafter':("self.default_dict['keysafter']",labels.KEYS_AFTER),
                      'carryoverkeys':("self.default_dict['carryoverkeys']",labels.CARRY_OVER_KEYS),
                      'carryall':("self.default_dict['carryall']",labels.CARRY_ALL),
                      'returnquit':("self.default_dict['returnquiton']",labels.RETURN_QUIT_ON),
                      'rqon':("self.default_dict['returnquiton']",labels.RETURN_QUIT_ON),
                      'negresults':("self.negative_results",labels.NEGATIVE_RESULTS),
                      'negativeresults':("self.negative_results",labels.NEGATIVE_RESULTS),
                      'nr':("self.negative_results",labels.NEGATIVE_RESULTS),
                      'iteratemode':("self.iteratormode",labels.ITERATOR),
                      'showimages':("self.show_images",labels.SHOW_IMAGES),
                      'showtext':("self.show_text",labels.SHOW_TEXTFILES),
                      'editdelete':("self.delete_by_edit",labels.DELETE_WHEN_EDITING),
                      'variablesize':("self.default_dict['variablesize']",labels.VARIABLE_SIZE),
                      'seqintext':("self.default_dict['sequences_in_text']",labels.SEQUENCE_IN_TEXT),
                      'fromtext':("self.default_dict['fromtext']",labels.FROM_TEXT)}
                      

LOAD_COM = 'self.loadtext_com(otherterms=otherterms,predicate=predicate)'
AUTOKEY_COM = 'self.autokey_com(mainterm=mainterm,otherterms=otherterms,predicate=predicate)'
LIMITLIST_COM = 'self.limitlist_com(mainterm=mainterm,otherterms=otherterms)'
STREAM_COM = 'self.stream_com(mainterm=mainterm,otherterms=otherterms,predicate=predicate)'
COPY_COM = 'self.copy_com (mainterm=mainterm,otherterms=otherterms,predicate=predicate)'
DEFAULT_COM = 'self.default_com(mainterm=mainterm,otherterms=otherterms)'
LOADBY_COM = 'self.loadby_com(mainterm=mainterm,otherterms=otherterms,predicate=predicate)'
ELIMINATE_COM = 'self.eliminate_com(mainterm=mainterm,otherterms=otherterms)'
DETERM_COM = 'self.determ_com(mainterm=mainterm,otherterms=otherterms,predicate=predicate)'
SPELLING_COM = 'self.spelling_com(mainterm=mainterm,longphrase=longphrase,otherterms=otherterms,predicate=predicate)'
CULKEYS_COM = 'self.culkeys_com(mainterm=mainterm)'
FLIP_COM = 'self.flip_com(mainterm=mainterm,otherterms=otherterms,longphrase=longphrase,totalterms=totalterms)'
RESIZE_COM = 'self.resize_etc_com(longphrase=longphrase,mainterm=mainterm,otherterms=otherterms,predicate=predicate,totalterms=0)'
REFORMATING_COM = 'self.reformating_com(mainterm=mainterm,otherterms=otherterms,predicate=predicate,longphrase=longphrase)'
COPY_MOVE_SEARCH_COM = 'self.copy_move_search_com(longphrase=longphrase,mainterm=mainterm,otherterms=otherterms,predicate=predicate)'
JSON_COM = 'self.json_com(longphrase=longphrase,mainterm=mainterm,otherterms=otherterms,predicate=predicate,totalterms=0)'


simple_commands =  {'dumpprojects':JSON_COM,
                    'loadprojects':JSON_COM,
                    'clearprojects':JSON_COM,
                    'setsides':RESIZE_COM,
                    'convertdefinitions':RESIZE_COM,
                    'newconvertmode':RESIZE_COM,
                    'switchconvertmode':RESIZE_COM,
                    'showallconvertmodes':RESIZE_COM,
                    'setflipat':RESIZE_COM,                  
                    'flexflip':RESIZE_COM,                    
                    'flashforward':'self.side+=1',
                    'ff':'self.side+=1',
                    'flashback':'self.side-=1',
                    'fb':'self.side-=1',
                    'flashreset':'self.side = 0',
                    'fr':'self.side = 0',
                    'ft':RESIZE_COM,
                    'flashto':RESIZE_COM,
                    'run':RESIZE_COM,
                    'interpret':RESIZE_COM,
                    'variables':'self.show_variables()',
                    'showvariables':'self.show_variables()',
                    'showvar':'self.show_variables()',
                    'clearmarks': "self.default_dict['marked'].clear()", 
                    'allchildren': 'self.iterator.change_level(0)',
                    'inc': 'self.showall_incremental(index=str(lastup))',
                    'quickall': 'self.showall(quick=True)',
                    'refresh': 'self.constitute_word_dict()',
                    'undomany': 'self.undo_many()',
                    'redo': 'self.redo()',
                    'printformout': 'print(self.format_output())',
                    'saveconfigurations': 'self.configuration.save()',
                    'loadconfigurations': 'self.configuration.load()',
                    'showconfigurations': 'self.configuration.show(self.box_configs)',
                    'killclusters': "self.set_iterator(flag=self.default_dict['setitflag'])",
                    'allknowledge': "self.default_dict['knower'].bore(self.display_buffer)",
                    'autodefaults': 'self.autodefaults()',
                    'searchlog': 'self.show_search_log()',
                    'resultlog': 'self.show_search_log(enterlist=self.result_buffer)',
                    'plainenglish': "switchlanguage(language='ple')",
                    'language':RESIZE_COM,
                    'politeenglish': "switchlanguage(language='poe')",
                    'rudeenglish': "switchlanguage(language='rue')",
                    'clearsearchlog': "self.searchlog = []",
                    'clearlog': "self.searchlog = []",
                    'changekeydefinitions': "self.default_dict['definitions'].console()",
                    'changeknowledge': "self.default_dict['knower'].console()",
                    'spelldictionary': 'self.speller.console()',
                    'keystags': 'self.keys_for_tags()',
                    'marked':'self.marked_com(mainterm=mainterm,otherterms=otherterms)',
                    'addmarks':'self.marked_com(mainterm=mainterm,otherterms=otherterms)',
                    'deletemarks':'self.marked_com(mainterm=mainterm,otherterms=otherterms)',
                    'documentation':'self.documentation_com()',
                    'showsettings':'self.show_settings()',
                    'showiterators':'self.show_iterators()',
                    'randomon':"self.iterator.random_on()",
                    'randomoff':"self.iterator.random_off()",
                    'branchone':"self.hypermovemode = 0",
                    'branchtwo':"self.hypermovemode = 1",
                    'branchthree':"self.hypermovemode = 2",
                    'loadtext':LOAD_COM,
                    'lt':LOAD_COM,
                    'echo':RESIZE_COM,
                    'clearautokeys':AUTOKEY_COM,
                    'clearkeys':AUTOKEY_COM,
                    'addkeys':AUTOKEY_COM,
                    'addkey':AUTOKEY_COM,
                    'addautokeys':AUTOKEY_COM,
                    'changekeys':AUTOKEY_COM,
                    'ak':AUTOKEY_COM,
                    'deleteautokey':AUTOKEY_COM,
                    'deletekey':AUTOKEY_COM,
                    'dk':AUTOKEY_COM,
                    'autokeys':AUTOKEY_COM,
                    'save':RESIZE_COM,
                    'defaultkeys':AUTOKEY_COM,
                    'afk':AUTOKEY_COM,
                    'showlimitlist':LIMITLIST_COM,
                    'resetlimitlist':LIMITLIST_COM,
                    'resetll':LIMITLIST_COM,
                    'limitlist':LIMITLIST_COM,
                    'streams':STREAM_COM,
                    'deletestream':STREAM_COM,
                    'copyto':COPY_COM,
                    'copyfrom':COPY_COM,
                    'clearcommandmacros':DEFAULT_COM,
                    'clearknowledge':DEFAULT_COM,
                    'clearcodes':DEFAULT_COM,
                    'clearmacros':DEFAULT_COM,
                    'clearkeydefinitions':DEFAULT_COM, 
                    'clearkeymacros':DEFAULT_COM,
                    'defaultcommandmacros':DEFAULT_COM,
                    'defaultkeymacros':DEFAULT_COM,
                    'recordkeydefinitions':DEFAULT_COM,
                    'recordkeymacros':DEFAULT_COM,
                    'recordcodes':DEFAULT_COM,
                    'recordmacros':DEFAULT_COM,
                    'recordknowledge':DEFAULT_COM,
                    'recordcommandmacros':DEFAULT_COM,
                    'changecodes':DEFAULT_COM,
                    'changemacros':DEFAULT_COM,
                    'changekeymacros':DEFAULT_COM,
                    'changecommandmacros':DEFAULT_COM,
                    'learn':DEFAULT_COM,
                    'forget':DEFAULT_COM,
                    'defaultcodes':DEFAULT_COM,
                    'clearcodes':DEFAULT_COM,
                    'defaultmacros':DEFAULT_COM,
                    'defaultknowledge':DEFAULT_COM,
                    'defaultkeydefinitions':DEFAULT_COM,
                    'loadbyparagraph':LOADBY_COM,
                    'splitload':LOADBY_COM,
                    'deletedefaultkeys':AUTOKEY_COM,
                    'deleteautokeys':AUTOKEY_COM,
                    'eliminateblanks':ELIMINATE_COM,
                    'eliminatekeys':ELIMINATE_COM,
                    'changedeterminant':DETERM_COM,
                    'changedet':DETERM_COM,
                    'showdeterminant':DETERM_COM,
                    'showdet':DETERM_COM,
                    'clearpurgekeys':DETERM_COM,
                    'setpurgekeys':DETERM_COM,
                    'showpurgekeys':DETERM_COM,
                    'showspelling':SPELLING_COM,
                    'defaultspelling':SPELLING_COM,
                    'capkeys':CULKEYS_COM,
                    'upperkeys':CULKEYS_COM,
                    'lowerkeys':CULKEYS_COM,
                    'flipbook':FLIP_COM,
                    'showflip':FLIP_COM,
                    'runinterpret':RESIZE_COM,
                    'showflipbook':FLIP_COM,
                    'conflate':RESIZE_COM,
                    'undo':RESIZE_COM,
                    'deletefield':RESIZE_COM,
                    'fields':RESIZE_COM,
                    'resize':RESIZE_COM,
                    'size':RESIZE_COM,
                    'sz':RESIZE_COM,
                    'keytrim':RESIZE_COM,
                    'texttrim':RESIZE_COM,
                    'editnote':RESIZE_COM,
                    'explode':RESIZE_COM,
                    'load':RESIZE_COM,
                    'en':RESIZE_COM,
                    'editnotekeys':RESIZE_COM,
                    'indentmultiplier':RESIZE_COM,
                    'setreturnquit':RESIZE_COM,
                    'enk':RESIZE_COM,
                    'editnotetext':RESIZE_COM,
                    'ent':RESIZE_COM,
                    'compress':RESIZE_COM,
                    'rehome':RESIZE_COM,
                    'showdel':RESIZE_COM,
                    'permdel':RESIZE_COM,
                    'clear':RESIZE_COM,
                    'undel':RESIZE_COM,
                    'addfield':RESIZE_COM,
                    'cluster':RESIZE_COM,
                    'descendents':RESIZE_COM,
                    'cpara':RESIZE_COM,
                    SEMICOLON:RESIZE_COM,
                    'setlongmax':RESIZE_COM,
                    'purgefrom':RESIZE_COM,
                    'showuser':RESIZE_COM,
                    'link':RESIZE_COM,
                    'loop':RESIZE_COM,
                    'chain':RESIZE_COM,
                    'unlink':RESIZE_COM,
                    'newkeys':RESIZE_COM,
                    'header':RESIZE_COM,
                    'footer':RESIZE_COM,
                    'leftmargin':RESIZE_COM,
                    'deeper':RESIZE_COM,
                    'shallower':RESIZE_COM,
                    'testdate':RESIZE_COM,
                    'changeuser':RESIZE_COM,
                    'formout':RESIZE_COM,
                    'findwithin':RESIZE_COM,
                    'inspect':RESIZE_COM,
                    'updatetags':RESIZE_COM,
                    'showmeta':RESIZE_COM,
                    'text':COPY_MOVE_SEARCH_COM,
                    'depth':RESIZE_COM,
                    'delete':RESIZE_COM,
                    'showsequences':RESIZE_COM,
                    'del':RESIZE_COM,
                    'gc':RESIZE_COM,
                    'gocluster':RESIZE_COM,
                    'd':RESIZE_COM,
                    'killchild':RESIZE_COM,
                    'all':RESIZE_COM,
                    DOLLAR:RESIZE_COM,
                    DOLLAR+DOLLAR:RESIZE_COM,
                    'show':RESIZE_COM,
                    's':RESIZE_COM, 
                    'histogram':RESIZE_COM,
                    'keysfortags':RESIZE_COM,
                    'terms':RESIZE_COM,
                    '???':RESIZE_COM,
                    'indexes':RESIZE_COM,
                    'ind':RESIZE_COM,
                    'i':RESIZE_COM,
                    'reform':RESIZE_COM,
                    'override':RESIZE_COM,
                    'showdepth':RESIZE_COM,
                    'refreshfreq':RESIZE_COM,
                    'cleardatedict':RESIZE_COM,
                    'multi':RESIZE_COM,
                    'showstream':RESIZE_COM,
                    'constdates':RESIZE_COM,
                    'constitutedates':RESIZE_COM,
                    'showdatedict':RESIZE_COM,
                    'showdatedictpurge':RESIZE_COM,
                    'makedates':RESIZE_COM,
                    'actdet':RESIZE_COM,
                    'put':RESIZE_COM,
                    'activedet':RESIZE_COM,
                    'grabkeys':RESIZE_COM,
                    'invert':RESIZE_COM,
                    'correctkeys':REFORMATING_COM,
                    'help':RESIZE_COM,
                    'grabdefaultkeys':RESIZE_COM,
                    'smallsize':RESIZE_COM,
                    'grabautokeys':RESIZE_COM,
                    'mergemany':REFORMATING_COM,
                    'mm':REFORMATING_COM,
                    'columns':REFORMATING_COM,
                    'col':REFORMATING_COM,
                    'split':REFORMATING_COM,
                    'helpall':REFORMATING_COM,
                    'sidenote':REFORMATING_COM,
                    'revise':REFORMATING_COM,
                    'rev':REFORMATING_COM,
                    'keys':COPY_MOVE_SEARCH_COM,
                    'key':COPY_MOVE_SEARCH_COM,
                    'k':COPY_MOVE_SEARCH_COM,
                    'search':COPY_MOVE_SEARCH_COM,
                    QUESTIONMARK:COPY_MOVE_SEARCH_COM,
                    'move':COPY_MOVE_SEARCH_COM,
                    'copy':COPY_MOVE_SEARCH_COM,
                    'dictionaryload':RESIZE_COM,
                    'seqformone':RESIZE_COM,
                    'seqformtwo':RESIZE_COM,
                    'mainsequences':RESIZE_COM}         
          
          





