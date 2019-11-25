"""Global constants
pylint rated 10.0/10
"""

import string

ANDSIGN = '&'

LEFTCURLY = '{'

RIGHTCURLY = '}'

LEFTPAREN = '('

RIGHTPAREN = ')'

LEFTBRACKET = '['

RIGHTBRACKET = ']'

ATSIGN = '@'

POUND = '#'

CARET = '^'

PLUS = '+'

STAR = '*'

QUESTIONMARK = '?'

PERIOD = '.'

COLON = ':'

SEMICOLON = ';'

EQUAL = '='

COMMA = ','

EXCLAMATION = '!'

DOLLAR = '$'

PERCENTAGE = '%'

EMPTYCHAR = ''

VERTLINE = '|'

LONGDASH = '—'

BLANK = ' '

TAB = '\t'

EOL = '\n'

LEFTNOTE = '<'

RIGHTNOTE = '>'

SLASH = '/'

DASH = '-'

TILDA = '~'

UNDERLINE = '_'

BACKSLASH = '\\'

COMMABLANK = COMMA + BLANK

BOX_CHAR = {'v':'│',
            'h':'─',
            'lu':'┌',
            'ru':'┐',
            'lm':'├',
            'rm':'┤',
            'll':'└',
            'rl':'┘',
            'xl':'┬',
            'xu':'┴',
            'x':'┼'}

BOX_CHAR_NORMAL = {'v':'│',
                   'h':'─',
                   'lu':'┌',
                   'ru':'┐',
                   'lm':'├',
                   'rm':'┤',
                   'll':'└',
                   'rl':'┘',
                   'xl':'┬',
                   'xu':'┴',
                   'x':'┼'}

BOX_CHAR_ROUND = {'v':'│',
                  'h':'─',
                  'lu':'╭',
                  'ru':'╮',
                  'lm':'├',
                  'rm':'┤',
                  'll':'╰',
                  'rl':'╯',
                  'xl':'┬',
                  'xu':'┴',
                  'x':'┼'}

BOX_CHAR_THICK = {'v':'┃',
                  'h':'━',
                  'lu':'┏',
                  'ru':'┓',
                  'lm':'┣',
                  'rm':'┫',
                  'll':'┗',
                  'rl':'┛',
                  'xl':'┳',
                  'xu':'┻',
                  'x':'╋'}

BOX_CHAR_DOUBLE = {'v':'║',
                  'h':'═',
                  'lu':'╔',
                  'ru':'╗',
                  'lm':'╠',
                  'rm':'╣',
                  'll':'╚',
                  'rl':'╝',
                  'xl':'╦',
                  'xu':'╩',
                  'x':'╬'}



KNOWLEDGEITERATIONS = 20

MARGINFACTOR = 3.0
        #marginfactor is used to determine
        #the size of the margin. Too small wasted space,
        #too large causes note overflow.

OPENING_WIDTH = 200

KEYLENGTH = 200

VOIDTERM = 'VOID'

SMALLWORDS = ['and',
              'or',
              'not',
              'but',
              'how']

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

ADDTERMS = ['A',
            'a',
            'add',
            'ADD',
            'Add']

DELETETERMS = ['D',
               'd',
               'Delete',
               'delete',
               'DELETE']

SHOWTERMS = ['S',
             's',
             'Show',
             'show',
             'SHOW']

QUITTERMS = ['Q',
             'q',
             'Quit',
             'quit',
             'QUIT']

CLEARTERMS = ['C',
              'c',
              'clear',
              'CLEAR',
              'Clear']

QUITALLTERMS = ['a',
                'A',
                'quitall',
                'QUITALL']

LEARNTERMS = ['L',
              'l',
              'learn',
              'LEARN',
              'Learn']

UNLEARNTERMS = ['U',
                'u',
                'unlearn',
                'UNLEARN',
                'Unlearn']

BREAKTERMS = ['b',
              'B',
              'BREAK',
              'break',
              'Break']

NEWTERMS = ['n',
            'N',
            'NEW',
            'new',
            'New']



##LEFTDETERMINANTS = ['y',
##                    'm',
##                    'd',
##                    'ymd',
##                    'md',
##                    'yd',
##                    '']
##
##RIGHTDETERMINANTS = 'h',

DELETECHARACTERS = string.punctuation+string.whitespace.replace(DASH,EMPTYCHAR) + '�”“‘’»«— „'


INTROSCRIPT = """
%┎────────────────────────────────────────────────────────────────────────────────────┒
%┃                                                                                    ┃
%┃             █      ███      ███       █      ████     █████    ███                 ┃
%┃            █ █     █  █    █   █     █ █     █   █    █       █   █                ┃
%┃           █   █    ████    █        █   █    █   █    ███      ██                  ┃
%┃           █████    █ █     █        █████    █   █    █          █                 ┃
%┃           █   █    █  █    █   █    █   █    █   █    █       █   █                ┃
%┃           █   █    █   █    ███     █   █    ████     █████    ███                 ┃
%┃                                                                                    ┃
%┃                                                                                    ┃
%┃                        ACADEMIC NOTE-TAKE SOFTWARE WITH A                          ┃
%┃                             TEXT-ONLY INTERFACE                                    ┃
%┃                                                                                    ┃
%┃                     Copyright 2018 Anthony Curtis Adler                            ┃
%┃                                                                                    ┃
%┃Permission is hereby granted, free of charge, to any person obtaining a copy of this┃
%┃software and associated documentation files (the "Software"),to deal in the Software┃
%┃without restriction, including without limitation the rights to use, copy, modify,  ┃
%┃merge, publish, distribute, sublicense, and/or sell copies of the Software, and to  ┃
%┃permit persons to whom the Software is furnished to do so, subject to the following ┃
%┃conditions:                                                                         ┃
%┃                                                                                    ┃
%┃The above copyright notice and this permission notice shall be included             ┃
%┃in all copiesor substantial portions of the Software.                               ┃
%┃                                                                                    ┃
%┃THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, ┃
%┃INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A       ┃
%┃PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT  ┃
%┃HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF┃
%┃CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE┃
%┃OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                       ┃
%┖────────────────────────────────────────────────────────────────────────────────────┚
"""


ENTERSCRIPT = """% for the PROSE mode.
%% for the POETRY mode.
~ to discard line.
# to replace last line with new line.
@ to replace entered line with new line with EOL.
$ to replace entered line with new line without EOL.
| for a EOL in PROSE mode.
|| to quit.
~| to quit and edit."""


FORMATTINGSCRIPT = """
/BREAK/ to ADD a BREAK.
/NEW/ to divide into a SEPARATE NOTE.
[INT] to change size of note.
/DEF/ to return to default size

/COL/ To initiate columns by line.
_ to separate columns on the line.
/ENDCOL/ To terminate columns

/SPlIT/ To initiate columns by chunk
/M/ To separate chunks of text
/ENDSPLIT/ To terminate columns

/C / To center (no space)
/R / To right (no space)


"""









