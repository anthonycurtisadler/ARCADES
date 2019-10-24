import curses
import time
from globalconstants import BOX_CHAR
from itertools import cycle



keys = {curses.KEY_LEFT:(0,-1),
        curses.KEY_RIGHT:(0,1),
        curses.KEY_UP:(-1,0),
        curses.KEY_DOWN:(1,0),
        ord('i'):(-1,0),
        ord('m'):(1,0),
        ord('k'):(0,1),
        ord('j'):(-1,0)}

curses.KEY_TAB = 9



class MovingWindow:

     def __init__ (self, textlist=None):


          if textlist is None:

               test_text = input('?')*1000
          
               self.textlist = [test_text[0:10]*100,test_text[1:11]*100,
                          test_text[2:12]*100,test_text[3:13]*100,
                          test_text[4:14]*100,test_text[5:15]*100,
                          test_text[6:16]*100,test_text[7:17]*100]*30

          else:
               self.textlist = textlist

          self.coordinate_list = []
          for y in range(len(self.textlist)):

               for x, char in enumerate(self.textlist[y]):

                    if char == BOX_CHAR['lu']:

                         self.coordinate_list.append((y,x))
          self.sheet_cycling_through = cycle(self.coordinate_list)
              

     def moving_screen (self,screen,y_coord=0,x_coord=0,b_margin=4,t_margin=3,l_margin=1,r_margin=1,entering=False):

     
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
##               screen.addstr(str(x_dim)+':'+str(y_dim)+':'+str(x_dim_min)+'\n')
               return x_dim, y_dim



          if not self.textlist:
               return False

          x_total,y_total = dimensions()
          multiplier = 1


          y_inc,x_inc = 0,0

          go_on = True

          cycling = False                
          x_max = curses.COLS
          y_max = curses.LINES 
          while go_on :


               key = screen.getch()
               if cycling:
                              
                         if key == curses.KEY_RIGHT:
                              next_note = next(self.sheet_cycling_through)
                              
                              y_coord = next_note[0]
                              x_coord = next_note[1]
                         elif key == curses.KEY_LEFT:
                              for x in range(len(self.coordinate_list)):
                                   next_note = next(self.sheet_cycling_through)
                              y_coord = next_note[0]
                              x_coord = next_note[1]
                         elif key == curses.KEY_UP:
                              self.sheet_cycling_through = cycle(self.coordinate_list)
                              next_note = next(self.sheet_cycling_through)
                              y_coord = next_note[0]
                              x_coord = next_note[1]
                         elif key == curses.KEY_DOWN:
                              self.cycling_through = cycle(self.coordinate_list)
                              for x in range(len(self.coordinate_list)):
                                   next_note = next(self.sheet_cycling_through)
                              
                              y_coord = next_note[0]
                              x_coord = next_note[1]
                              
               elif key in keys.keys():
                    y_inc,x_inc = keys[key][0],keys[key][1]

                    y_coord += y_inc * multiplier
                    x_coord += x_inc * multiplier
                    
               elif key in [ord('b'),curses.KEY_BREAK,curses.KEY_EXIT]:
                    go_on = False
               elif key in [curses.KEY_NPAGE]:
                    y_coord += y_total
               elif key in [curses.KEY_PPAGE]:
                    y_coord -= t_total
               elif key == ord('z'):

                    if multiplier > 1:
                         multiplier -= 1
               elif key == ord('x'):
                    if multiplier <30:
                         multiplier += 1

               elif key == ord('r'):
                    cycling = not cycling
                    



                                        
                                                  
               self.print_to(screen,str(x_coord)+':'+str(y_coord),y_pos=1,x_pos=2)
               

               if y_coord < 0:
                    y_coord = 0
               elif y_coord > y_total - y_max:
                    y_coord = y_total - y_max
               if x_coord < 0:
                    x_coord = 0
               elif x_coord > x_total - x_max:
                    x_coord = x_total - x_max



               put(y_coord,x_coord)
          return y_coord,x_coord, None, None


     def create_frame (self,screen):

          x_max = curses.COLS
          y_max = curses.LINES
          screen.addstr(0,0,BOX_CHAR['lu']+BOX_CHAR['h']*(x_max-2)+BOX_CHAR['ru'])

          screen.addstr(y_max-4,0,BOX_CHAR['lm']+BOX_CHAR['h']*(x_max-2)+BOX_CHAR['rm'])
          screen.addstr(3,0,BOX_CHAR['lm']+BOX_CHAR['h']*(x_max-2)+BOX_CHAR['rm'])
          screen.addstr(y_max-1,0,BOX_CHAR['ll']+BOX_CHAR['h']*(x_max-3))
          for y in range(1,y_max-1):

               screen.addstr(y,0,BOX_CHAR['v'])
               screen.addstr(y,x_max-1,BOX_CHAR['v'])
          window = curses.newwin(3,x_max-2,y_max-3,1)
          return window 

     def print_to (self,screen,text='',length=30,y_pos=0,x_pos=0):

          text = (text + length*' ')[0:length]
          screen.addstr(y_pos,x_pos,text)


     def activate (self,y_max=55,x_max=180,y_pos=0,x_pos=0,entering=False):

          self.screen = curses.initscr()
          curses.resize_term(y_max,x_max)
          self.screen.box()
          
          curses.cbreak()
          self.screen.clear()
          curses.noecho()
          self.screen.keypad(True)

          self.bottom_window = self.create_frame(self.screen)
          
          y_pos,x_pos, object_dict, textlist = self.moving_screen(self.screen,y_coord=y_pos,x_coord=x_pos,entering=entering)                                                       

          curses.nocbreak()
          self.screen.keypad(False)
          curses.echo()
          curses.endwin()
          del self.screen
          return y_pos,x_pos, object_dict, textlist 

     def restore (self):

          curses.nocbreak()
          self.screen.keypad(False)
          curses.echo()
          curses.endwin()
          print('RESTORED')
          return X


if __name__ == '__main__':

     textlist = ['^    ^'*1000,'X    X'*1000]*100

     a = MovingWindow(textlist)
     a.activate()



                         
     


          


          


     


     




                                                                     
