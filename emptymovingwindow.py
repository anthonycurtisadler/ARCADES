
import curses
from conway import Conway
from drawingobject import DrawingObject
import time
from loopfinder import LoopFinder 
from movingwindow import MovingWindow
from stack import Stack 
from math import sqrt, cos, sin
import winsound
from globalconstants import BOX_CHAR,\
     BOX_CHAR_NORMAL,\
     BOX_CHAR_THICK,\
     BOX_CHAR_ROUND,\
     BOX_CHAR_DOUBLE
import copy
from itertools import cycle
from indexclass import Index
from indexutilities import index_expand
from randomdirection import find_direction
from limitedstack import LimitedStack
from randomdirectionclass import Movement
import datetime 

import os
from globalconstants import EMPTYCHAR, SLASH
import random


help_script = ['F2 = to enter a note']+['F3 = to switch modes']+\
              ['shift F3 = to switch linetype']+\
               ['F4 = to contract or extend the workpad']+\
               ['TAB = to toggle through notes']+\
               ['F5 = to move selected objects']+\
               ['F6 = to move screen while moving selected objects']+\
               ['F7 = to select an object to move']+\
               ['F8 = to delect an object to move']+\
               ['F9 = to toggle between cycle or select']+\
               ['F10 = to exit']+\
               ['F11 = to dump stack']+\
               ['shift F12 = help menu']+\
               ['[ = page up']+\
               ['] = page down']+\
               ['{ = page left']+\
               ['} = page right']+\
               ['z = decrease speed']+\
               ['x = increase speed']+\
               ['o =move through workpad']+\
               ['n = automatically cycle through notes']+\
               ['m =set objects in motion/activate conway']+\
               ['ctrl c = copy']+\
               ['ctrl v = paste']+\
               ['ctrl a = screen shot']+\
               ['ctrl s = save text']+\
               ['insert = to add note from stack']+\
               ['delete = to return note from stack']


help_script2 = ['ARROW KEYS = draw object']+\
               ['FUNC+ARROW = move without drawing']+\
               ['.  contract horizontally']+\
               ['% set on conway mode']+\
               ['TAB next drawing character']+\
               ['shift F11 next drawing palette']+\
               ['* fill out space']+\
               ['BACKSPACE previous drawing character']+\
               ['> stretch horizontally']+\
               [', contract vertically']+\
               ['< stretch vertically']+\
               ['| flip object on vertical axis']+\
               ['_ flip object on horizontal axis']+\
               ['+ rotate object']+\
               ['= atomize object']


helpscripts = {0:help_script,
               1:help_script2}




painting_chars ={(curses.KEY_RIGHT,curses.KEY_RIGHT):('h',0,1),
                     (curses.KEY_LEFT,curses.KEY_LEFT):('h',0,-1),
                     (curses.KEY_RIGHT,curses.KEY_UP):('rl',-1,0,),
                     (curses.KEY_RIGHT,curses.KEY_DOWN):('ru',1,0),
                     (curses.KEY_LEFT,curses.KEY_UP):('ll',-1,0),
                     (curses.KEY_LEFT,curses.KEY_DOWN):('lu',1,0),
                     (curses.KEY_UP,curses.KEY_UP):('v',-1,0),
                     (curses.KEY_DOWN,curses.KEY_DOWN):('v',1,0),
                     (curses.KEY_UP,curses.KEY_LEFT):('ru',0,-1),
                     (curses.KEY_UP,curses.KEY_RIGHT):('lu',0,1),
                     (curses.KEY_DOWN,curses.KEY_LEFT):('rl',0,-1),
                     (curses.KEY_DOWN,curses.KEY_RIGHT):('ll',0,1),
                     (curses.KEY_RIGHT,curses.KEY_LEFT):('h',0,0),
                     (curses.KEY_LEFT,curses.KEY_RIGHT):('h',0,0),
                     (curses.KEY_UP,curses.KEY_DOWN):('v',0,0),
                     (curses.KEY_DOWN,curses.KEY_UP):('v',0,0),
                     ('',curses.KEY_UP):('v',-1,0),
                     ('',curses.KEY_DOWN):('v',1,0),
                     ('',curses.KEY_LEFT):('h',0,-1),
                     ('',curses.KEY_RIGHT):('h',0,1)}


drawing_chars = {}
drawing_chars[0] = cycle("┼ █░▒▓╭╮╯╰╱╲╳")
drawing_chars[1] = cycle('>■□▪▫▬▲▴▸►▼▾◂◄◊○◌●◙◦')
drawing_chars[2] = cycle('┅┆┇┈┉┊┋╌╍╎╏')
drawing_chars[3] = cycle('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUZWXYZ')
drawing_chars[4] = cycle('1234567890')
drawing_chars[5] = cycle('!@#$%^&*()_-+={}[]<>,.?/')
drawing_keys = cycle(drawing_chars.keys())




boxchar_decomp = {'v':((False,True,False),(False,True,False),(False,True,False)),  # vertical 
                 'h':((False,False,False),(True,True,True),(False,False,False)),   # horizontal 
                 'lu':((False,False,False),(False,True,True),(False,True,False)), #'┎'
                 'ru':((False,False,False),(True,True,False),(False,True,False)), #'┒'
                 'lm':((False,True,False),(False,True,True),(False,True,False)), #'┠'
                 'rm':((False,True,False),(True,True,False),(False,True,False)), #'┨'
                 'll':((False,True,False),(False,True,True),(False,False,False)), #'┖'
                 'rl':((False,True,False),(True,True,False),(False,False,False)), #'┚'
                 'xl':((False,False,False),(True,True,True),(False,True,False)),  # '┬'
                 'xu':((False,True,False),(True,True,True),(False,False,False)),  # '┴'
                 'x': ((False,True,False),(True,True,True),(False,True,False))}  # '┼'

top_touching = set()
bottom_touching = set()
left_touching = set()
right_touching = set()

for x in boxchar_decomp:

     if boxchar_decomp[x][0][1]:
          top_touching.add(x)
     if boxchar_decomp[x][2][1]:
          bottom_touching.add(x)
     if boxchar_decomp[x][1][0]:
          left_touching.add(x)
     if boxchar_decomp[x][1][2]:
          right_touching.add(x)

##BOX_CHAR_REVERSE = {}
##for x in BOX_CHAR:
##     BOX_CHAR_REVERSE[BOX_CHAR[x]] = x

boxchar_recomp  = {}
for x in boxchar_decomp:
     boxchar_recomp[boxchar_decomp[x]] = x



curses.KEY_RETURN = 10
curses.KEY_TAB = 9
curses.KEY_F1 = 265
curses.KEY_F2 = 266
curses.KEY_F3 = 267
curses.KEY_F4 = 268
curses.KEY_F5 = 269
curses.KEY_F6 = 270
curses.KEY_F7 = 271
curses.KEY_F8 = 272
curses.KEY_F9 = 273
curses.KEY_F10 = 274
curses.KEY_F11 = 275

curses.KEY_PAGEUP = 339
curses.KEY_PAGEDOWN = 338
curses.KEY_HOME = 262
curses.KEY_END = 35

curses.KEY_BACKSPACE = 8
curses.KEY_INSERT = 331
curses.KEY_DELETE = 330
 
keys = {curses.KEY_LEFT:(0,-1),
        curses.KEY_RIGHT:(0,1),
        curses.KEY_UP:(-1,0),
        curses.KEY_DOWN:(1,0)}


ec_keys = {curses.KEY_LEFT:(0,0,1,0),
           curses.KEY_RIGHT:(0,0,0,1),
           curses.KEY_UP:(1,0,0,0),
           curses.KEY_DOWN:(0,1,0,0)}


def trace (x):
     #for debugging 

     print({}[x])

     
def save_file(returntext=EMPTYCHAR,
              filename=EMPTYCHAR,
              folder=os.altsep+'textfiles'):

    """for saving a file"""
    
              
    directoryname = os.getcwd()+folder
    with open(directoryname+os.altsep
                    +filename+'.txt',
                    'x',
                    encoding='utf-8') as textfile:
         textfile.write(returntext.replace('\ufeff', EMPTYCHAR))
          

    return 'Saved to ' + directoryname+SLASH+filename+'.txt'

def fill (textlist):

     """ returns a list of strings of equal length"""

     try:
          width = max ([len(x) for x in textlist])
     except:
          return []
     returnlist = []
     for line in textlist:
          returnlist.append(line+(width-len(line))*' ')
     return returnlist

def simple_rectangle (height,width):

     """Creates a block character rectangle of the given dimension"""
     
     textlist = []

     for y in range(0,height):

          if y == 0:
               textlist.append(BOX_CHAR['lu']+BOX_CHAR['h']*(width-2)+BOX_CHAR['ru'])
          elif 0 < y < height-1:
               textlist.append(BOX_CHAR['v']+' '*(width-2)+BOX_CHAR['v'])
          else:
               textlist.append(BOX_CHAR['ll'] + BOX_CHAR['h']*(width-2) + BOX_CHAR['rl'])

               
     return textlist


def return_boxed_note (schema=None):

     if not schema:
          return ''

     y_coords = [c[0] for c in schema]
     x_coords = [c[1] for c in schema]
               
     min_y = min(y_coords)
     min_x = min(x_coords)
     max_y = max(y_coords)
     max_x = max(x_coords)

     height = (max_y - min_y) + 4
     width = (max_x - min_x) + 4
     textlist = simple_rectangle(height=height,width=width)

     for c in schema:

          y = c[0]+2
          x = c[1]+2
          new_char = schema[c]
          
          textlist[y] = textlist[y][0:x] + new_char + textlist[y][x+1:]
     return '\n'.join(textlist)
              

class ScrollPad:

     """ A simple scroll pad/ text editor"""

     def __init__(self,
                  height=10,
                  width=10,
                  y_pos=5,
                  x_pos=5,
                  u_margin=0,
                  l_margin=0,
                  enframe=False,
                  screen=None,
                  textlist=None,
                  bufferobject_redo=None,
                  bufferobject_undo=None):
          
          self.height = height  # height of entry box
          self.width = width    # length of entry text
          self.top_line = 0     # the topline of displayed text
          self.cursor_y = 0     # cursor position when inputing
          self.cursor_x = 0
          self.u_margin = u_margin  
          self.l_margin = l_margin 
          if textlist is None:
               self.textlist = [' ']*self.height   #the total text
          else: #for editing an existing note
               self.textlist = textlist
               try:
                    self.width = min([self.width,max([len(x) for x in textlist])])
                    self.height = min([self.height,len(textlist)])
               except:
                    pass
                      
               
          self.window = screen
          self.y_pos = y_pos  # for the relation of the entry
          self.x_pos = x_pos  # to the screen in which it is place
          self.highlighted_coords = set()
          self.selected_coords = set()
          self.text_buffer = ''
          if bufferobject_redo:
               self.bufferobject_redo = bufferobject_redo
          if bufferobject_undo:
               self.bufferobject_undo = bufferobject_undo
               

     def copy_self (self):
          return (list(self.textlist),
                  set(self.highlighted_coords),
                  set(self.selected_coords),
                  self.height,self.width,
                  self.top_line,
                  self.cursor_y,
                  self.cursor_x,
                  self.y_pos,
                  self.x_pos,
                  self.text_buffer)
     
     def change_self (self,other):

          if not other:
               return 

          self.textlist, self.highlighted_coords, self.selected_coords = list(other[0]),set(other[1]),set(other[2])

          self.height, self.width, self.top_line = other[3],other[4],other[5]

          self.cursor_y, self.cursor_x, self.y_pos, self.x_pos, self.text_buffer = other[6],other[7],other[8],other[9],other[10]

     
     def put_in (self,y_start,x_start,fromtextlist=None,totextlist=None,skip=[' ']):

          """ places one textlist inside another textlist """

          for y in range(len(fromtextlist)):
               if y_start+y < len(totextlist):
                    
                    newline = totextlist[y_start+y][0:min(len(totextlist[y_start+y])-1,x_start)]
                    for x in range(len(fromtextlist[y])):
                         if fromtextlist[y][x] not in skip:
                              newline+=fromtextlist[y][x]
                         else:
                              if x_start+x < len(totextlist[y_start+y]):
                                   newline+=totextlist[y_start+y][x_start+x]
                                   
                              else:
                                   newline+=' '
                    if x_start+x+1 < len(totextlist[y_start+y]):
                         newline += totextlist[y_start+y][x_start+x+1:]
                                   
                    
                    if y_start+y < len(totextlist[y_start+y]):
                         totextlist[y_start+y] = newline

                    
          return totextlist

     def add_line (self,lines=1):

          """adds a new line to the end of the text list"""
          
          self.textlist += [' '*self.width]*lines
         

     def scroll_down (self):
          if self.top_line + self.height < len(self.textlist):
          
               self.top_line +=1

     def scroll_up (self):
          if self.top_line > 0:
               self.top_line -=1



     def move_up (self): 

          if self.cursor_y > 0:
               self.cursor_y -= 1
          if self.cursor_y < self.top_line:
               self.top_line -= 1

     def move_down (self,add_to_line=None):

          
          self.cursor_y += 1
          if add_to_line:
               if self.top_line+self.cursor_y < len(self.textlist):
                    self.textlist[self.top_line+self.cursor_y] = add_to_line
               else:
                    self.textlist += [add_to_line]
               self.cursor_x = len(add_to_line)
          if self.cursor_y >= self.height:
     
               self.top_line += 1
               self.cursor_y -=1

               if self.top_line + self.height > len(self.textlist):
                    self.add_line()

               self.put_all()

     def move_right (self,char=None):
          add_to_line = ''
          if self.cursor_x < self.width-1:
               self.cursor_x += 1
               return 'EOL'
          elif self.cursor_x >=self.width-1:
               
##               if self.cursor_y < len(self.textlist)-1:

               if char != ' ':
                    if ' ' in self.textlist[self.cursor_y]:
                         add_to_line = self.textlist[self.top_line+self.cursor_y].split(' ')[-1]
               
                    
               self.cursor_x = 0
               if ' ' in self.textlist[self.top_line + self.cursor_y]:
                    self.textlist[self.top_line + self.cursor_y] = ' '.join(self.textlist[self.top_line + self.cursor_y].split(' ')[0:-1])+'\n'
                    self.move_down(add_to_line=add_to_line)
               else:
                    self.textlist[self.top_line + self.cursor_y] = self.textlist[self.top_line + self.cursor_y][0:self.width]
                    add_to_line = self.textlist[self.top_line + self.cursor_y][self.width:]
                    self.move_down(add_to_line)
               
               return 'EOT'


     def hard_return (self):


          line = self.textlist[self.cursor_y]
          left_of = line[0:self.cursor_x]
          right_of = line[self.cursor_x:]
          self.textlist = self.textlist[0:self.cursor_y] + [left_of] + [right_of] + self.textlist[self.cursor_y+1:]
          self.cursor_x = 0
          self.move_down()
          

     def move_left (self):

          if self.cursor_x > 0:
               self.cursor_x -=1
          else:  
               if self.cursor_y > 0:
                    self.cursor_x = len(self.textlist[self.cursor_y+self.top_line-1])
                    self.move_up()
               else:
                    self.cursor_x = 0
                    



     def put_char (self,char,y=None,x=None,insert=True):

          """ places a character in the textlist """
          if y is None:
               y = self.cursor_y
          if x is None:
               x = self.cursor_x

          if 0 <= y < self.height and self.cursor_y+self.top_line < len(self.textlist) and 0 <= x < self.width:


               self.textlist[self.cursor_y+self.top_line] = self.textlist[self.cursor_y+self.top_line][0:self.cursor_x]\
                                                           +char+self.textlist[self.cursor_y+self.top_line][self.cursor_x+(not insert):]
               self.window.refresh()
          else:
               self.cursor_y -= 1
               self.cursor_x -= 1

               self.cursor_y = max([0,self.cursor_y])
               self.cursor_x = max([0,self.cursor_x])

     def finalize (self):

          """ returns a list of strings of equal length """

          def force_length (line='',length=0):

               line = line.rstrip(' ').replace('\n','')
               if len(line) == length:
                    return line
               elif len(line) > length:
                    return line[0:length]
               return line + ' '*(length-len(line))
          for y in range(0,len(self.textlist)):
               self.textlist[y] = force_length(line=self.textlist[y],length=self.width)

          for y in reversed(range(self.height+1,len(self.textlist))):
               if not self.textlist[y].rstrip():
                    self.textlist = self.textlist[0:-1]
               else:
                    break
 
     def cascade (self,line_from=0):

          """ carries over a word partially crossed over
          the right margin down to the next line
          Repeats for subsequent lines.
          """

          for y in range(line_from,len(self.textlist)-1):

               if len(self.textlist[y])>self.width:
                    if ' ' in self.textlist[y]:
                         add_to_text = self.textlist[y].split(' ')[-1]
                         self.textlist[y] = ' '.join(self.textlist[y].split(' ')[0:-1])
                    else:
                         add_to_text = ''

                    self.textlist[y+1] = add_to_text + ' ' + self.textlist[y+1]
          while len(self.textlist[-1]) > self.width:
               if ' ' in self.textlist[-1][0:self.width]:
                    add_to_line = self.textlist[-1][0:self.width].split(' ')[-1]+self.textlist[-1][self.width:]
                    self.textlist[-1] = ' '.join(self.textlist[-1][0:self.width].split(' ')[0:-1])
                    self.textlist += [add_to_line+' ']
               else:
                    self.textlist[-1] = self.textlist[-1][0:self.width]
                    self.textlist += self.textlist[-1][self.width:]

     def purge_empty_lines (self,line_from=0,line_to=None):
          """Removes empty lines from textlist"""

          if not line_to:
               line_to = len(self.textlist)-1

          deleted = 0

          for y in reversed(range(line_from,line_to+1)):
               if not self.textlist[y].strip():
                    self.textlist = self.textlist[0:y]+self.textlist[y+1:]
                    deleted += 1
          self.textlist += deleted * [' ']
          
     def find_first_empty_line (self,line_from=0,line_to=None):

          """ Notice that line_to is inclusive"""
          
          if not line_to:
               line_to = len(self.textlist)-1
          if line_from >= line_to+1:
               return 0
          last_empty = False
          for y in range(line_from,line_to+1):
               if self.textlist[y].startswith('  ') or (not self.textlist[y].strip() and last_empty):
                    break
               if not self.textlist[y].strip():
                    last_empty = True
          return y 
     
                    
     def reverse_cascade (self,line_from=0,line_to=None):

          """Fills in spaces in the lines above with complete words"""

          def modified_strip(x):
               if x.startswith('  '):
                    return x
               else:
                    return x.lstrip()

          if line_to is None:
               line_to = len(self.textlist)

  
          while True:

               oldtextlist = list(self.textlist)   
          
               for y in range(line_from,line_to):
                    if y < line_to-1:
                         while True:
                              remaining  = self.width - len(self.textlist[y].rstrip())
                              word = ''
                              if ' ' in self.textlist[y+1]:
                                   word = self.textlist[y+1].split(' ')[0]
                              elif self.textlist[y+1].strip():
                                   word = self.textlist[y+1]

                              if word.strip() and len(word.strip()) < remaining:
                                   self.textlist[y] = modified_strip((self.textlist[y].rstrip() + ' ' + word.strip()))
                                   self.textlist[y+1] = modified_strip(' '.join(self.textlist[y+1].split(' ')[1:]))

                              elif not word.strip() and len(word) > 0:
                                   self.textlist[y+1] = self.textlist[y+1][len(word):]
                              else:
                                   break

               if self.textlist == oldtextlist:
                    break
                              
          self.purge_empty_lines(line_from=line_from,line_to=line_to)
               

     def put_all (self,lines=None):

          """Displays a sections of the textlist in the window"""


          text_line = self.top_line
          y = 0
          
          
          while text_line < len(self.textlist):

               if (lines and text_line in lines) or (not lines and self.top_line <= text_line < self.top_line+self.height):

                    for x in range (0,self.width):
                         add_char = (self.textlist[text_line]+' '*self.width)[x].replace('\n',' ')
                         if (y==self.cursor_y and x==self.cursor_x) or (y+self.top_line,x) in self.highlighted_coords:
                              try:
                                   self.window.addch(self.y_pos+y+self.u_margin,self.x_pos+x+2+self.l_margin,add_char,curses.A_REVERSE)
                              except:
                                   pass
                              
                         else:
                              try:
                                   self.window.addch(self.y_pos+y+self.u_margin,self.x_pos+x+2+self.l_margin,add_char,curses.A_NORMAL)
                              except:
                                   pass
                         
               self.window.refresh()
               y += 1
               text_line += 1


     def collect_text(self,gather=True,delete=False):

          if not self.selected_coords:
               return ''
          temp_list =  sorted(list(self.selected_coords))
          
          
          starting = True
          line_at = 0
          first_line = 0
          returntext = ''
          for temp_xy in temp_list:
               if starting:
                    line_at = temp_xy[0]
                    first_line = line_at
                    starting = False
               if temp_xy[0] > line_at:
                    returntext += '\n'
                    line_at = temp_xy[0]
                    
               returntext += temp_xy[2]



          if delete:
               temp_list.sort(key=lambda x:(x[0],-x[1]))  #to make sure that text deletion is from left to right 
               for temp_xy in temp_list:
                         self.textlist[temp_xy[0]] = self.textlist[temp_xy[0]][0:temp_xy[1]]+self.textlist[temp_xy[0]][temp_xy[1]+1:]

          old_textlist = list(self.textlist)
          self.textlist = [x for x in self.textlist if x.strip()]
          self.textlist += (len(old_textlist)-len(self.textlist))*[' ']
          self.selected_coords, self.highlighted_coords = set(), set()
          
          return returntext, first_line
        

     def get_highlighted(self,start_yx=None,end_yx=None):

          
          def get_coords (y,up_to=None,after=None,line=None):
               returnset = set()
               if up_to and not after:
                    for x_temp in range(0,up_to+1):
                         if x_temp < len(line):
                              returnset.add((y,x_temp,line[x_temp]))
               elif after:
                    if after < len(line):
                         if not up_to:
                              for x_temp in range(after,len(line)):
                                   returnset.add((y,x_temp,line[x_temp]))
                         elif up_to > after:
                              for x_temp in range(after,up_to):
                                   returnset.add((y,x_temp,line[x_temp]))
                         else:
                              for x_temp in range(up_to,after):
                                   returnset.add((y,x_temp,line[x_temp]))
                         
                              
                              
               else:
                    for x_temp in range(0,len(line)):
                         returnset.add((y,x_temp,line[x_temp]))
               return returnset
          if not start_yx or not end_yx:
               return set(),set()
          returnset = set()
          if start_yx > end_yx:
               start_yx, end_yx = end_yx, start_yx
          if start_yx == end_yx:
               return set(),set()
          if  start_yx[0] != end_yx[0]:
               for y_temp in range(start_yx[0],end_yx[0]+1):
   
                    if y_temp == start_yx[0]:
                         returnset.update(get_coords(y_temp,after=start_yx[1],line=self.textlist[y_temp]))
                    elif y_temp == end_yx[0]:
                         returnset.update(get_coords(y_temp,up_to=end_yx[1],line=self.textlist[y_temp]))
                    else:
                         returnset.update(get_coords(y_temp,line=self.textlist[y_temp]))
          else:

               returnset.update(get_coords(start_yx[0],after=start_yx[1],up_to=end_yx[1],line=self.textlist[start_yx[0]]))
          
          return {x[0:2] for x in returnset},returnset 

     def type (self,framelist=None,y_offset=0,skip=False):

          
          """For text extry"""

          def clear_selected():

               return 

               self.highlighted_coords, self.selected_coords = set(),set()

          
          go_on = True
          inserting = False
          highlighting = False
          select_from_xy = None
          select_to_xy = None
          backspace_starting = False
          #If true, then the loop repeats only once.
          #For entering a single note, called from the main program.
          changed = False

          
          lastkey = 0  #Previous key entered

          
          if not skip:

               while go_on:
                    if select_from_xy:
                         # if a selection has been initiated

                         temp_set = self.get_highlighted(select_from_xy,(self.cursor_y+self.top_line,self.cursor_x))
                         self.highlighted_coords = temp_set[0]
                         self.selected_coords = temp_set[1]
                         
                         
                    self.put_all()  # display the contents of the screen
                    key = self.window.getch()  # get a character 
                    
                    changed = True 

                    if key == curses.KEY_ENTER or key == 10 or key == 13:
                         # hard return
                         self.hard_return()
                         clear_selected()
                         
                    elif key in keys:
                         changed = False
                         if highlighting:
                              # if highlighting, then keep track of cursor position
                              self.highlighted_coords.add((self.cursor_y+self.top_line,self.cursor_x))
                              if self.cursor_y+self.top_line < len(self.textlist) and self.cursor_x < len(self.textlist[self.cursor_y+self.top_line]):
                                   self.selected_coords.add((self.cursor_y+self.top_line,self.cursor_x,self.textlist[self.cursor_y+self.top_line][self.cursor_x]))
                         

                         if self.cursor_x < self.width:
                              # moves the cursor horizontally
                              self.cursor_x += keys[key][1]
                              if self.cursor_x == self.width:
                                   self.cursor_x = 0
                                   if self.cursor_y < self.height-1:
                                        self.cursor_y += 1
                                        if self.cursor_y == self.height - 1:
                                             self.move_up()
                              if self.cursor_x < 0:
                                   self.move_left()

                         
                              
                         if self.cursor_y < self.height:
                              # moves the cursor vertically
                              self.cursor_y += keys[key][0]
                              if self.cursor_y == self.height:
                                   self.scroll_down()
                                   self.cursor_y = self.height-1

                              elif self.cursor_y < 0:
                                   self.cursor_y = 0
                                   self.scroll_up()

       
                                   
                              
                                   
                         else:
                              if key == curses.KEY_UP:
                                   self.move_up 
                              
                    elif key == 19:

                         highlighting = not highlighting
                         changed = False

                    elif key == 27:
                         # initiate selecting 
                         select_from_xy = (self.cursor_y+self.top_line,self.cursor_x)

                         
                    elif key == 29:
                         # conclude selecting
                         if select_from_xy:
                              select_to_xy = (self.cursor_y+self.top_line,self.cursor_x)
                              
                              if select_from_xy == select_to_xy:
                                   select_from_xy, select_to_xy = None,None
                                   

                              else:
                                   self.selected_coords.update(self.get_highlighted(select_from_xy,(self.cursor_y+self.top_line,self.cursor_x))[1])
                                   select_from_xy, select_to_xy = None,None
                    elif key == 1:
                         # to select all
                         select_from_xy = (0,0)
                         select_to_xy = (len(self.textlist)-1,len(self.textlist[len(self.textlist)-1])-1)
                    elif key == 3:
                         # to copy
                         if self.selected_coords:
                              self.text_buffer = self.collect_text()[0]
                         self.selected_coords = set()
                    elif key == 24:
                         # to cut
                         if self.selected_coords:
                              temp_col = self.collect_text(delete=True)
                              self.text_buffer,starting_at = temp_col[0], temp_col[1]
                         self.selected_coords = set()
                         self.reverse_cascade(line_from=starting_at,line_to=self.find_first_empty_line(line_from=starting_at))
                    elif key == 22:
                         # to paste
                         
                         if  '\n' not in self.text_buffer:
                              if self.cursor_y+self.top_line < len(self.textlist) and self.cursor_x < self.textlist[self.cursor_y+self.top_line]:
                                   self.textlist[self.cursor_y+self.top_line] = self.textlist[self.cursor_y+self.top_line][0:self.cursor_x] +\
                                                                                self.text_buffer +\
                                                                                self.textlist[self.cursor_y+self.top_line][self.cursor_x:]

                         elif self.cursor_y+self.top_line+1 < len(self.textlist):
                              self.buffer_lines = self.text_buffer.split('\n')
                              self.textlist[self.cursor_y+self.top_line] = self.textlist[self.cursor_y+self.top_line] + self.buffer_lines[0]
                              self.textlist[self.cursor_y+self.top_line+1] = self.buffer_lines[-1] + self.textlist[self.cursor_y+self.top_line+1]
                              if len(self.buffer_lines) > 2:
                                   self.textlist = self.textlist[0:self.cursor_y+self.top_line+1] + self.buffer_lines[1:-1] + self.textlist[self.cursor_y+self.top_line+1:]
                                    
                         self.cascade(self.cursor_y+self.top_line)
                         changed = True
                         

                    elif key == curses.KEY_INSERT:
                         inserting = not inserting
                         
                    elif key == 19: ## ctr a 
                         self.scroll_down()
                    elif key == 1: ##ctr s
                         self.scroll_up()
                    elif 30 <= key < 255:
                         # for an ordinary key entry 
                         self.put_char(str(chr(key)),insert=inserting)

                         self.move_right(str(chr(key)))
                         
                         if self.cursor_y + self.top_line < len(self.textlist) and len(self.textlist[self.top_line + self.cursor_y].rstrip()) > self.width:
                              self.cascade(self.top_line + self.cursor_y)
                         clear_selected()
                    elif key == curses.KEY_TAB:
                         for x in range(6):
                              self.put_char(' ',insert=True)

                              self.move_right(' ')
                              
                              if len(self.textlist[self.top_line + self.cursor_y].rstrip()) > self.width:
                                   self.cascade(self.top_line + self.cursor_y)
                              clear_selected()
                         
                    elif key in [curses.KEY_DELETE, curses.KEY_BACKSPACE]:
                         # to delete 
                         backspace_starting = True
                         if ((self.top_line + self.cursor_y) < len(self.textlist)
                             and len(self.textlist[self.top_line + self.cursor_y]) >= self.cursor_x):
                              if self.cursor_x > 0:
                                   self.textlist[self.top_line + self.cursor_y] = self.textlist[self.top_line + self.cursor_y][0:self.cursor_x-1] + \
                                                                                  self.textlist[self.top_line + self.cursor_y][self.cursor_x:]
                                   
                                   self.move_left()
                              elif self.cursor_y > 0:
                                  temp_cursor_x = min([len(self.textlist[self.top_line + self.cursor_y-1]),self.width])
                                  self.textlist[self.top_line + self.cursor_y-1] = self.textlist[self.top_line + self.cursor_y-1] + ' ' + \
                                                                                   self.textlist[self.top_line + self.cursor_y].lstrip().split(' ')[0]
                                  if len(self.textlist[self.top_line + self.cursor_y].lstrip().split(' ')) > 0:
                                       self.textlist[self.top_line + self.cursor_y] = ' '.join(self.textlist[self.top_line + self.cursor_y].lstrip().split(' ')[1:])
                                  else: 
                                       self.textlist = self.textlist[0:self.top_line + self.cursor_y] + self.textlist[self.top_line + self.cursor_y+1:] + [' ']
                              
                                  self.cursor_y -=1
                                  self.cursor_x = temp_cursor_x
                                                    
                         if len(self.textlist[self.top_line + self.cursor_y].replace('\n','')) == 0 and len(self.textlist) > self.top_line + self.cursor_y:
                              self.textlist = self.textlist[0:self.top_line+self.cursor_y] + self.textlist[self.top_line+self.cursor_y+1:]
                              self.textlist += [' ']
                                  

                         clear_selected()
                                   

                              
                    elif key == 493:

                         self.cursor_y = 0
                         self.top_line = 0
                         self.cursor_x = 0
                    elif key == 491:

                         self.cursor_y = self.height - 1
                         self.cursor_x = self.width - 1
                         self.top_line = len(self.textlist)-self.height

                    elif key == 21:

                         self.bufferobject_redo.add(self.copy_self())
                         self.change_self(self.bufferobject_undo.get())
                         changed = False
                         
                    elif key == 18:
                         self.bufferobject_undo.add(self.copy_self())
                         self.change_self(self.bufferobject_redo.get())

                    else:
                         changed = False

                    if key != curses.KEY_BACKSPACE and backspace_starting:
                         self.cascade()
                         self.reverse_cascade(self.top_line+self.cursor_y,line_to=self.find_first_empty_line(line_from=self.top_line+self.cursor_y))
                         backspace_starting = False
                         
                         
                    
                    if key == curses.KEY_F1:
                         go_on = False

                    if changed:
                         self.bufferobject_undo.add(self.copy_self())

                         

                    self.window.addstr(3,3,'   '+str(key)+'   ')

                    lastkey = key
               self.cascade()
               self.finalize()
               self.newtextlist = list(self.textlist)

          
          if framelist:
               
               self.newtextlist = self.put_in(1+y_offset,1,self.textlist[self.top_line:self.top_line+self.height-1],framelist) 
          return self.newtextlist,self.textlist
                    
 
class EmptyMovingWindow (MovingWindow):



     def __init__ (self,textlist=None,object_dict=None,y_dim=2000,x_dim=2000):

          if object_dict is None:
               self.object_dict = {}
          else:
               self.object_dict = copy.deepcopy(object_dict)
          if textlist is None:
               self.textlist = [' '*x_dim]*y_dim
          else:
               self.textlist = list(textlist)

          self.y_dim = y_dim
          self.x_dim = x_dim
          self.index = 0
          self.size = 5
          self.note_stack = Stack()
          self.added_notes = {0}
          self.cycling_through = None
          self.get_margins = True
          self.selected = set()
          self.cursor_y = 0
          self.cursor_x = 0
          self.drew_or_typed = False
          self.moving_dict = {}
          self.moving_qualities = {}
          self.help = None


     def populate (self,dict_object=None,totextlist=None):

          for ind_temp in dict_object:
               
               if not ind_temp.startswith('%'):
          
                    obj_list = dict_object[ind_temp]['o']
                    y,x = dict_object[ind_temp]['p'][0],dict_object[ind_temp]['p'][1]
                    self.put_in(y_start=y,x_start=x,fromtextlist=obj_list,totextlist=totextlist)

     def put_in (self,y_start,x_start,fromtextlist=None,totextlist=None,skip=[' ']):

          """ Placed one list within another list"""

          for y in range(len(fromtextlist)):
               newline = totextlist[y_start+y][0:x_start]
               for x in range(len(fromtextlist[0])):
                    if fromtextlist[y][x] not in skip:
                         newline+= fromtextlist[y][x]
                    else:
                         newline+=totextlist[y_start+y][x_start+x]
               newline += totextlist[y_start+y][x_start+x+1:]
               totextlist[y_start+y] = newline
                    
          return totextlist
     
     def transform_dictionary (self,dictionaryobject=None,fromprefix='$',toprefix='$$'):

          """Changes the prefix before a key in dictionary"""

          if dictionaryobject is None:
               dictionaryobject = self.object_dict
          for oldkey in list(dictionaryobject):
               if oldkey.startswith(fromprefix) and oldkey.count(fromprefix)==1:
                    newkey = oldkey.replace(fromprefix,toprefix)
                    dictionaryobject[newkey] = copy.deepcopy(dictionaryobject[oldkey])
                    del dictionaryobject[oldkey] 
    

     def extract (self,textlistobject=None,y_pos=0,x_pos=0,y_dim=0,x_dim=0):

          """ to extract a rectangular segment from the textlist"""

          if textlistobject is None:
               textlistobject = self.textlist

          returnlist = []

          for y in range(y_pos,y_pos+y_dim):

               line = textlistobject[y][x_pos:x_pos+x_dim]
               returnlist.append(line)
          return returnlist 
     
     def make_rectangle (self,height,width,blank=False,divider=0,BOX_CHAR=None):

          """Creates a block character rectangle of the given dimension"""
          if BOX_CHAR  is None:
               BOX_CHAR = BOX_CHAR_NORMAL
          
          textlist = []
          if not blank:
               for y in range(0,height):

                    if y == 0:
                         textlist.append(BOX_CHAR['lu']+BOX_CHAR['h']*(width-2)+BOX_CHAR['ru'])
                    elif y == divider:
                         textlist.append(BOX_CHAR['lm']+BOX_CHAR['h']*(width-2)+BOX_CHAR['rm'])
                    elif 0 < y < height-1:
                         textlist.append(BOX_CHAR['v']+' '*(width-2)+BOX_CHAR['v'])
                    else:
                         textlist.append(BOX_CHAR['ll'] + BOX_CHAR['h']*(width-2) + BOX_CHAR['rl'])
          else:
               textlist = [' '*width]*height
                    
          return textlist

     def show_temporary (self,showlist=None,y_pos=None,x_pos=None):

          """For temporary displaying help instructions """

          showlist = fill(showlist)
          
          y_dim = len(showlist)+2
          x_dim = len(showlist[0])+2

          frame = self.make_rectangle(height=y_dim,width=x_dim,divider=0,BOX_CHAR=BOX_CHAR_DOUBLE)
          showlist = self.put_in(y_start=1,x_start=1,fromtextlist=showlist,totextlist=frame)
          
          
          
          if y_pos is None or x_pos is None:

               if self.cursor_y <= int(curses.LINES/2):
                    if y_dim <= int(curses.LINES/2):
                         y_pos = int((curses.LINES/2-y_dim)/2)+int(curses.LINES/2)-5
                    else:
                         y_pos = int((curses.LINES-y_dim)/2)
               else:
                    if y_dim <= int(curses.LINES/2):
                         y_pos = int((curses.LINES/2-y_dim)/2)
                    else:
                         y_pos = int((curses.LINES-y_dim)/2)
               if self.cursor_x <= int(curses.COLS/2):
                    if x_dim <= int(curses.COLS/2):
                         x_pos = int((curses.COLS/2-x_dim)/2)+int(curses.COLS/2)
                    else:
                         x_pos =int((curses.COLS-x_dim)/2)
               else:
                    if x_dim <= int(curses.COLS/2):
                         x_pos = int((curses.COLS/2-x_dim)/2)
                    else:
                         x_pos =int((curses.COLS-x_dim)/2)

          background = self.extract(y_pos=y_pos,x_pos=x_pos,y_dim=y_dim,x_dim=x_dim)

          while True:

               for l  in (showlist,background):
               
                    for y in range(y_dim):
                         
                         self.textlist[y_pos+y] = self.textlist[y_pos+y][0:x_pos]\
                                                  + l[y]\
                                                  + self.textlist[y_pos+y][x_pos+x_dim:]
                    yield l==background

          
          
                         
                    
               

          

     def new_note (self,y_coord,x_coord,height=30,width=30,totextlist=None,blank=False,divider=0,BOX_CHAR=None):

          """Creates a frame for a new note """

          
          skip = [' ']
          if blank:
               skip = []
          
               
          if totextlist is None:
               totextlist = self.textlist
          frame = self.make_rectangle(height,width,blank=blank,divider=divider,BOX_CHAR=BOX_CHAR)
          self.put_in(y_coord,x_coord,fromtextlist=frame,totextlist=totextlist,skip=skip)
          return frame 


     def extend (self,top_ex=0,bottom_ex=0,left_ex=0,right_ex=0):

          """Enlarges the textlist"""

          for y in range(len(self.textlist)):
               self.textlist[y] = left_ex*' ' + self.textlist[y] + right_ex *' '
          if self.textlist:
               x_total = len(self.textlist[0])
               self.textlist = [' '*x_total]*top_ex + self.textlist + [' '*x_total]*bottom_ex
          else:
               return 0,0

          if top_ex != 0 and left_ex != 0:
               # to move objects if top row or left column added 

               for obj in self.object_dict:

                    if 'p' in self.object_dict[obj]:

                         positions = self.object_dict[obj]['p']
                         up_bound = positions[0]
                         left_bound = positions[1]
                         down_bound = positions[2]
                         right_bound = positions[3]
                         up_bound += top_ex
                         down_bound += top_ex
                         left_bound += left_ex
                         right_bound += left_ex
                         self.object_dict[obj]['p'] = (up_bound,left_bound,down_bound,right_bound)
                            
          return len(self.textlist),x_total


     def trim (self,top_tr=0,bottom_tr=0,left_tr=0,right_tr=0):

          """ Eliminates empty rows and columns"""

          def establish_margins():

               top_margin = 0
               bottom_margin = 0
               left_margin = 0
               right_margin = 0
               top_found = False
               bottom_found = False
               left_found = False
               right_found = False


               for top_margin, y in enumerate(self.textlist):
                    if y.count(' ') != len(y):
                         break

               for bottom_margin, y in enumerate(reversed(self.textlist)):
                    if y.count(' ') != len(y):
                         break

               left_margins = []
               right_margins = []

               for line in self.textlist[top_margin:len(self.textlist) - bottom_margin]:
                         for left_margin, x in enumerate(line):
                              if x != ' ':
                                   left_margins.append(left_margin)
                         for right_margin, x in enumerate(reversed(line)):
                              if x != ' ':
                                   right_margins.append(right_margin)

               if left_margins and right_margins:
               
                    left_margin = min(left_margins)
                    right_margin = max(right_margins)
               else:
                    left_margin = len(self.textlist[0])
                    right_margin = len(self.textlist[0])
               

               return top_margin,left_margin,bottom_margin,right_margin
               
          if self.get_margins:              
               self.top_margin,self.left_margin,self.bottom_margin,self.right_margin = establish_margins()
               self.get_margins = False 
          
          if top_tr != -1:
               top_tr = min ([top_tr,self.top_margin])
          else:
               top_tr = self.top_margin
          if bottom_tr != -1:
               bottom_tr = min ([bottom_tr,self.bottom_margin])
          else:
               bottom_tr = self.bottom_margin
          if left_tr != -1:
               left_tr = min ([left_tr,self.left_margin])
          else:
               left_tr = self.left_margin
          if right_tr != -1:
               right_tr = min ([right_tr,self.right_margin])
          else:
               right_tr = self.right_margin 

          self.textlist = self.textlist[top_tr:len(self.textlist)-bottom_tr]
          self.textlist = [line[left_tr:len(line)-right_tr] for line in self.textlist]
          self.get_margins = True



          for obj in self.object_dict:

               if 'p' in self.object_dict[obj]:

                    positions = self.object_dict[obj]['p']
                    up_bound = positions[0]
                    left_bound = positions[1]
                    down_bound = positions[2]
                    right_bound = positions[3]
                    up_bound -= top_tr
                    down_bound -= top_tr
                    left_bound -= left_tr
                    right_bound -= left_tr
                    self.object_dict[obj]['p'] = (up_bound,left_bound,down_bound,right_bound)          
          if self.textlist:
               
               return len(self.textlist[0]),len(self.textlist)
          else:
               return 0,0
          
        
          
     def dimensions (self,textlist):

          """Find dimensions of textlist"""

          x = max([len(l) for l in textlist])
          
          textlist = [l + (x-len(l))*' ' for l in textlist]
          y = len(textlist)
          return textlist,y,x


     def find_object_in (self,y_pos,x_pos):

          """Find if the coordinates are inside an object, and return the object"""

          
          for obj in self.object_dict:

               if 'p' in self.object_dict[obj]:

                    positions = self.object_dict[obj]['p']
                    up_bound = positions[0]
                    left_bound = positions[1]
                    down_bound = positions[2]
                    right_bound = positions[3]
                    if up_bound <= y_pos <= down_bound and \
                       left_bound <= x_pos <= right_bound:
                         return obj
               elif 'c' in self.object_dict[obj]:

                    if self.object_dict[obj]['c'].contains(y_pos,x_pos):
                         return obj

               


                    
          return ''
     

                    
     def is_clear (self,y_pos,x_pos,y_dim,x_dim,thorough=True):

          """Test to see a new object overlaps with existing objects"""
          # y_dim = dimension of object

          yrange = range(0,y_dim+1)
          xrange_inner = list(range(1,x_dim))
          xrange_outer = [0,x_dim]
          xrange = xrange_inner + xrange_outer 

          if y_pos <=1 or x_pos <=1:
               return False

          if y_pos+y_dim >= self.y_dim or x_pos+x_dim >= self.x_dim:
               
               return False
          
          for y in yrange:
               if thorough or y in [0,y_dim]:
                    for x in xrange:
                         if self.textlist[y_pos+y][x_pos+x] != ' ':
                              return False
               else:
                    for x in xrange_outer:
                         if self.textlist[y_pos+y][x_pos+x] != ' ':
                              return False
                         
          else:
               return True

     def is_clear_drawn (self,coords,auto=False):

          """tests to see if there is space open for a drawn object"""
          
          copy_coords = list(coords)
          if auto:
               coords = set()
               for c_temp in copy_coords:

                    for y,x in ((-1,0),(1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1),(0,0)):
                         coords.add((c_temp[0]+y,c_temp[1]+x))
               
          for c_temp in coords:
               

               if self.textlist[c_temp[0]][c_temp[1]] != ' ' \
                  or c_temp[0]<=0 or c_temp[0]>=self.y_dim \
                  or c_temp[1]<=0 or c_temp[1]>=self.x_dim:
                    return False
          return True
     


               

     def find_clear (self,height,width,start_y=0,start_x=0,from_corner=True):

          """ Finds a clear space to locate an object. Some issues with it"""

          def square_generator(increment=50,start_y=0,start_x=0):

               for y in range(int(start_y/increment),int(self.y_dim/increment)):
                    for x in range(int(start_y/increment),int(self.x_dim/increment)):
                         yield y*increment,x*increment

          def centripetal_generator(increment=5,start_y=0,start_x=0):

               def hypot (x,y):

                    return int(sqrt(x*x+y*y))

               a = hypot(start_y-0,start_x-0)
               b = hypot(start_y-0,self.x_dim-start_x)
               c = hypot(self.y_dim-start_y,start_x-0)
               d = hypot(self.y_dim-start_y,self.x_dim-start_x)
               longest = max([a,b,c,d])

               for rad in range(0, int(longest/increment)):
                    side = int(sqrt((rad*rad)/2))
                    up_left = start_y - side, start_x - side
                    up_right = start_y - side, start_x + side
                    down_left = start_y + side, start_x - side
                    down_right = start_y + side, start_x + side

                    for inc in range(0,int(side*2/increment)):
                         yield up_left[0],up_left[1]+inc
                         yield up_right[0]+inc,up_right[1]
                         yield down_right[0],down_right[1]-inc
                         yield down_left[0]-inc,down_left[1]
                    
          if from_corner:
               diagn = []
               for y,x in square_generator(50,start_y=start_y,start_x=start_x):
                    diagn.append((y,x))
                    if self.is_clear(y_pos=y,x_pos=x,y_dim=height,x_dim=width):
                         return y,x
               return False,False

          else:
               diagn = []
               for y,x in centripetal_generator(5,start_y=start_y,start_x=start_x):
                    diagn.append((y,x))
                    if self.is_clear(y_pos=y,x_pos=x,y_dim=height,x_dim=width):
                         
                         return y,x
               return False,False


     def add_from_stack (self,y_st=0,x_st=0,y_pos=None,x_pos=None):

          """ Add a note into the pad from a stack of objects"""

 

          if not self.note_stack.exists():

               return False
          popped = self.note_stack.pop()
          if isinstance(popped,(list,tuple)):
               popped = tuple(popped) + (None,None,None)

               index,note1,note2,keywords = popped[0],popped[1],popped[2],popped[3]

          else:
               self.add_drawn_object(popped,y_pos=y_pos,x_pos=x_pos)
               return True 

          
          note1, height, width = self.dimensions(note1)


          if not  (y_pos and x_pos) or not self.is_clear(y_pos,x_pos,height,width):
               
               y_pos,x_pos = self.find_clear(height,width,y_st,x_st)

          if isinstance(y_pos,int):
               if not note2:
                    

                    self.add_object(index,new_object_list=note1,y_pos=y_pos,x_pos=x_pos,l_prop=keywords)
               else:
                    self.add_object(index,new_object_list=note1,new_object_list2=note2,y_pos=y_pos,x_pos=x_pos,l_prop=keywords)

          else:
               self.import_note(popped[0:3])
          
                    
     def show_notes (self):

          """Show all the notes in the pad"""
          
          returnlist = []
          for n in self.object_dict:

               if 'p' in self.object_dict[n]:
                    coords = self.object_dict[n]['p']
                    returnlist.append(str(n)+' = '
                                      + str(coords[0]) + '/' 
                                      + str(coords[1]) + '/' 
                                      + str(coords[2]) + '/' 
                                      + str(coords[3]))
          return '\n'.join(returnlist)

     def move_object (self,indexes=None,vert_inc=0,hor_inc=0,auto=False,mode='n'):

          """To move an object.  Accepts a list of indexes for objects
          mode = o for overwrite
          """
          
          if isinstance(indexes,str):
               indexes = [indexes]

          for index in indexes:

               if index in self.object_dict and 'p' in self.object_dict[index]:
                    
                    positions = list(self.object_dict[index]['p'])
                    up_bound = positions[0]
                    left_bound = positions[1]
                    down_bound = positions[2]
                    right_bound = positions[3]

                    old_up_bound = up_bound
                    old_left_bound = left_bound
                    height = down_bound - up_bound
                    width = right_bound - left_bound
                    up_bound += vert_inc
                    down_bound += vert_inc
                    left_bound += hor_inc
                    right_bound += hor_inc

                    obj = self.object_dict[index] # eliminated deepcopy

                    self.delete_object(index)
                    if mode == 'o' or self.is_clear(up_bound-(1*auto),left_bound-(1*auto),height+(2*auto),width+(2*auto),thorough=True):
                         
                         
                         self.add_object (index,new_object_list=obj['o'],
                                          new_object_list2=obj['oo'],
                                          l_prop=obj['l'],
                                          x_prop=obj['x'],
                                          y_pos=up_bound,
                                          x_pos=left_bound)
                    else:
                         self.add_object (index,new_object_list=obj['o'],
                                          new_object_list2=obj['oo'],
                                          l_prop=obj['l'],
                                          x_prop=obj['x'],
                                          y_pos=old_up_bound,
                                          x_pos=old_left_bound)

               elif index in self.object_dict and 'c' in self.object_dict[index]:

                    self.delete_drawn_object(index)
                    self.object_dict[index]['c'].move(vert_inc,hor_inc)
                    
                    if mode == 'o' or self.is_clear_drawn([(x[0][0],x[0][1]) for x in self.object_dict[index]['c'].get_coords()],auto=True):
                         self.add_drawn_object(index,mode='o')
                                                     
                    else:
                         self.object_dict[index]['c'].move(-vert_inc,-hor_inc)
                         self.add_drawn_object(index,mode='o')
                        
                         
                    
     def atomize (self,index=''):

          """identify separate objets"""
          

          if index in self.object_dict:
               self.delete_drawn_object(index)
               if 'c' in self.object_dict[index]:
                    coords = self.object_dict[index]['c'].get_coords()
                    coord_dict = {}
                    for c in coords:
                         coord_dict[c[0]] = (c[1][0],c[1][1])
                    loopfinder = LoopFinder(elements=set(coord_dict.keys()))
                    partial_objects = loopfinder.find_all_loops()
                    del self.object_dict[index]     
                    
                    for p_o in partial_objects.keys():
                         partial_obj_coords = {x:coord_dict[x] for x in partial_objects[p_o]}
                         new_object, obj_ind = self.assign_drawing_object()
                         new_object.drawn_object = partial_obj_coords
                         time.sleep(1)
                         self.add_drawn_object(obj_ind)
                         
     def fill_space (self,y_pos,x_pos,blankchar=' ',tochar='X'):

          """fills up an empty space"""

          def get_adjacent (y_pos,x_pos):

               returnlist = []
               for x in (-1,0,1):
                    for y in (-1,0,1):
                         if abs(x)+abs(y) != 0:
                              returnlist.append((y_pos+y,x_pos+x))
               return returnlist
                              
                         
          seed_set =  {(y_pos,x_pos)}
          done_set = set()
          counter = 0
          
          while True:
               counter += 1
               done_set_copy = set(done_set)
               for c in list(seed_set):
                    counter += 1
                    if c not in done_set:
                         if self.textlist[c[0]][c[1]] == blankchar:
                              self.textlist[c[0]] = self.textlist[c[0]][0:c[1]]+tochar+self.textlist[c[0]][c[1]+1:]
                              done_set.add(c)
                         seed_set.update([c for c in get_adjacent(c[0],c[1]) if self.textlist[c[0]][c[1]] == blankchar])
               if not len(done_set) > len(done_set_copy) or counter > 40000:
                    break
          
               

     def add_drawn_object(self,index='',mode='n',delete=False,y_pos=None,x_pos=None,schema=None):

          """ add in a drawn object
          mode = n for normal, =o for overwrite
          delete = true to delete the coordinates"""

          
##          if not index.startswith('%'):
##               return False
          print('index='+index)
          if index in self.object_dict:

               if 'c' in self.object_dict[index]:

                    if y_pos and x_pos:
                         self.object_dict[index]['c'].position_object(y_pos,x_pos)

                    coords = self.object_dict[index]['c'].get_coords()

                    for c_temp in coords:

                         y_pos = c_temp[0][0]
                         x_pos = c_temp[0][1]

                         if delete:
                              new_char = c_temp[1][0]
                         else:
                              new_char = c_temp[1][1]

                         self.textlist[y_pos] = self.textlist[y_pos][0:x_pos] + new_char + self.textlist[y_pos][x_pos+1:]
                         
               return True
          return False

                       
     def delete_drawn_object(self,index=''):

          """deletes a drawn object"""
          
          self.add_drawn_object(index,delete=True)


     def delete_object(self,index='',for_show=False):

          """To delete an object"""
          
          if index in self.object_dict and 'p' in self.object_dict[index]:
               positions = self.object_dict[index]['p']
               up_bound = positions[0]
               left_bound = positions[1]
               down_bound = positions[2]
               right_bound = positions[3]
               objecttext = []

               if 'r' not in self.object_dict[index]:
                    # if there is information for the overwritten coordinates 
                    for y in range(up_bound,down_bound):
                         objecttext.append(self.textlist[y][left_bound:right_bound+1])
                         self.textlist[y] = self.textlist[y][0:left_bound] + ' '*(right_bound-left_bound) + self.textlist[y][right_bound:]
               else:
                    for y in range(up_bound,down_bound):
                         objecttext.append(self.textlist[y][left_bound:right_bound+1])
                         self.textlist[y] = self.textlist[y][0:left_bound] + self.object_dict[index]['r'][y-up_bound][0:right_bound-left_bound] + self.textlist[y][right_bound:]
 
                    

               if not for_show:

                    # deletes object from note_dict
                    
                    del self.object_dict[index]
                    self.import_note(index,objecttext)
                    self.cycling_through = cycle(self.object_dict.keys())
                    
               self.get_margins = True

                    
               

     def add_object(self,index='',
                    new_object_list=None, #the displayed text of note
                    new_object_list2=None, #full text of note
                    l_prop=None,           # keyset
                    x_prop=None,
                    
                    y_pos=0,
                    x_pos=0,
                    use_second=False,
                    for_show=False):

          """To add an object into the pad"""


               
          
          index = str(index)
          if l_prop is None:
               l_prop = set()

          if not for_show:
               new_object_list, height,width = self.dimensions(new_object_list)

          else:
               height = self.object_dict[index]['p'][3]-self.object_dict[index]['p'][1]
               width = self.object_dict[index]['p'][2]-self.object_dict[index]['p'][0]

##          if not for_show and not self.is_clear(y_pos,x_pos,height,width):
##               
##               return False

          if index not in self.object_dict or for_show:

               remnant_list = self.extract(y_pos=y_pos,x_pos=x_pos,y_dim=height,x_dim=width)

               if for_show and index in self.object_dict:

                    new_object_list = self.object_dict[index]['o']
                    new_object_list2 = self.object_dict[index]['oo']
                    y_pos, x_pos = self.object_dict[index]['p'][0], self.object_dict[index]['p'][1]
                    new_object_list, height,width = self.dimensions(new_object_list)
                    
                    
                    

               for y in range(height):

                    # enters new object into textlist

                    if new_object_list2 and use_second:
                         self.textlist[y_pos+y] = self.textlist[y_pos+y][0:x_pos]\
                                                  + new_object_list2[y]\
                                                  + self.textlist[y_pos+y][x_pos+width:]
                    
                    else:
                         self.textlist[y_pos+y] = self.textlist[y_pos+y][0:x_pos]\
                                                  + new_object_list[y]\
                                                  + self.textlist[y_pos+y][x_pos+width:]

                         


               if not for_show:
                    # adds back to note 
                    self.object_dict[index] = {'o':new_object_list,
                                               'oo':new_object_list2,
                                               'p':(y_pos,x_pos,y_pos+height,x_pos+width),
                                               'l':l_prop,
                                               'x':x_prop,
                                               'r':remnant_list}
                    self.cycling_through = cycle(self.object_dict.keys())
                    self.get_margins = True 
               
          else:
               return False
          

     def import_note (self,index,show_note=None,full_note=None,keyset=None):

          """To import a note into the stack."""

          if not index.startswith('%'):
          
               self.note_stack.add((str(index),show_note,full_note,keyset))
          else:
               self.note_stack.add((str(index)))

     def empty_stack (self):
          self.note_stack = Stack()

          
     def display (self,y_pos=0,x_pos=0):

          """ displays a note in the stack"""
          
          if not self.note_state.exists():
               return False
          popped = self.note_stack.pop()
          if popped:
               index, note = popped[0],popped[1]
          note, height, width = self.dimensions(note)
          if not self.is_clear(y_pos,x_pos,height,width):
               return False
          self.add_object(index,note,y_pos,x_pos)

     def objects_in_stack (self):

          """Returns objects in the stack"""
          
          return self.note_stack.size()


     def assign_drawing_object (self,y_pos=0,x_pos=0,schema=None):

          """used to assign a new drawn object to an index in the object dictionary """

          assigned_obj = ''
          for obj in self.object_dict:

               if obj.startswith('%'):

                    if self.object_dict[obj]['c'].contains(y_pos,x_pos):
                         assigned_obj = obj
                         
                         break
                    
          if not assigned_obj:
               try:
                    assigned_obj = '%'+str(max([int(x[1:]) for x in self.object_dict if x.startswith('%')])+1)
               except:
                    assigned_obj = '%1'
                         # to increment by one the last drawn_object added to object_dict
               self.object_dict[assigned_obj] = {}
               self.object_dict[assigned_obj]['c'] = DrawingObject(textlistobject = self.textlist,schema=schema)
          self.cycling_through = cycle(self.object_dict.keys())
          return self.object_dict[assigned_obj]['c'], assigned_obj
          
               
        
          
     def moving_screen (self,screen,y_coord=0,x_coord=0,b_margin=4,t_margin=3,l_margin=1,r_margin=1,entering=False,override=True):

          """Main loop"""


          def put(y_pos,x_pos):

               if x_pos + x_max > x_total:

                    x_pos = x_total - x_max

               if y_pos + y_max > y_total:
                    y_pos = x_total - y_max

               if x_pos < 0:
                    x_pos = 0
               if y_pos < 0:
                    y_pos = 0
               

               for y in range(y_max-1-b_margin-t_margin):

                    for x in range(x_max-l_margin-r_margin):

                         if y_pos+y <= y_total:
                              try:
                                   if x == self.cursor_x and y == self.cursor_y:
                                        screen.addstr(y+b_margin,l_margin+x,self.textlist[y_pos+y][x_pos+x],curses.A_REVERSE)
                                   else:
                                        screen.addstr(y+b_margin,l_margin+x,self.textlist[y_pos+y][x_pos+x],curses.A_NORMAL)
                              except:
                                   pass
                         

               
                    
               screen.refresh()

          def cursor_show (y_pos,x_pos,activate=True):

               if activate:
                    screen.addstr(y_pos+b_margin,x_pos+l_margin,'X',curses.A_REVERSE)
               if not activate:
                    screen.addstr(y_pos+b_margin,x_pos+l_margin,' ',curses.A_NORMAL)
               screen.refresh()


               
          def dimensions ():



               x_dim = max([len(l) for l in self.textlist])
               
               self.textlist = [l + (x_dim-len(l))*' ' for l in self.textlist]
               x_dim = max([len(l) for l in self.textlist])
               x_dim_min = min([len(l) for l in self.textlist])
               y_dim = len(self.textlist)
               return x_dim, y_dim



          if not self.textlist:
               return False

          x_total,y_total = dimensions()
          multiplier = 1


          y_inc,x_inc = 0,0

          go_on = True

                         
          x_max = curses.COLS
          y_max = curses.LINES

          int(x_max/2)
          stack_dump = False
          moving_object = False
          objects_to_move = set()
          moving_screen_too = False
          extending = False
          contracting = False
          selecting = False
          cursor_move = True
          once_through = False
          cycling = False
          self.cursor_y = int(y_max/2)
          self.cursor_x = int(x_max/2)
          drawing = False
          last_key = curses.KEY_RIGHT
          typing = False
          started_typing = False
          started_drawing = False
          started_selecting = False
          left_margin = 0
          self.copy_buffer = None
          starting_coord = (0,0)
          self.copy_buffer = None
          drawing_key = next(drawing_keys)
          drawing_char = next(drawing_chars[drawing_key])
          conway = None
          self.cursor_moved = False
          self.linetypes = cycle(['normal','round','thick','double'])
          linetype = 'normal'
          self.BOX_CHAR = BOX_CHAR





##
##               
##
##
##          try:
          while go_on and not once_through:
               if conway:
                     conway.generate()


               if self.cursor_x < 0 or self.cursor_x > x_max:
                    self.cursor_x = int(x_max/2)
                    self.cursor_moved = True 
               if self.cursor_x < 0 or self.cursor_y > y_max:
                    self.cursor_y = int(y_max/2)
                    self.cursor_moved = True 
               
               self.print_to(screen,self.find_object_in(y_coord+self.cursor_y,x_coord+self.cursor_x),length=10,y_pos=1,x_pos=25)
               self.print_to(screen,' '.join(list(sorted(self.object_dict))),length=35,y_pos=1,x_pos=70)
               self.print_to(screen,', '.join(objects_to_move),length=30,y_pos=1,x_pos=36)
               self.print_to(screen,str(len(self.object_dict.keys()))+'/'+str(self.objects_in_stack()),length=21,y_pos=1,x_pos=3)
               self.print_to(screen,'█'*(not not (self.find_object_in(y_coord+2,x_coord+2)) and (self.find_object_in(y_coord+2,x_coord+2) in self.selected)),length=1,y_pos=1,x_pos=1)
               self.print_to(screen,linetype+' SHIFT+F12 for HELP '+'['+drawing_char+'] '
                             +'CYCLING'*cycling
                             +' MOVING OBJECTS'*moving_object
                             +' DRAWING'*drawing
                             +' TYPING'*typing
                             +' MOVING SCREEN'*moving_screen_too
                             +' SELECTING'*selecting
                             +' EXTENDING'*extending+' '
                             +' CONTRACTING'*contracting
                             +' COPYBUFFER '*(not self.copy_buffer == None)
                             +' PRESS = to SELECT  '*((y_coord+self.cursor_y,x_coord+self.cursor_x) == starting_coord)
                             +' CURSOR'*cursor_move+' SPEED='+str(multiplier),
                             length=90,y_pos=y_max-3,x_pos=1)
               
               
               if started_drawing and not drawing:
                    started_drawing = False
                         
               if started_selecting and not selecting:
                    started_selecting = False
               if stack_dump:
                    if self.note_stack.exists():
                         self.add_from_stack(y_coord,x_coord)
                         curses.beep()
                    else:
                         stack_dump = False
                    
               else:
                    if not entering:
                         key = screen.getch()
                    else:
                         key = ''
                         

                    def superimpose (a,b):

                         def super_lines (c,d):

                              return (c[0] or d[0],c[1] or d[1],c[2] or d[2])

                         return (super_lines(a[0],b[0]),super_lines(a[1],b[1]),super_lines(a[2],b[2]))

                    if typing:
                         if not started_typing and 30 < key < 265:
                              started_typing = True
                              left_margin = self.cursor_x
                              typing_object, type_obj_ind = self.assign_drawing_object(y_coord,x_coord)

                         if started_typing and (key == curses.KEY_ENTER or key==10 or key==13):

                              self.cursor_x = left_margin
                              self.cursor_y += 1

                         elif key == curses.KEY_DELETE:

                              typing_object.add(y_pos=y_coord+self.cursor_y,x_pos=x_coord+self.cursor_x,newchar=' ')
                              self.textlist[y_coord+self.cursor_y] = self.textlist[y_coord+self.cursor_y][0:x_coord+self.cursor_x]\
                                                                +' '+self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x+1:]
                              self.cursor_x += 1
                         elif key == curses.KEY_BACKSPACE:

                              if self.cursor_x > left_margin:
                                   typing_object.add(y_pos=y_coord+self.cursor_y,x_pos=x_coord+self.cursor_x,newchar=' ')
                                   self.textlist[y_coord+self.cursor_y] = self.textlist[y_coord+self.cursor_y][0:x_coord+self.cursor_x]\
                                                                +' '+self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x+1:]
                                   self.cursor_x -= 1
                                   
                                   
                              
                              
                         elif key not in keys and started_typing and 30 < key <265:


                              char_on = self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x]
                                                            
                              while char_on != ' ' and self.cursor_x <= x_max:
                                   self.cursor_x += 1

                              if char_on == ' ':
                                   char_on = chr(key)
                                   typing_object.add(y_pos=y_coord+self.cursor_y,x_pos=x_coord+self.cursor_x,newchar=char_on)

                                   self.textlist[y_coord+self.cursor_y] = self.textlist[y_coord+self.cursor_y][0:x_coord+self.cursor_x]\
                                                                +char_on+self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x+1:]
                                   self.drew_or_typed = True
                              self.cursor_x += 1
                              
                         elif key in keys:
                              y_inc,x_inc = keys[key][0],keys[key][1]
                              self.cursor_y += y_inc
                              self.cursor_x += x_inc
                 
                    if not typing and (key in keys or key in [ord('#'),ord('%'),ord('*'),ord('.'),ord('>'),ord(','),ord('<'),287,339,338,358,262,ord('|'),ord('_'),ord('+'),ord('='),curses.KEY_BACKSPACE,curses.KEY_TAB]):

                         if selecting and not drawing:
                              if not started_selecting:

                                   frame_x_dim = 10
                                   frame_y_dim = 10
                                   drawing_frame, obj_ind = self.assign_drawing_object(y_coord+self.cursor_y,x_coord+self.cursor_x)
                                   started_selecting = True

                                   

                              self.delete_drawn_object(obj_ind) #to delete selection frame
                              
                              temp_frame = self.make_rectangle(frame_y_dim,
                                                               frame_x_dim,
                                                               divider=-1,BOX_CHAR=self.BOX_CHAR_DOUBLE)
                              drawing_frame.enter_superimposed_object(y_coord=y_coord+self.cursor_y,
                                                                      x_coord=x_coord+self.cursor_x,
                                                                      objectlist=temp_frame)
                              if key == curses.KEY_RIGHT:
                                   frame_x_dim += 1
                              elif key == curses.KEY_LEFT:
                                   frame_x_dim -= 1
                              elif key == curses.KEY_UP:
                                   frame_y_dim -= 1
                              elif key == curses.KEY_DOWN:
                                   frame_y_dim += 1
                              elif key == ord('<'):
                                   selecting = False
                              elif key == ord('>'): #to select object 
                                   selecting = False
                                   drawing_frame.select()
                                   self.copy_buffer = DrawingObject(textlistobject=self.textlist,schema=self.object_dict[obj_ind]['c'].get_schema())
                                   del self.object_dict[obj_ind]
                                   
                                   
                              if selecting:
                                   self.add_drawn_object(obj_ind) #to redraw selection frame
                              
                              
                              
                              
                          
                         elif drawing:

                              

                              if key == ord('.') and started_drawing:
                                   self.delete_drawn_object(draw_obj_ind)
                                   drawing_object.stretch(x_pos=x_coord+self.cursor_x)
                                   self.cursor_x += 1
                                   self.add_drawn_object(draw_obj_ind)
                              elif key == ord('%'):
                                   conway = Conway(textlistobject=self.textlist,
                                                                  y_min=max([0,self.cursor_y-100]),
                                                                  y_max=min([self.cursor_y+100,y_total]),
                                                                  x_min=max([0,self.cursor_x-140]),
                                                                  x_max=min([self.cursor_x+140,x_total]))
                              
                              elif key == curses.KEY_TAB and started_drawing:
                                   drawing_char = next(drawing_chars[drawing_key])
                              elif key == 287 and started_drawing:
                                   drawing_key = next(drawing_keys)
                                   drawing_char = next(drawing_chars[drawing_key])
                              elif key == ord('*'):
                                   self.fill_space(y_pos=y_coord+self.cursor_y,x_pos=x_coord+self.cursor_x,
                                                   blankchar=self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x],
                                                   tochar=drawing_char)
                                   
                              elif key == curses.KEY_BACKSPACE and started_drawing:
                                   for x in range(5):
                                        drawing_char = next(drawing_chars)
                              elif key == ord('>') and started_drawing:
                                   self.delete_drawn_object(draw_obj_ind)
                                   drawing_object.stretch(y_pos=y_coord+self.cursor_y)
                                   self.cursor_y += 1
                                   self.add_drawn_object(draw_obj_ind)
                              elif key == ord(',') and started_drawing:
                                   self.delete_drawn_object(draw_obj_ind)
                                   drawing_object.stretch(x_pos=x_coord+self.cursor_x,contracting=True)
                                   self.cursor_x -= 1
                                   self.add_drawn_object(draw_obj_ind)
                              elif key == ord('<') and started_drawing:
                                   self.delete_drawn_object(draw_obj_ind)
                                   drawing_object.stretch(y_pos=y_coord+self.cursor_y,contracting=True)
                                   self.cursor_y -= 1
                                   self.add_drawn_object(draw_obj_ind)
                              elif key == 339: # fn up
                                   self.cursor_y -= 1
                              elif key == 338: # fn down
                                   self.cursor_y += 1
                              elif key == 358: #fn right 
                                   self.cursor_x += 1
                              elif key == 262: #fn left 
                                   self.cursor_x -= 1
                              elif key == ord('|') and started_drawing:
                                   self.delete_drawn_object(draw_obj_ind)
                                   drawing_object.flip(vertical=True)
                                   self.add_drawn_object(draw_obj_ind)
                              elif key == ord('_') and started_drawing:
                                   self.delete_drawn_object(draw_obj_ind)
                                   drawing_object.flip(horizontal=True)
                                   self.add_drawn_object(draw_obj_ind)
                              elif key == ord('+') and started_drawing:
                                   self.delete_drawn_object(draw_obj_ind)
                                   drawing_object.rotate()
                                   self.add_drawn_object(draw_obj_ind)
                              elif key == ord('=') and started_drawing and not started_selecting:
                                   self.atomize(draw_obj_ind)
##                                   self.add_drawn_object(draw_obj_ind)
                              elif key == ord('=') and started_drawing and started_selecting:
                                   if (y_coord+self.cursor_y,x_coord+self.cursor_x) == starting_coord:
                                        self.delete_drawn_object(draw_obj_ind)
                                        drawing_object.select(square=False)
                                        
                                        self.copy_buffer = DrawingObject(textlistobject=self.textlist,schema=self.object_dict[draw_obj_ind]['c'].get_schema())
                                        
                                        del self.object_dict[draw_obj_ind]
                                        drawing = False
                                        selecting = False
                                        
                                     
                              else:
                                   if selecting and not started_selecting:
                                        started_selecting = True
                                        starting_coord = (y_coord+self.cursor_y,x_coord+self.cursor_x) # for selecting 
                                        

                                   if not started_drawing:
                                        started_drawing = True
                                        drawing_object,draw_obj_ind = self.assign_drawing_object(y_coord+self.cursor_y,x_coord+self.cursor_x)
                                        
                                   
                                   else: # To avoid an error a key error for Painting Chars

                                        
                                        self.drew_or_typed = True

                                        if drawing_char != '┼':

                                             y_inc,x_inc = keys[key][0],keys[key][1]

                                             old_y = self.cursor_y
                                             old_x = self.cursor_x
                                             
                                             self.cursor_y += y_inc
                                             self.cursor_x += x_inc

                                             drawing_object.add(y_pos=y_coord+self.cursor_y,x_pos=x_coord+self.cursor_x,newchar=drawing_char)
                                             self.textlist[y_coord+self.cursor_y] = self.textlist[y_coord+self.cursor_y][0:x_coord+self.cursor_x]\
                                                                          +drawing_char+self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x+1:]

                                        else:     
                                             
                                             char_from = orig_char = self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x]
                                             char_above = char_below = char_left = char_right = ' '
                                             char_above = self.textlist[y_coord+self.cursor_y-1][x_coord+self.cursor_x]
                                             char_below = self.textlist[y_coord+self.cursor_y+1][x_coord+self.cursor_x]
                                             char_left = self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x-1]
                                             char_right = self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x+1]


                                             new_char = self.BOX_CHAR[painting_chars[(last_key,key)][0]]
                                             y_inc,x_inc = painting_chars[(last_key,key)][1],painting_chars[(last_key,key)][2]

                                             if new_char in (self.BOX_CHAR['ru'],self.BOX_CHAR['lu'],self.BOX_CHAR['ll'],self.BOX_CHAR['rl']):


                                                  if new_char == self.BOX_CHAR['ru'] and char_above in [self.BOX_CHAR[x] for x in bottom_touching]:
                                                       new_char = self.BOX_CHAR['rm']
                                                  if new_char == self.BOX_CHAR['ru'] and char_right in [self.BOX_CHAR[x] for x in left_touching]:
                                                       new_char = self.BOX_CHAR['xl']
                
                                                  if new_char == self.BOX_CHAR['lu'] and char_above in [self.BOX_CHAR[x] for x in top_touching]:
                                                       new_char = self.BOX_CHAR['lm']
                                                  if new_char == self.BOX_CHAR['lu'] and char_left in [self.BOX_CHAR[x] for x in right_touching]:
                                                       new_char = self.BOX_CHAR['lm']
                                                  if new_char == self.BOX_CHAR['ll'] and char_left in [self.BOX_CHAR[x] for x in right_touching]:
                                                       new_char = self.BOX_CHAR['xu']
                                                  if new_char == self.BOX_CHAR['ll'] and char_below in [self.BOX_CHAR[x] for x in top_touching]:
                                                       new_char = self.BOX_CHAR['lm']
                                                  if new_char == self.BOX_CHAR['rl'] and char_right in [self.BOX_CHAR[x] for x in left_touching]:
                                                       new_char = self.BOX_CHAR['xu']
                                                  if new_char == self.BOX_CHAR['rl'] and char_below in [self.BOX_CHAR[x] for x in top_touching]:
                                                       new_char = self.BOX_CHAR['rm']
                                                  if new_char in [self.BOX_CHAR['rm'],self.BOX_CHAR['lm'],self.BOX_CHAR['xu'],self.BOX_CHAR['xl']] and char_above in [self.BOX_CHAR[x] for x in bottom_touching] \
                                                     and char_below in [self.BOX_CHAR[x] for x in top_touching] \
                                                     and char_right in [self.BOX_CHAR[x] for x in left_touching] \
                                                     and char_left in [self.BOX_CHAR[x] for x in right_touching]:
                                                       new_char = self.BOX_CHAR['x']
                                                  
                                                  
                                                  drawing_object.add(y_pos=y_coord+self.cursor_y,x_pos=x_coord+self.cursor_x,newchar=new_char)
                                                  self.textlist[y_coord+self.cursor_y] = self.textlist[y_coord+self.cursor_y][0:x_coord+self.cursor_x]\
                                                                               +new_char+self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x+1:]
                                                  
                                                  
                                                  
                                                  
                                             else:

                                                  
                                                  old_y = self.cursor_y
                                                  old_x = self.cursor_x
                                                  
                                                  self.cursor_y += y_inc
                                                  self.cursor_x += x_inc
                                                  

                                                  if char_from == self.BOX_CHAR['v'] and x_inc != 0:
                                                       

                                                       if self.cursor_x == 1:
                                                            new_char = self.BOX_CHAR['rm']
                                                       else:
                                                            new_char = self.BOX_CHAR['lm']
                                                  if char_from == self.BOX_CHAR['h'] and y_inc != 0:
                                                       if self.cursor_y == 1:
                                                            new_char = self.BOX_CHAR['xl']
                                                       else:
                                                            new_char = self.BOX_CHAR['xu']

                                                  
                                                  drawing_object.add(y_pos=y_coord+self.cursor_y,x_pos=x_coord+self.cursor_x,newchar=new_char)
                                                  self.textlist[y_coord+self.cursor_y] = self.textlist[y_coord+self.cursor_y][0:x_coord+self.cursor_x]\
                                                                               +new_char+self.textlist[y_coord+self.cursor_y][x_coord+self.cursor_x+1:]
                                                  
                                                 
                                             if key not in [ord('#'),ord('%'),ord('*'),ord('.'),ord('>'),ord(','),ord('<'),287,339,338,358,262,ord('|'),ord('_'),ord('+'),ord('='),curses.KEY_TAB,curses.KEY_BACKSPACE]:
                                                  last_key = key

                                   

                              

                         elif cycling and key in keys:
                              
                              if key == curses.KEY_RIGHT:
                                   next_note = next(self.cycling_through)
                                   
                              elif key == curses.KEY_LEFT:
                                   for x in range(len(self.object_dict.keys())-1):
                                        next_note = next(self.cycling_through)
                                   
                              elif key == curses.KEY_UP:
                                   self.cycling_through = cycle(self.object_dict.keys())
                                   next_note = next(self.cycling_through)
                                   
                              elif key == curses.KEY_DOWN:
                                   self.cycling_through = cycle(self.object_dict.keys())
                                   for x in range(len(self.object_dict.keys())-1):
                                        next_note = next(self.cycling_through)
                                   

                              if 'p' in self.object_dict[next_note]:
                                   positions = self.object_dict[next_note]['p']  #for notes
                                   
                                   y_coord = max([0,positions[0]-self.cursor_y])# to keep from going 
                                   x_coord = max([0,positions[1]-self.cursor_x])# off the side

                              elif 'c' in self.object_dict[next_note]:          # for non-note objects 
                                   y_coord, x_coord = self.object_dict[next_note]['c'].top_left()
                                   y_coord = max([0,y_coord-self.cursor_y])     # to keep from going 
                                   x_coord = max([0,x_coord-self.cursor_x])     # off the side 
                                
                         elif key in keys and (extending or contracting):
                              
                              up, down, left, right = ec_keys[key][0]*multiplier,\
                                                      ec_keys[key][1]*multiplier,\
                                                      ec_keys[key][2]*multiplier,\
                                                      ec_keys[key][3]*multiplier

                              if contracting:
                                   x_total, y_total = self.trim(up,down,left,right)
                                   if x_total < x_max:
                                        x_max = x_total
                                   if y_total < y_max:
                                        y_max = y_total
                              elif extending:
                                        x_total, y_total = self.extend(up,down,left,right)

                         elif key in keys and cursor_move:

                              y_inc,x_inc = keys[key][0],keys[key][1]

                              self.cursor_y += y_inc
                              self.cursor_x += x_inc
                              self.cursor_moved = True 
                              if self.cursor_y < 0:
                                   self.cursor_y = 0
                              elif self.cursor_y > y_max - 9:
                                   self.cursor_y = y_max - 9
                              if self.cursor_x < 0:
                                   self.cursor_x = 0
                              elif self.cursor_x > x_max - 3:
                                   self.cursor_x = x_max - 3
                                        


                         elif key in keys:
                              y_inc,x_inc = keys[key][0],keys[key][1]
                              
                              if not moving_object:

                                   y_coord += y_inc * multiplier
                                   x_coord += x_inc * multiplier

                              if moving_object:
                                   #and self.find_object_in(y_coord+self.cursor_y,x_coord+self.cursor_x)
                                   self.move_object(objects_to_move,y_inc*multiplier,x_inc*multiplier,mode='o')
                                   if moving_screen_too:
                                        x_coord += x_inc * multiplier
                                        y_coord += y_inc * multiplier
                                   
                    elif key == curses.KEY_F3:
                         # toggles between extension, contraction, and cursor
                         if typing:
                              cursor_move = True
                              extending = False
                              contracting = False
                              moving_object = False
                              moving_screen_too = False
                              drawing = False
                              typing = False
                              self.cursor_moved = True
                         elif cursor_move:
                              cursor_move = False
                              extending = True
                              contracting = False
                              moving_object = False
                              moving_screen_too = False
                              drawing = False
                              typing = False
                              self.cursor_moved = True
                         elif extending:
                              cursor_move = False
                              extending = False
                              contracting = True
                              moving_object = False
                              moving_screen_too = False
                              drawing = False
                              typing = False
                              self.cursor_moved = True
                         elif contracting:
                              moving_object = True
                              cursor_move = False
                              extending = False 
                              contracting = False
                              moving_screen_too = False
                              drawing = False
                              typing = False
                              self.cursor_moved = True
                         elif moving_object and not moving_screen_too:
                              moving_object = True
                              cursor_move = False
                              extending = False 
                              contracting = False
                              moving_screen_too = True
                              drawing = False
                              typing = False
                              self.cursor_moved = True
                         elif moving_object and  moving_screen_too:
                              moving_object = False
                              cursor_move = False
                              extending = False 
                              contracting = False
                              moving_screen_too = False
                              drawing = True
                              typing = False
                              self.cursor_moved = True 
                         elif drawing:
                              cursor_move = False
                              extending = False
                              contracting = False
                              moving_object = False
                              moving_screen_too = False
                              drawing = False
                              typing = False
                              self.cursor_moved = True
                         else:
                              cursor_move = False
                              extending = False
                              contracting = False
                              moving_object = False
                              moving_screen_too = False
                              drawing = False
                              typing = True
                              self.cursor_moved = True
                              
                              
                              
                    if not typing:

                         started_typing = False

##                         if key == curses.KEY_F1:
##                              show_note=fill(help_script)
##                              width = len(show_note[0])+2
##                              height = len(show_note)+2
##                              
##                              rectangle = self.make_rectangle (height=height,
##                                                               width=width,
##                                                               divider=0)
##                              rectangle = self.put_in (1,1,fromtextlist=show_note,
##                                                       totextlist=rectangle,
##                                                       skip=[' '])
##                              
##
##                              self.import_note (index='help',show_note=rectangle,full_note=rectangle,keyset={})
                         if key == curses.KEY_F4:
                              contracting = not contracting
                              if contracting and extending:
                                   extending = False
                         elif entering or key == curses.KEY_F2:
                              divider = 3
                              startnote = False
                              note_y_dim = 10
                              note_x_dim = 10
                              object_textlist = None
                              object_keylist = None
                              editing = ''
                              if self.is_clear(y_coord+3,
                                               x_coord+3,
                                               note_y_dim,
                                               note_x_dim):
                                   # To create a new note
                                   frame = self.new_note(y_coord+3,
                                                         x_coord+3,
                                                         note_y_dim,
                                                         note_x_dim,
                                                         divider=divider,
                                                         BOX_CHAR=self.BOX_CHAR)
                                   put(y_coord,x_coord)
                                   startnote = True
                              elif self.find_object_in(y_coord+3,x_coord+3):
                                   # To edit an existing note
                                   editing = '$$'
                                   
                                   
                                   obj = self.find_object_in(y_coord+3,x_coord+3)
                                   

                                   if obj and obj in self.object_dict:

                                        positions = self.object_dict[obj]['p']
                                        note_y_dim = positions[2] - positions[0]
                                        note_x_dim = positions[3] - positions[1]
                                        object_textlist = self.object_dict[obj]['o'] #the display text
                                        if self.object_dict[obj]['oo']:
                                             object_textlist = self.object_dict[obj]['oo']  #the full text of the note                                         
                                             object_keyset = self.object_dict[obj]['l']
                                             object_keylist = [str(obj) + ' | ' + ', '.join(object_keyset),'']


                                        else:
                                             # to extract information from an enframed note
                                             object_keylist = '\n'.join(object_textlist).split(self.BOX_CHAR['lm'])[0]
                                             object_textlist ='\n'.join(object_textlist).split(self.BOX_CHAR['rm'])[1]

                                             

                                             for char in self.BOX_CHAR:

                                                  object_keylist = object_keylist.replace(self.BOX_CHAR[char],'')
                                                  object_textlist = object_textlist.replace(self.BOX_CHAR[char],'')
                                             object_keylist = [x.rstrip() for x
                                                               in object_keylist.split('\n')
                                                               if x.rstrip()] #purges empty lines
                                             object_textlist = [x.rstrip() for x
                                                                in object_textlist.split('\n')
                                                                if x.rstrip()]

                                                    
                                        divider = len(object_keylist)+1
                                        self.delete_object(obj)
                                        frame = self.new_note(y_coord+3,
                                                              x_coord+3,
                                                              note_y_dim,
                                                              note_x_dim,
                                                              divider=divider)
                                        put(y_coord,x_coord)
                                        startnote = True

                                        
                              if startnote:      
                                   
                                   while True: #to establish size of new note 


                                        frame_key = screen.getch()
                                        if frame_key in keys or frame_key in [338,339]:

                                             
                                             frame = self.new_note(y_coord+3,
                                                                   x_coord+3,
                                                                   note_y_dim,
                                                                   note_x_dim,
                                                                   blank=True,
                                                                   divider=divider)
                                             # to delete the existing frame before resizing

                                             if frame_key in keys:
                                                  fy_inc, fx_inc = keys[frame_key]
                                                  
                                                  y_temp = note_y_dim
                                                  x_temp = note_x_dim
                                                  note_y_dim += fy_inc
                                                  note_x_dim += fx_inc
                                                  note_y_dim += fy_inc
                                                  note_x_dim += fx_inc
                                             if frame_key in [339,338]:
                                                  if frame_key == 338:
                                                       divider += 1
                                                  if frame_key == 339:
                                                       divider -= 1
                                             if divider < 0:
                                                  divider = 0
                                             if divider > note_y_dim -1:
                                                  divider = note_y_dim - 1
                                                  
                                             
                                             if note_y_dim <10:
                                                  note_y_dim = 10
                                             if note_x_dim <10:
                                                  note_x_dim = 10
                                             if note_y_dim > y_max:
                                                  note_y_dim = y_max
                                             if note_x_dim > x_max:
                                                  note_x_dim = x_max
                                             if self.is_clear(y_coord+3,
                                                              x_coord+3,
                                                              note_y_dim,
                                                              note_x_dim):
                                                  
                                                  frame = self.new_note(y_coord+3,
                                                                        x_coord+3,
                                                                        note_y_dim,
                                                                        note_x_dim,
                                                                        divider=divider)
                                                  put(y_coord,x_coord)
                                             else:
                                                  self.new_note(y_coord+3,x_coord+3,note_y_dim,note_x_dim,divider=divider)
                                                  put(y_coord,x_coord)
                                                  
                                             
                                        if frame_key == curses.KEY_F2:
                                             break

                                   

                                   section = False # False for the upper window/True for the lower window
                                   sizing = {False:(divider-1,5,3),  
                                             True:(note_y_dim-divider-2,5+divider,3)}
                                             #verticle dimension/vertical starting coordinate/horizontal starting coordinate

                                   count = 0

                                   if isinstance(object_textlist,str):
                                        # For transforming a string into a list 
                                        temp_x_dim = note_x_dim-int(note_x_dim/3)
                                        # for the right margin 

                                        linelist = []

                                        for paragraph in object_textlist.split('\n'):
                                             

                                             line = ''

                                             counter = 0
                                             for counter, char in enumerate(paragraph):
                                                  if char != ' ':
                                                       break
                                             line = counter * ' '
                                             paragraph = paragraph[counter:]

                                             for word in paragraph.split(' '):
                                                  if word:
                                                       if (len(line) + len(word)) < temp_x_dim:
                                                            line += word + ' '
                                                       elif not line and (len(word) >= temp_x_dim):
                                                            line += word + ' '
                                                            linelist.append(line)
                                                            line = ''
                                                       else:
                                                            line += word + ' '
                                                            linelist.append(line)
                                                            line = ''
                                             linelist.append(line)
                                        object_textlist = linelist
                                        if  note_y_dim > len(linelist):
                                             object_textlist +=(note_y_dim - len(linelist))*' '

           
                                   # the entry box for the keywords
                                   newkeys1, newkeys2 = None, None 
                                   newpad = ScrollPad(sizing[section][0],
                                                           note_x_dim-2,
                                                           sizing[section][1],
                                                           2,sizing[section][2],
                                                           l_margin=1,screen=screen,
                                                           textlist=object_keylist,
                                                           bufferobject_undo=LimitedStack(),
                                                           bufferobject_redo=LimitedStack())
                                   temp_typed = newpad.type(frame,skip=(divider==0))
                                   newkeys1,newkeys2 = fill(temp_typed[0]), fill(temp_typed[1])
                                   section = True
##                                   if divider == 0:
##                                        sizing[section] = (sizing[section][0]-1,sizing[section][1],sizing[section][2])
                                   # the entry box for the text

                                   

                                        

                                   
                                   newpad = ScrollPad(sizing[section][0],note_x_dim-2,sizing[section][1],
                                                      2,sizing[section][2],l_margin=1,screen=screen,
                                                      textlist=object_textlist,
                                                      bufferobject_undo=LimitedStack(),
                                                      bufferobject_redo=LimitedStack())
                                   temp_typed = newpad.type(newkeys1,y_offset=divider)
                                   newnote1,newnote2 = fill(temp_typed[0]), fill(temp_typed[1])
                                   if not newnote1:
                                        newnote1 = [' ']
                                   if not newnote2:
                                        newnote2 = [' ']
                                   if '|' in ''.join(newkeys2):
                                        newindex = ''.join(newkeys2).split('|')[0].strip()
                                        newkeys2 = ''.join(newkeys2).split('|')[1]
                                        try:
                                             newindex = str(Index(index_expand(newindex)))
                                        except:
                                             newindex = max([int(str(x).split('.')[0]) for x in self.added_notes])+1
                                             
                                   else:
                                        newindex = max([int(str(x).split('.')[0]) for x in self.added_notes])+1                              
                                   self.added_notes.add(newindex)
                                   newindex = '$'+editing+str(newindex)
                                   keyset = {k_temp.strip() for k_temp in ''.join(newkeys2).split(',')}
                                   self.import_note(newindex,newnote1,newnote2,keyset)
                                   self.new_note(y_coord+3,x_coord+3,note_y_dim,note_x_dim,blank=True,divider=divider)
                                        # to delete old note 
                                   self.add_from_stack(y_pos=y_coord+3,x_pos=x_coord+3)
                                   
                                    # deletes the note frame and text

                                   section = not section
                           

                         elif key == curses.KEY_TAB and not drawing:
                              next_note = next(self.cycling_through)
                              label = '['+ str(next_note) + '] '
                              
                              
                              if next_note in self.moving_qualities:
                                   
                                   label += str(self.moving_qualities[next_note][0]) + '/' + str(self.moving_qualities[next_note][1])
                              
                              self.print_to(screen,label,length=40,y_pos=y_max-3,x_pos=20)
                              
                              if 'p' in self.object_dict[next_note]:            #for notes 
                                   positions = self.object_dict[next_note]['p']
                                   y_coord = max([0,positions[0]-self.cursor_y])
                                   x_coord = max([0,positions[0]-self.cursor_x])
                                   put(y_coord,x_coord)
                                   self.delete_object(next_note,for_show=True)
                                   self.add_object(next_note,for_show=True)
                                   length = 1
                                   movementtype = 'r'
                                   while True:
                                        
                                        label = '[' + str(next_note) + '] '
                                        label += str(movementtype+ '/' + str(length))
                                        self.print_to(screen,' '*45,length=45,y_pos=y_max-2,x_pos=20)
                                        self.print_to(screen,label,length=40,y_pos=y_max-2,x_pos=20)
                                        
                                        selected_key = screen.getch()
                                        if selected_key in [curses.KEY_TAB]:
                                             self.print_to(screen,' '*45,length=45,y_pos=y_max-3,x_pos=20)
                                             self.print_to(screen,' '*45,length=45,y_pos=y_max-2,x_pos=20)
                                             break
                                        if selected_key == ord('s'):
                                             movementtype = 's'
                                        elif selected_key == ord('s'):
                                             movementtype = 'r'
                                        elif selected_key == curses.KEY_UP:
                                             length *= 10
                                        elif selected_key == curses.KEY_DOWN:
                                             length =  max([1,int(length/10)])
                                        elif selected_key == curses.KEY_RIGHT:
                                             length += 1
                                        elif selected_key == curses.KEY_LEFT:
                                             length -= 1 
                                        elif selected_key == ord('+'):
                                             self.moving_qualities[next_note] = (movementtype,length)
                                        elif selected_key == ord('-'):
                                             del self.moving_qualities[next_note]
                                        
                                             
                                        
                                        
                                   
                                             
                                   
                                   
                              elif 'c' in self.object_dict[next_note]:          # for non-note objects 
                                   y_coord, x_coord = self.object_dict[next_note]['c'].top_left()
                                   y_coord = max([0,y_coord-self.cursor_y])     # to keep from going 
                                   x_coord = max([0,x_coord-self.cursor_x])     # over the edge
                                   put(y_coord,x_coord)

                                   length = 1
                                   movementtype = 'r'
                                   while True:
                                        
                                        label = '[' + str(next_note) + '] '
                                        label += str(movementtype+ '/' + str(length))
                                        self.print_to(screen,' '*45,length=45,y_pos=y_max-2,x_pos=20)
                                        self.print_to(screen,label,length=40,y_pos=y_max-2,x_pos=20)
                                        
                                        selected_key = screen.getch()
                                        if selected_key in [curses.KEY_TAB]:
                                             self.print_to(screen,' '*45,length=45,y_pos=y_max-3,x_pos=20)
                                             self.print_to(screen,' '*45,length=45,y_pos=y_max-2,x_pos=20)
                                             break
                                        if selected_key == ord('s'):
                                             movementtype = 's'
                                        elif selected_key == ord('s'):
                                             movementtype = 'r'
                                        elif selected_key == curses.KEY_UP:
                                             length *= 10
                                        elif selected_key == curses.KEY_DOWN:
                                             length =  max([1,int(length/10)])
                                        elif selected_key == curses.KEY_RIGHT:
                                             length += 1
                                        elif selected_key == curses.KEY_LEFT:
                                             length -= 1 
                                        elif selected_key == ord('+'):
                                             self.moving_qualities[next_note] = (movementtype,length)
                                        elif selected_key == ord('-'):
                                             del self.moving_qualities[next_note]
                                        
                                             
                                    

                                   
                                   


                         elif key == ord ('o'):
                              screen.nodelay(True)
                              starting = True
                              new_direction = False
                              y_coord = int(y_total/2)
                              x_coord = int(x_total/2)
                              float_y = float(y_coord)
                              float_x = float(x_coord)
                              key_pressed = -1
                              
                              while key_pressed == -1:
                                   key_pressed = screen.getch()
                                   if starting:
                                        direction = random.choice(range(360))
                                        going_for = 0
                                        starting = False
                                   going_for += 1
                                   if float_y  < 10:
                                        float_y  = 10.0
                                        new_direction = True                                  
                                   elif float_y  > y_total - y_max -10:
                                       float_y  = float(y_total - y_max - 10)
                                       new_direction = True 
                                   if float_x < 10:
                                        float_x = 10.0
                                        new_direction = True                                       
                                   elif float_x > x_total - x_max - 10:
                                        float_x = float(x_total - x_max - 10)
                                        new_direction = True
                                   if new_direction:
                                        direction = random.choice(range(360))
                                        new_direction = False

                                   float_y += sin(direction) 
                                   float_x += cos(direction)

                                   if abs(y_coord-int(float_y)) + abs(x_coord-int(float_x)) >= 1:
                                          y_coord = int(float_y)
                                          x_coord = int(float_x)
                                   put(y_coord,x_coord)
                                   time.sleep(.02)
                                   self.print_to(screen,
                                                 str(x_coord)
                                                 +'/'+str(x_total)
                                                 +' : '+str(y_coord)
                                                 +'/'+str(y_total),
                                                 length=20,
                                                 y_pos=2,
                                                 x_pos=3)
                              screen.nodelay(False)
                                   
                                                                     
                                 
                         elif key == ord('n'):

                              screen.nodelay(True)
                              key_pressed = -1

                              while key_pressed == -1:
                                   key_pressed = screen.getch()
                                   next_note = next(self.cycling_through)
                                   if 'p' in self.object_dict[next_note]:
                                        positions = self.object_dict[next_note]['p']
                                        y_coord = max([0,positions[0]-5])
                                        x_coord = max([0,positions[1]-10])
                                        

                                   elif 'c' in self.object_dict[next_note]:          # for non-note objects 
                                        y_coord, x_coord = self.object_dict[next_note]['c'].top_left()
                                        y_coord = max([0,y_coord-self.cursor_y])     # to keep from going 
                                        x_coord = max([0,x_coord-self.cursor_x])     # over the edge 
                                   time.sleep(.5)
                                   put(y_coord,x_coord)

                              screen.nodelay(False)
                         elif key == 3: # to copy object

                              object_to_copy = self.find_object_in(y_coord+self.cursor_y,x_coord+self.cursor_x)
                              if object_to_copy:
                                   if 'o' in self.object_dict[object_to_copy]:

                                        self.copy_buffer = DrawingObject(textlistobject=self.textlist,objectlist=self.object_dict[object_to_copy]['o'])
                                   elif 'c' in self.object_dict[object_to_copy]:
                                        self.copy_buffer = DrawingObject(textlistobject=self.textlist,schema=self.object_dict[object_to_copy]['c'].get_schema())
                                        
                         elif key == 22: # to paste objet 

                              if self.copy_buffer:
                                   copy_object,draw_obj_ind = self.assign_drawing_object(y_coord+self.cursor_y,
                                                                                            x_coord+self.cursor_x,
                                                                                            schema=self.copy_buffer.get_schema())
                                   
                                   copy_object.position_object(y_pos=y_coord+self.cursor_y,x_pos=x_coord+self.cursor_x,from_schema=True)
                                   self.add_drawn_object(draw_obj_ind)

                         elif key == 279:

                              linetype = next(self.linetypes)
                              if linetype == 'normal':
                                   self.BOX_CHAR = BOX_CHAR_NORMAL
                              elif linetype == 'round':
                                   self.BOX_CHAR = BOX_CHAR_ROUND
                              elif linetype == 'thick':
                                   self.BOX_CHAR = BOX_CHAR_THICK
                              elif linetype == 'double':
                                   self.BOX_CHAR = BOX_CHAR_DOUBLE
                              
                                   
                                   
                         elif key == 288:
                              # shift F12
                              if drawing:
                                   hs=1
                              else:
                                   hs=0
                              if self.help is None:
                                   
                                   self.help = self.show_temporary(showlist=helpscripts[hs])
                                   next(self.help)
                                        
                              else:
                                   
                                   next(self.help)
                                   self.help = None 


                                 
                         elif key == 92:
                              if self.find_object_in(y_coord+self.cursor_y,x_coord+self.cursor_x):
                                   if self.find_object_in(y_coord+self.cursor_y,x_coord+self.cursor_x) in self.selected:
                                        self.selected.discard(self.find_object_in(y_coord+self.cursor_y,x_coord+self.cursor_x))
                                   else:
                                        self.selected.add(self.find_object_in(y_coord+self.cursor_y,x_coord+self.cursor_x))
                                        is_selected = True
                         elif key == curses.KEY_F5:
                              moving_object = not moving_object
                         elif key == curses.KEY_F6:
                              moving_screen_too = not moving_screen_too
                         elif key == curses.KEY_F7:
                              if (self.find_object_in(y_coord+self.cursor_y,
                                                      x_coord+self.cursor_x)):
                                   objects_to_move.add(self.find_object_in(y_coord+self.cursor_y,
                                                                           x_coord+self.cursor_x))
                         elif key == curses.KEY_F8:
                              if (self.find_object_in(y_coord+self.cursor_y,
                                                      x_coord+self.cursor_x)):  
                                   objects_to_move.discard(self.find_object_in(y_coord+self.cursor_y,
                                                                               x_coord+self.cursor_x))
                         elif key in [curses.KEY_F10,curses.KEY_BREAK,curses.KEY_EXIT]:
                              go_on = False
                         elif key in [curses.KEY_DELETE,curses.KEY_BACKSPACE] and self.find_object_in(y_coord+self.cursor_y,
                                                                               x_coord+self.cursor_x):

                              obj_temp = self.find_object_in(y_coord+self.cursor_y,
                                                                     x_coord+self.cursor_x)

                              if not obj_temp.startswith('%'):
                                   self.delete_object(obj_temp)
                                   
                              else:
                                   self.delete_drawn_object(obj_temp)
                                   if key == curses.KEY_DELETE:
                                        self.import_note(obj_temp)

                                   else:
                                        del self.object_dict[obj_temp]
                                   
                                        
                         elif key == ord('['):
                              if y_coord - y_max >= 0:
                                   
                                   y_coord -= y_max
                              
                         elif key == ord(']'):
                              if y_coord - y_max <= y_total:
                                   
                                   y_coord += y_max
                         elif key == ord('{'):
                              if x_coord - x_max >= 0:
                                   x_coord -= x_max
                         elif key == ord('}'):
                              if x_coord + x_max <= x_total:
                                   x_coord += x_max
                         elif key == curses.KEY_F9:
                              if not selecting and not cycling:
                                   cycling = True
                                   
                              elif cycling and not selecting:
                                   selecting = True
                                   cycling = False
                                   
                              elif selecting and not cycling:
                                   selecting = False   
                                   cycling = False 
                              
                              
                         elif key == curses.KEY_F11:
                              stack_dump = True
                         elif key == 19:
                              return_text = '\n'.join(self.textlist)
                              save_file (returntext=return_text,
                                         filename = 'workpad '+str(datetime.datetime.now()).split('.')[0].replace(':',' '))
                              
                         elif key == 1:
                              return_text = '\n'.join([x[x_coord:x_coord+x_max-17] for x in self.textlist[y_coord:y_coord+y_max-8]])
                              save_file (returntext=return_text,
                                         filename = 'screenshot '+str(datetime.datetime.now()).split('.')[0].replace(':',' '))
                                   
                                   
                         elif key == ord('z'):

                              if multiplier > 1:
                                   multiplier -= 1
                         elif key == ord('x'):
                              if multiplier <30:
                                   multiplier += 1
          
                         elif key == curses.KEY_INSERT:
                              self.add_from_stack(y_pos=y_coord+self.cursor_y,x_pos=x_coord+self.cursor_x)
                         elif key == ord('c'):
                              self.size -= 1
                         elif key == ord('v'):
                              self.size += 1
                         elif key == ord('m'):
                              screen.nodelay(True)
                              

                              old_textlist = copy.deepcopy(self.textlist)
                              old_object_dict = copy.deepcopy(self.object_dict)
                              
                              
                              

                              temp_dict = {}

                              if self.moving_qualities:


                                   for temp_ind in self.moving_qualities:

                                        movementtype = self.moving_qualities[temp_ind][0]
                                        attribute2 = self.moving_qualities[temp_ind][1]
                                        if temp_ind in self.object_dict:
                                             if 'p' in self.object_dict[temp_ind]:

                                                  positions = self.object_dict[temp_ind]['p']
                                                  y_p = positions[0]
                                                  x_p = positions[1]
                                                  y_d = positions[2]-positions[0]
                                                  x_d = positions[3]-positions[1]

                                                  self.moving_dict[temp_ind]  = Movement(movementtype=movementtype,
                                                                                         attribute2=attribute2,
                                                                                         y_pos=y_p,
                                                                                         x_pos=x_p,
                                                                                         y_dim=y_d,
                                                                                         x_dim=x_d)
                                             elif 'c' in self.object_dict[temp_ind]:
                                                  positions = self.object_dict[temp_ind]['c'].boxed_dimensions()
                                                  y_p = positions[0]
                                                  x_p = positions[1]
                                                  y_d = positions[2]-positions[0]
                                                  x_d = positions[3]-positions[1]
          
                                                  self.moving_dict[temp_ind] = Movement(movementtype=movementtype,
                                                                                         attribute2=attribute2,
                                                                                         y_pos=y_p,
                                                                                         x_pos=x_p,
                                                                                         y_dim=y_d,
                                                                                         x_dim=x_d)

                                            
     

                              iteration = 0
                              key_pressed = -1
                              distance = 1
                              left_odd = 100
                              key_set = 0
                              iteration = 0
     ##                              try:
                              while key_pressed in [-1,curses.KEY_UP,curses.KEY_DOWN,curses.KEY_LEFT,curses.KEY_RIGHT,curses.KEY_INSERT]:
                                   key_pressed = screen.getch()
                                   iteration += 1
                                   
                                   if conway:
                                        
                                        if key_pressed == curses.KEY_UP:
                                             distance += 1
                                        elif key_pressed == curses.KEY_DOWN:
                                             distance -= 1
                                        elif key_pressed == curses.KEY_LEFT:
                                             left_odd += 5
                                        elif key_pressed == curses.KEY_RIGHT:
                                             left_odd -= 5
                                        elif key_pressed == curses.KEY_INSERT:
                                             key_set += 1
                                        if left_odd < 50:
                                             left_odd = 50
                                        if left_odd > 100:
                                             left_odd = 100
                                        if distance > 5:
                                             distance = 5
                                        if distance < 1:
                                             distance = 1
                                             
                                        conway.change_odds((left_odd,100),key=(key_set%4)+1)
                                        conway.change_distance(distance)
                                        if random.randrange(0,3) == 2:
                                             conway.burst()
                                        self.print_to(screen,str(iteration)+' / '+str(distance)+' / '+str(conway.get_properties()),length=90,y_pos=2,x_pos=25)
                                        
                                        
                                        
                                        
                                        conway.generate()
                                   iteration += 1
                                   for obj in self.moving_dict:
                                        
                                        
                                        dummy1,dummy2,y_inc,x_inc,counter = self.moving_dict[obj].move()
                                          
                                   
                                        self.move_object([obj],
                                                         y_inc,
                                                         x_inc,
                                                         auto=True)
                                        
                                   
##                                   if iteration == 100:
##                                        y_coord = random.randrange(0,y_total-y_max,y_max)
##                                        x_coord = random.randrange(0,x_total-x_max,x_max)
##                                        iteration = 0
##                                        curses.beep()
                                        put(y_coord,x_coord)
                                   put(y_coord,x_coord)
                              
     ##                                        
     ##                              except:
     ##                                   pass
                              screen.nodelay(False)
                              if key_pressed != ord('m'):
                                   
                                   self.textlist = old_textlist
                                   self.object_dict = old_object_dict
                              
                                   
                                   


                         
                    
                                   
                    
               self.print_to(screen,
                             str(x_coord)
                             +'/'+str(x_total)
                             +' : '+str(y_coord)
                             +'/'+str(y_total),
                             length=20,
                             y_pos=2,
                             x_pos=3)
                

               if y_coord < 0:
                    y_coord = 0
                    curses.beep()
                    curses.flushinp()
               elif y_coord > y_total - y_max:
                    y_coord = y_total - y_max
                    curses.beep()
                    curses.flushinp()
               if x_coord < 0:
                    x_coord = 0
                    curses.beep()
                    curses.flushinp()
               elif x_coord > x_total - x_max:
                    x_coord = x_total - x_max
                    curses.beep()
                    curses.flushinp()



               put(y_coord,x_coord)


               if entering:
                    self.add_from_stack(y_coord,x_coord)
                    once_through = True

          if self.copy_buffer:

               return  y_coord,x_coord,self.object_dict,self.textlist, return_boxed_note(schema=self.copy_buffer.get_schema())
          else:
               return  y_coord,x_coord,self.object_dict,self.textlist,''
                    

##          except:
##               
##               return y_coord,x_coord,self.object_dict,self.textlist, return_boxed_note(schema=self.copy_buffer)

          

if __name__ == '__main__':


     a = EmptyMovingWindow()
     a.activate()

