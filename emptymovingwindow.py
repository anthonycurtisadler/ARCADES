
import curses
import time
from movingwindow import MovingWindow
from stack import Stack 
from math import sqrt
import winsound 

 
keys = {curses.KEY_LEFT:(0,-1),
        curses.KEY_RIGHT:(0,1),
        curses.KEY_UP:(-1,0),
        curses.KEY_DOWN:(1,0)}



def trace (x):
     #for debugging 

     print({}[x])
     
class EmptyMovingWindow (MovingWindow):

     def __init__ (self,textlist=None,y_dim=1000,x_dim=1000):

 

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

               index,note = popped[0],popped[1]

          else:
               return False
          note, height, width = self.dimensions(note)

          try:
               y_pos,x_pos = self.find_clear(height,width,y_st,x_st)
          except:
               return False
          if isinstance(y_pos,int):

               self.add_object(index,note,y_pos,x_pos)
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

     def move_object (self,index='',vert_inc=0,hor_inc=0):

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
               self.add_object (index,obj['o'],up_bound,left_bound)
               

         

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
                    
               

     def add_object(self,index='',new_object_list=None,y_pos=0,x_pos=0):
          index = str(index)

          new_object_list, height,width = self.dimensions(new_object_list)

          if not self.is_clear(y_pos,x_pos,height,width):
               
               return False

          if index not in self.object_dict:

               for y in range(height):

                    self.textlist[y_pos+y] = self.textlist[y_pos+y][0:x_pos]\
                                             + new_object_list[y]\
                                             + self.textlist[y_pos+y][x_pos+width:]



               self.object_dict[index] = {'o':new_object_list,
                                          'p':(y_pos,x_pos,y_pos+height,x_pos+width),
                                          'l':set(),
                                          'x':None}
               
          else:
               return False
          

     def import_note (self,index,note):
          self.note_stack.add((str(index),note))
          
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
          stack_dump = False
          moving_object = False
          while go_on :
               self.print_to(screen,self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2)),length=10,y_pos=1,x_pos=20)
               self.print_to(screen,', '.join(sorted(self.object_dict.keys())),length=30,y_pos=1,x_pos=40)
               
               if stack_dump:
                    if self.note_stack.exists():
                         self.add_from_stack(y_coord,x_coord)
                         winsound.Beep(440,333)
                         winsound.Beep(880,333)
                         winsound.Beep(440,333)
                    else:
                         if stack_dump and not self.note_stack.exists():
                              stack_dump = False
                    
               else:
                    key = screen.getch()

                    if key in keys.keys():
                         y_inc,x_inc = keys[key][0],keys[key][1]
                         if not moving_object:
                              y_coord += y_inc * multiplier
                              x_coord += x_inc * multiplier
                         if moving_object and self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2)):
                              if y_coord < 5 or y_coord > y_max -5:
                                   y_coord += y_inc * multiplier
                              if x_coord < 5 or x_coord > x_max -5:
                                   x_coord += x_inc * multiplier
                                   
                              self.move_object(self.find_object_in(y_coord+int(y_max/2),x_coord+int(x_max/2)),y_inc*multiplier,x_inc*multiplier)
                                   
                         
                    elif key == ord('m'):
                         moving_object = not moving_object
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
                    
               self.print_to(screen,str(x_coord)+':'+str(y_coord),y_pos=1,x_pos=2)
               

               if y_coord < 0:
                    y_coord = 0
                    winsound.Beep(440,333)
               elif y_coord > y_total - y_max:
                    y_coord = y_total - y_max
                    winsound.Beep(440,333)
               if x_coord < 0:
                    x_coord = 0
                    winsound.Beep(440,333)
               elif x_coord > x_total - x_max:
                    x_coord = x_total - x_max
                    winsound.Beep(440,333)



               put(y_coord,x_coord)
          return  y_coord,x_coord
              

               
          
          
     

          

     

if __name__ == '__main__':

     a = EmptyMovingWindow()
     a.activate()



                         
     


          


          


     


     




                                                                     
