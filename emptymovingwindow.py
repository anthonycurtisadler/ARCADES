
import curses
import time
from movingwindow import MovingWindow
from stack import Stack 
from math import sqrt
import winsound
from globalconstants import BOX_CHAR
import copy
from itertools import cycle

curses.KEY_RETURN = 10
curses.KEY_TAB = 9
curses.KEY_F1 = 265
curses.KEY_F2 = 266
curses.KEY_F3 = 267
curses.KEY_F4 = 268

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

     

def fill (textlist):

     width = max ([len(x) for x in textlist])
     returnlist = []
     for line in textlist:
          returnlist.append(line+(width-len(line))*' ')
     return returnlist 

class ScrollPad:

     def __init__(self,height=10,width=10,y_pos=5,x_pos=5,u_margin=0,l_margin=0,enframe=False,screen=None):
          self.height = height
          self.width = width
          self.top_line = 0
          self.cursor_y = 0
          self.cursor_x = 0
          self.u_margin = u_margin
          self.l_margin = l_margin


          self.textlist = [' '*self.width]*self.height
          self.window = screen
          self.y_pos = y_pos
          self.x_pos = x_pos

     
     def put_in (self,y_start,x_start,fromtextlist=None,totextlist=None,skip=[' ']):

          for y in range(len(fromtextlist)):
               newline = totextlist[y_start+y][0:x_start]
               for x in range(len(fromtextlist[0])):
                    if fromtextlist[y][x] not in skip:
                         newline+=fromtextlist[y][x]
                    else:
                         newline+=totextlist[y_start+y][x_start+x]
               newline += totextlist[y_start+y][x_start+x+1:]
               totextlist[y_start+y] = newline
                    
          return totextlist

     def add_line (self,lines=1):
          
          self.textlist += [' '*self.width]*lines
         

     def scroll_down (self):
          if self.top_line <= len(self.textlist)-1:
          
               self.top_line +=1
 
     def scroll_up (self):
          if self.top_line > 0:
               self.top_line -=1


     def move_up (self): 

          if self.cursor_y > 0:
               self.cursor_y -= 1
          if self.cursor_y < self.top_line:
               self.top_line -= 1

     def move_down (self):

          
          self.cursor_y += 1
          if self.cursor_y >= self.height - 1:
     
               self.top_line += 1
               self.cursor_y -=1

               if self.top_line + self.height > len(self.textlist) -1:
                    self.add_line()

               self.put_all()

     def move_right (self):

          if self.cursor_x < self.width-1:
               self.cursor_x += 1
          elif self.cursor_x == self.width-1:
               if self.cursor_y < len(self.textlist)-1:
                    self.cursor_x = 0
                    self.move_down()
                    return 'EOL'
               return 'EOT'

               
          

     def hard_return (self):

          self.cursor_x = 0
          self.move_down()
          

     def move_left (self):

          if self.cursor_x > 0:
               self.cursor_x -=1
          elif self._cursor_x == 0:
               if self.cursor_y > 0:
                    self.cursor_x = self.width-1
                    self.move_up()
                    return 'BACK'
               return 'START'

     def put_char (self,char,y=None,x=None):
          if y is None:
               y = self.cursor_y
          if x is None:
               x = self.cursor_x

          self.textlist[self.cursor_y+self.top_line] = self.textlist[self.cursor_y+self.top_line][0:self.cursor_x]\
                                                      +char+self.textlist[self.cursor_y+self.top_line][self.cursor_x+1:]
          self.window.refresh()


     def put_all (self):


          text_line = 0
          y = 0
          
          
          while text_line < len(self.textlist):

               if self.top_line <= text_line < self.top_line+self.height:
##                    self.window.addstr(2,2,'['+str(self.height)+']'+str(self.top_line)+'/'+str(len(self.textlist))+' :'+str(self.cursor_y)+'/'+str(self.cursor_x))
                    
                    for x in range (0,self.width):
                         if y==self.cursor_y and x==self.cursor_x:
                              self.window.addch(self.y_pos+y+self.u_margin,self.x_pos+x+2+self.l_margin,self.textlist[text_line][x],curses.A_REVERSE)
                              
                         else:
                              
                              self.window.addch(self.y_pos+y+self.u_margin,self.x_pos+x+2+self.l_margin,self.textlist[text_line][x])
                    self.window.refresh()
                    y += 1
               text_line += 1
               
                    

     def type (self,framelist=None):
          go_on = True


          while go_on:
               self.put_all()
               key = self.window.getch()

               if key == curses.KEY_ENTER or key == 10 or key == 13:
                    self.hard_return()
               elif key in keys:

                    if self.cursor_x < self.width:
                         self.cursor_x += keys[key][1]
                         if self.cursor_x == self.width:
                              self.cursor_x = 0
                              if self.cursor_y < self.height-1:
                                   self.cursor_y += 1
                                   if self.cursor_y == self.height - 1:
                                        self.move_down()   
                         
                    if self.cursor_y < self.height-1:
                         self.cursor_y += keys[key][0]
                         if self.cursor_y == self.height - 1:
                              self.move_down()
                              

                         
                    
               elif key == 1: ## ctr a 
                    self.scroll_down()
               elif key == 19: ##ctr s
                    self.scroll_up()
               elif 0 <= key < 255:
                    self.put_char(str(chr(key)))

                    self.move_right()
               elif key == 493:

                    self.cursor_y = 0
                    self.top_line = 0
                    self.cursor_x = 0
               elif key == 491:

                    self.cursor_y = self.height - 1
                    self.cursor_x = self.width - 1
                    self.top_line = len(self.textlist)-self.height
                    
                    
               if key == curses.KEY_F1:
                    go_on = False

                    

               self.window.addstr(3,3,'   '+str(key)+'   ')
          self.newtextlist = self.textlist
          if framelist:
               
               self.newtextlist = self.put_in(1,1,self.textlist[self.top_line:self.top_line+self.height-1],framelist) 
          return self.newtextlist,self.textlist
                    
     
               
     
class EmptyMovingWindow (MovingWindow):



     def __init__ (self,textlist=None,y_dim=300,x_dim=300):

 

          if textlist is None:

               self.textlist = [' '*x_dim]*y_dim
          else:
               self.textlist = textlist

          self.object_dict = {}
          self.y_dim = y_dim
          self.x_dim = x_dim
          self.index = 0
          self.size = 5
          self.note_stack = Stack()
          self.added_notes = {0}
          self.cycling_through = None 

     def put_in (self,y_start,x_start,fromtextlist=None,totextlist=None,skip=[' ']):

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

          if dictionaryobject is None:
               dictionaryobject = self.object_dict
          for oldkey in list(dictionaryobject):
               if oldkey.startswith(fromprefix) and oldkey.count(fromprefix)==1:
                    newkey = oldkey.replace(fromprefix,toprefix)
                    dictionaryobject[newkey] = copy.deepcopy(dictionaryobject[oldkey])
                    del dictionaryobject[oldkey] 
               
     
     def make_rectangle (self,height,width,blank=False):
          textlist = []
          if not blank:
               for y in range(0,height):

                    if y == 0:
                         textlist.append(BOX_CHAR['lu']+BOX_CHAR['h']*(width-2)+BOX_CHAR['ru'])
                    elif 0 < y < width-1:
                         textlist.append(BOX_CHAR['v']+' '*(width-2)+BOX_CHAR['v'])
                    else:
                         textlist.append(BOX_CHAR['ll'] + BOX_CHAR['h']*(width-2) + BOX_CHAR['rl'])
          else:
               textlist = [' '*width]*height
                    
          return textlist

     def new_note (self,y_coord,x_coord,height=30,width=30,totextlist=None,blank=False):
          skip = [' ']
          if blank:
               skip = []
          
               
          if totextlist is None:
               totextlist = self.textlist
          frame = self.make_rectangle(height,width,blank=blank)
          self.put_in(y_coord,x_coord,fromtextlist=frame,totextlist=totextlist,skip=skip)
          return frame 


     def extend (self,top_ex=0,bottom_ex=0,left_ex=0,right_ex=0):

          for y in range(len(self.textlist)):
               self.textlist[y] = left_ex*' ' + self.textlist[y] + right_ex *' '
          if self.textlist:
               x_total = len(self.textlist[0])
               self.textlist = [' '*x_total]*top_ex + self.textlist + [' '*x_total]*bottom_ex
          else:
               return 0,0

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

          def establish_margins():

               top_margin = 0
               bottom_margin = 0
               left_margin = 0
               right_margin = 0
               top_found = False
               bottom_found = False
               left_found = False
               right_found = False

               while (len(self.textlist) > top_margin + bottom_margin) and \
                     self.textlist and \
                     (len(self.textlist[0]) > left_margin + right_margin) and \
                     not (top_found and bottom_found and left_found and right_found):

                    if not top_found and  not self.textlist[top_margin].strip(' '):
                         top_margin += 1
                    else:
                         top_found = True

                    if not bottom_found and not self.textlist[-bottom_margin-1].strip(' '):
                         bottom_margin += 1
                    else:
                         bottom_found = True

                    for y in range(len(self.textlist)):
                         if self.textlist[y][left_margin] != ' ':
                              left_found = True
                         if list(reversed(self.textlist[y]))[right_margin] != ' ':
                              right_found = True
                    if not left_found:
                         left_margin += 1
                    if not right_found:
                         right_margin += 1
               return top_margin,left_margin,bottom_margin,right_margin

          top_margin,left_margin,bottom_margin,right_margin = establish_margins()
          if top_tr != -1:
               top_tr = min ([top_tr,top_margin])
          else:
               top_tr = top_margin
          if bottom_tr != -1:
               bottom_tr = min ([bottom_tr,bottom_margin])
          else:
               bottom_tr = bottom_margin
          if left_tr != -1:
               left_tr = min ([left_tr,left_margin])
          else:
               left_tr = left_margin
          if right_tr != -1:
               right_tr = min ([right_tr,right_margin])
          else:
               right_tr = right_margin 

          if bottom_tr != 0:
               self.textlist = self.textlist[top_tr:-bottom_tr]
          else:
               self.textlist = self.textlist[top_tr:]

          if right_tr != 0:
               
               self.textlist = [line[left_tr:-right_tr] for line in self.textlist]
          else:
               self.textlist = [line[left_tr:] for line in self.textlist]



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

          x = max([len(l) for l in textlist])
          
          textlist = [l + (x-len(l))*' ' for l in textlist]
          y = len(textlist)
          return textlist,y,x


     def find_object_in (self,y_pos,x_pos):

          
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
          return ''
     

                    
     def is_clear (self,y_pos,x_pos,y_dim,x_dim):

          if y_pos <=1 or x_pos <=1:
               return False

          if y_pos+y_dim >= self.y_dim or x_pos+x_dim >= self.x_dim:
               
               return False
          
          for y in range(0,y_dim):
               for x in range(0,x_dim):
                    if self.textlist[y_pos+y][x_pos+x] != ' ':
                         return False
          else:
               return True

     def is_clear_quick (self,y_pos,x_pos,y_dim,x_dim,dict_object=None):
          if dict_object is None:
               dict_object = self.object_dict

          

          for key_temp in dict_object:

               positions = dict_object[key_temp]['p']
               up_bound = positions[0]
               left_bound = positions[1]
               down_bound = positions[2]
               right_bound = positions[3]

               if y_pos >= up_bound or \
                  y_pos + y_dim <= down_bound or \
                  x_pos >= left_bound or \
                  x+pos + x_dim <= right_bound:
                    return False
          return True 
               

     def find_clear (self,height,width,start_y=0,start_x=0,from_corner=False):

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
               return str(diagn)

          else:
               diagn = []
               for y,x in centripetal_generator(5,start_y=start_y,start_x=start_x):
                    diagn.append((y,x))
                    if self.is_clear(y_pos=y,x_pos=x,y_dim=height,x_dim=width):
                         
                         return y,x
               return str(diagn)


     def add_from_stack (self,y_st=0,x_st=0):

 

          if not self.note_stack.exists():

               return False
          popped =  self.note_stack.pop()
          if isinstance(popped,(list,tuple)):

               index,note1,note2 = popped[0],popped[1],popped[2]

          else:
               return False
          note1, height, width = self.dimensions(note1)

          try:
               y_pos,x_pos = self.find_clear(height,width,y_st,x_st)
          except:
               return False
          if isinstance(y_pos,int):
               if not note2:

                    self.add_object(index,new_object_list=note1,y_pos=y_pos,x_pos=x_pos)
               else:
                    self.add_object(index,new_object_list=note1,new_object_list2=note2,y_pos=y_pos,x_pos=x_pos)
                    
          return False
                    
     def show_notes (self):
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

     def move_object (self,indexes=None,vert_inc=0,hor_inc=0):

          for index in indexes:

               if index in self.object_dict and 'p' in self.object_dict[index]:
                    
                    positions = self.object_dict[index]['p']
                    up_bound = positions[0]
                    left_bound = positions[1]
                    down_bound = positions[2]
                    right_bound = positions[3]
                    height = down_bound - up_bound
                    width = right_bound - left_bound
                    up_bound += vert_inc
                    down_bound += vert_inc
                    left_bound += hor_inc
                    right_bound += hor_inc
                    
                    if self.find_clear(height,width,up_bound,left_bound):
                         
                         obj = self.object_dict[index]

                         self.delete_object(index)
                         self.add_object (index,new_object_list=obj['o'],
                                          new_object_list2=obj['oo'],
                                          l_prop=obj['l'],
                                          x_prop=obj['x'],
                                          y_pos=up_bound,
                                          x_pos=left_bound)
                    

         

     def delete_object(self,index=''):
          
          if index in self.object_dict and 'p' in self.object_dict[index]:
               positions = self.object_dict[index]['p']
               up_bound = positions[0]
               left_bound = positions[1]
               down_bound = positions[2]
               right_bound = positions[3]
               objecttext = []

               for y in range(up_bound,down_bound):
                    objecttext.append(self.textlist[y][left_bound:right_bound+1])
                    self.textlist[y] = self.textlist[y][0:left_bound] + ' '*(right_bound-left_bound) + self.textlist[y][right_bound:]
                    
               del self.object_dict[index]
               self.import_note(index,objecttext)
               self.cycling_through = cycle(self.object_dict.keys())
                    
               

     def add_object(self,index='',
                    new_object_list=None,
                    new_object_list2=None,
                    l_prop=None,
                    x_prop=None,
                    y_pos=0,
                    x_pos=0):
          
          index = str(index)
          if l_prop is None:
               l_prop = set()

          new_object_list, height,width = self.dimensions(new_object_list)

          if not self.is_clear(y_pos,x_pos,height,width):
               
               return False

          if index not in self.object_dict:

               for y in range(height):

                    self.textlist[y_pos+y] = self.textlist[y_pos+y][0:x_pos]\
                                             + new_object_list[y]\
                                             + self.textlist[y_pos+y][x_pos+width:]



               self.object_dict[index] = {'o':new_object_list,
                                          'oo':new_object_list2,
                                          'p':(y_pos,x_pos,y_pos+height,x_pos+width),
                                          'l':l_prop,
                                          'x':x_prop}
               self.cycling_through = cycle(self.object_dict.keys())
               
          else:
               return False
          

     def import_note (self,index,show_note=None,full_note=None):
          self.note_stack.add((str(index),show_note,full_note))
          
     def display (self,y_pos=0,x_pos=0):
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
          return self.note_stack.size()
          
          
     def moving_screen (self,screen,y_coord=0,x_coord=0,b_margin=4,t_margin=3,l_margin=1,r_margin=1):

          
          def put(y_pos,x_pos):

               if x_pos + x_max > x_total:

                    x_pos = x_total - x_max
               
               for y in range(y_max-1-b_margin-t_margin):

                    if y_pos+y <= y_total:
                         screen.addstr(y+b_margin,l_margin,self.textlist[y_pos+y][x_pos:x_pos+x_max-l_margin-r_margin])

               
                    
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
          cursor_move = False
          cycling = False 
          while go_on :
               self.print_to(screen,self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2)),length=10,y_pos=1,x_pos=20)
               self.print_to(screen,', '.join(sorted(self.object_dict.keys())),length=30,y_pos=1,x_pos=62)
               self.print_to(screen,', '.join(objects_to_move),length=30,y_pos=1,x_pos=31)
               self.print_to(screen,'MOVING OBJECTS'*moving_object+' '+'MOVING SCREEN'*moving_screen_too+' '+'EXTENDING'*extending+' '+'CONTRACTING'*contracting+'CUR'*cursor_move,
                             length=90,y_pos=y_max-3,x_pos=1)
               
               
               
               if stack_dump:
                    if self.note_stack.exists():
                         self.add_from_stack(y_coord,x_coord)
                         curses.beep()
                    else:
                         if stack_dump and not self.note_stack.exists():
                              stack_dump = False
                    
               else:
                    key = screen.getch()
                         

                    if key in keys.keys():

                         if cycling:
                              
                              if key == curses.KEY_RIGHT:
                                   next_note = next(self.cycling_through)
                                   positions = self.object_dict[next_note]['p']
                                   y_coord = positions[0]
                                   x_coord = positions[1]
                              elif key == curses.KEY_LEFT:
                                   for x in range(len(self.object_dict.keys())-1):
                                        next_note = next(self.cycling_through)
                                   positions = self.object_dict[next_note]['p']
                                   y_coord = positions[0]
                                   x_coord = positions[1]
                              elif key == curses.KEY_UP:
                                   self.cycling_through = cycle(self.object_dict.keys())
                                   next_note = next(self.cycling_through)
                                   positions = self.object_dict[next_note]['p']
                                   y_coord = positions[0]
                                   x_coord = positions[1]
                              elif key == curses.KEY_DOWN:
                                   self.cycling_through = cycle(self.object_dict.keys())
                                   for x in range(len(self.object_dict.keys())-1):
                                        next_note = next(self.cycling_through)
                                   positions = self.object_dict[next_note]['p']
                                   y_coord = positions[0]
                                   x_coord = positions[1]
                                   
                                        
                                        
                              

                                   
                         elif extending or contracting:
                              up, down, left, right = ec_keys[key][0],\
                                                      ec_keys[key][1],\
                                                      ec_keys[key][2],\
                                                      ec_keys[key][3]
                              if extending:
                                   x_total, y_total = self.extend(up,down,left,right)
                              if contracting:
                                   x_total, y_total = self.trim(up,down,left,right)
                                   if x_total < x_max:
                                        x_max = x_total
                                   if y_total < y_max:
                                        y_max = y_total



                         else:
                              y_inc,x_inc = keys[key][0],keys[key][1]
                              
                              if not moving_object:

                                   y_coord += y_inc * multiplier
                                   x_coord += x_inc * multiplier

                              if moving_object and self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2)):    
                                   self.move_object(objects_to_move,y_inc*multiplier,x_inc*multiplier)
                                   if moving_screen_too:
                                        x_coord += x_inc * multiplier
                                        y_coord += y_inc * multiplier
                                   
                    elif key == ord('w'):
                         extending = not extending
                         if contracting and extending:
                              contracting = False

                    

                    elif key == ord('t'):
                         cursor_move = not cursor_move 
                    elif key == ord('q'):
                         contracting = not contracting
                         if contracting and extending:
                              extending = False
                    elif key == ord('e'):

                         note_y_dim = 10
                         note_x_dim = 10
                         if self.is_clear(y_coord+3,x_coord+3,note_y_dim,note_x_dim):
                              frame = self.new_note(y_coord+3,x_coord+3,note_y_dim,note_x_dim)
                              put(y_coord,x_coord)
                              while True:


                                   frame_key = screen.getch()
                                   if frame_key in keys:

                                        
                                        frame = self.new_note(y_coord+3,x_coord+3,note_y_dim,note_x_dim,blank=True)
                                        fy_inc, fx_inc = keys[frame_key]
                                        
                                        y_temp = note_y_dim
                                        x_temp = note_x_dim
                                        note_y_dim += fy_inc
                                        note_x_dim += fx_inc
                                        note_y_dim += fx_inc
                                        note_x_dim += fy_inc
                                        
                                        if note_y_dim <10:
                                             note_y_dim = 10
                                        if note_x_dim <10:
                                             note_x_dim = 10
                                        if note_y_dim > y_max:
                                             note_y_dim = y_max
                                        if note_x_dim > x_max:
                                             note_x_dim = x_max
                                        if self.is_clear(y_coord+3,x_coord+3,note_y_dim,note_x_dim):
                                             
                                             frame = self.new_note(y_coord+3,x_coord+3,note_y_dim,note_x_dim)
                                             put(y_coord,x_coord)
                                        else:
                                             self.new_note(y_coord+3,x_coord+3,note_y_dim,note_x_dim)
                                             put(y_coord,x_coord)
                                             
                                        
                                   if frame_key == ord('x'):
                                        break
                                        


                              newpad = ScrollPad(note_y_dim-2,note_x_dim-2,5,2,u_margin=3,l_margin=1,screen=screen)
                              newnote1,newnote2 = fill(newpad.type(frame)[0]), fill(newpad.type(frame)[1])
                              
                              newindex = max(self.added_notes)+1
                              self.added_notes.add(newindex)
                              newindex = '$'+str(newindex)
                              self.import_note(newindex,newnote1,newnote2)
                              self.new_note(y_coord+3,x_coord+3,note_y_dim,note_x_dim,blank=True)
                              
                         

                    elif key == curses.KEY_TAB:
                         next_note = next(self.cycling_through)
                         positions = self.object_dict[next_note]['p']
                         y_coord = positions[0]
                         x_coord = positions[1]

                         
                    elif key == ord('t'):
                         t = ScrollPad(screen=screen)
                         t.type()
                    elif key == ord('m'):
                         moving_object = not moving_object
                    elif key == ord('y'):
                         moving_screen_too = not moving_screen_too
                    elif key == ord('n'):
                         if (self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2))):
                              objects_to_move.add(self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2)))
                    elif key == ord('u'):
                         if (self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2))):  
                              objects_to_move.discard(self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2)))
                    elif key in [ord('b'),curses.KEY_BREAK,curses.KEY_EXIT]:
                         go_on = False
                    elif key == ord('d') and self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2)):
                         self.delete_object(self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2)))
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
                    elif key == ord('f'):
                         cycling = not cycling
                         
                         
                    elif key == ord('p'):
                         stack_dump = True 
##                          while self.note_stack.exists():
##                               self.add_from_stack(y_coord,x_coord)
                              
                              
                    elif key == ord('z'):

                         if multiplier > 1:
                              multiplier -= 1
                    elif key == ord('x'):
                         if multiplier <30:
                              multiplier += 1
     
                    elif key == ord('s'):
                         self.add_from_stack(y_coord,x_coord)
                    elif key == ord('c'):
                         self.size -= 1
                    elif key == ord('v'):
                         self.size += 1
                    
               self.print_to(screen,str(x_coord)+'/'+str(x_total)+' : '+str(y_coord)+'/'+str(y_total)+' '+str(int(y_max/2))+':'+str(int(x_max/2)),y_pos=1,x_pos=2)
                

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
          return  y_coord,x_coord,self.object_dict
              

if __name__ == '__main__':


     a = EmptyMovingWindow()
##     tl = [' '*50]*100
##
##     print('\n'.join(a.new_note(5,5,30,30,tl)))
     a.activate()


     



                         
     


          


          


     


     




                                                                     
