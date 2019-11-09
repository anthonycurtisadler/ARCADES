import copy
import random
from globalconstants import BOX_CHAR


transformation_table = {}
transformation_table['horizontal_rotation'] =  {'v':'v',   #For rotation on horizonal axis
                                               'h':'h',
                                               'lu':'ll', #'┎'
                                               'ru':'rl', #'┒'
                                               'lm':'lm', #'┠'
                                               'rm':'rm', #'┨'
                                               'll':'lu', #'┖'
                                               'rl':'ru', #'┚'
                                               'xl':'xu',  # '┬'
                                               'xu':'xl',  # '┴'
                                               'x':'x'} # '┼'

transformation_table['vertical_rotation'] =  {'v':'v',   #For rotation on horizonal axis
                                               'h':'h',
                                               'lu':'ru', #'┎'
                                               'ru':'lu', #'┒'
                                               'lm':'rm', #'┠'
                                               'rm':'lm', #'┨'
                                               'll':'rl', #'┖'
                                               'rl':'ll', #'┚'
                                               'xl':'xu',  # '┬'
                                               'xu':'xl',  # '┴'
                                               'x':'x'} # '┼'

transformation_table['right_rotation'] =  {'v':'h',   #For rotation on horizonal axis
                                               'h':'v',
                                               'lu':'ru', #'┎'
                                               'ru':'rl', #'┒'
                                               'lm':'xl', #'┠'
                                               'rm':'xu', #'┨'
                                               'll':'lu', #'┖'
                                               'rl':'ll', #'┚'
                                               'xl':'rm',  # '┬'
                                               'xu':'lm',  # '┴'
                                               'x':'x'} # '┼'


for a in ['horizontal_rotation','vertical_rotation','right_rotation']:

     transformation_table[a] = {BOX_CHAR[x]:BOX_CHAR[transformation_table[a][x]]
                                                                         for x in transformation_table[a]}



class DrawingObject:

     def __init__ (self,textlistobject=None,objectlist=None,schema=None):

          self.drawn_object = {} # dictionary in the form
                           # (y,x):(oldchar,newchar)
          if textlistobject:
               self.textlistobject = textlistobject

          if not schema:
               self.schema = {}
          else:
               self.schema = schema
               

          if objectlist:
               for y in range(len(objectlist)):
                    for x in range(len(objectlist[y])):
                         self.schema[(y,x)] = objectlist[y][x]

     def make_schema (self):

          coord_list = sorted(self.drawn_object.keys())
          low_y,low_x = coord_list[0][0],coord_list[0][1]

          for c in coord_list:
               self.schema[c[0]-low_y,c[1]-low_x] = self.drawn_object[c][1]

     def get_schema (self):

          if not self.schema:
               self.make_schema()
          return self.schema

     def enter_superimposed_object (self,
                                    y_coord=0,
                                    x_coord=0,
                                    objectlist=None):

          new_object = {}

          for y in range(len(objectlist)):

               for x in range(len(objectlist[y])):

                    if objectlist[y][x] != ' ':

                         if (y+y_coord,x+x_coord) in self.drawn_object:
                              old_char = self.drawn_object[(y+y_coord,x+x_coord)][0]
                         else:
                              old_char = self.textlistobject[y+y_coord][x+x_coord]

                         new_object[(y+y_coord,x+x_coord)] = (old_char,objectlist[y][x])

          self.drawn_object = new_object 
          

                    
     

     def position_object (self,y_pos,x_pos,from_schema=False):

          if not from_schema:            
               self.make_schema()
          max_y = max([c[0] for c in self.schema])
          max_x = max([c[1] for c in self.schema])

          if y_pos + max_y > len(self.textlistobject) and x_pos + max_x > len(self.textlistobject[y_pos + max_y]):

               return False

          self.drawn_object = {}
          for c in self.schema:
               self.drawn_object[(c[0]+y_pos,c[1]+x_pos)] = (self.textlistobject[c[0]+y_pos][c[1]+x_pos],self.schema[c])

     def select (self,square=True):

          y_min,x_min,y_max,x_max = self.boxed_dimensions()

          objectlist = [x[x_min+1:x_max] for x in self.textlistobject[y_min+1:y_max]]
          self.enter_superimposed_object(y_coord=y_min+1,x_coord=x_min+1,objectlist=objectlist)

     def flip (self,horizontal=False,vertical=False):

          flipped_object = {}
          y_min,x_min,y_max,x_max = self.boxed_dimensions()

          for c in self.drawn_object:

               y_transformed,x_transformed = c[0],c[1]
               old_char_transformed,new_char_transformed = self.drawn_object[c][0],self.drawn_object[c][1]
               
               if horizontal:
                    y_transformed = y_max + y_min - y_transformed
               if vertical:
                    x_transformed = x_max + x_min - x_transformed 
               if (y_transformed,x_transformed) in self.drawn_object:
                    old_char_transformed = self.drawn_object[(y_transformed,x_transformed)][0]
               else:
                    old_char_transformed = self.textlistobject[y_transformed][x_transformed]
               if horizontal:
                    if new_char_transformed in transformation_table['horizontal_rotation']:
                         new_char_transformed = transformation_table['horizontal_rotation'][new_char_transformed]
               if vertical:
                    if new_char_transformed in transformation_table['vertical_rotation']:
                         new_char_transformed = transformation_table['vertical_rotation'][new_char_transformed]
               
               flipped_object[(y_transformed,x_transformed)] = (old_char_transformed,new_char_transformed)
          self.drawn_object = flipped_object

     def rotate (self,degrees=90):

          times = int(degrees/90)
          for t in range(times):

               flipped_object = {}
               y_min,x_min,y_max,x_max = self.boxed_dimensions()

               for c in self.drawn_object:

                    y_transformed,x_transformed = c[0],c[1]
                    old_char_transformed,new_char_transformed = self.drawn_object[c][0],self.drawn_object[c][1]

                    y_transformed = y_transformed - y_min
                    x_transformed  = x_transformed - x_min

                    y_transformed, x_transformed = x_transformed, y_transformed
                    x_transformed = (x_max - x_min) - x_transformed

                    y_transformed += y_min
                    x_transformed += x_min
                    
                    
                    
                    if (y_transformed,x_transformed) in self.drawn_object:
                         old_char_transformed = self.drawn_object[(y_transformed,x_transformed)][0]
                    else:
                         old_char_transformed = self.textlistobject[y_transformed][x_transformed]
                    if new_char_transformed in transformation_table['right_rotation']:
                              new_char_transformed = transformation_table['right_rotation'][new_char_transformed]
                    
                    
                    flipped_object[(y_transformed,x_transformed)] = (old_char_transformed,new_char_transformed)
               self.drawn_object = flipped_object
               

     def stretch (self,x_pos=0,y_pos=0,contracting = False):
          polarity = {True:-1,
                      False:1}[contracting]
          
                              
          if x_pos > 0:

               stretching = []
               for c in self.drawn_object:

                    if c[1] == x_pos:
                         if self.drawn_object[c][1] == BOX_CHAR['h']:
                              stretching.append(c[0])
                         else:
                              return False

               if not contracting:
                    self.move(x_inc=1,min_x=x_pos)
               for temp_y in stretching:
                    if not contracting:
                         self.add(y_pos=temp_y,x_pos=x_pos+1,newchar=BOX_CHAR['h'])
                    else:
                         self.delete(y_pos=temp_y,x_pos=x_pos+1)
               if contracting:
                    self.move(x_inc=-1,min_x=x_pos)
                         

          elif y_pos > 0:

               stretching = []
               for c in self.drawn_object:

                    if c[0] == y_pos:
                         if self.drawn_object[c][1] == BOX_CHAR['v']:
                              stretching.append(c[1])
                         else:
                              return False
               if not contracting:
                    self.move(y_inc=1,min_y=y_pos)
               for temp_x in stretching:
                    if not contracting:
                         self.add(y_pos=y_pos+1,x_pos=temp_x,newchar=BOX_CHAR['v'])
                    else:
                         self.delete(y_pos=y_pos+1,x_pos=temp_x)
               if contracting:
                    self.move(y_inc=-1,min_y=y_pos)
      
     def delete (self,y_pos,x_pos):

          if (y_pos,x_pos) in self.drawn_object:
               del self.drawn_object[(y_pos,x_pos)]
          
     def add (self,y_pos=0,x_pos=0,newchar=' '):

          if 0 <= y_pos < len(self.textlistobject)\
             and 0 <= x_pos < len(self.textlistobject[y_pos]):

               if (y_pos,x_pos) not in self.drawn_object:

                    self.drawn_object[(y_pos,x_pos)] = (self.textlistobject[y_pos][x_pos],
                                                        newchar)

               else:

                    temp_value = self.drawn_object[(y_pos,x_pos)]
                    temp_value = (temp_value[0],newchar)
                    self.drawn_object[(y_pos,x_pos)] = temp_value

     def move (self,y_inc=0,x_inc=0,min_y=-1,max_y=1000000000,min_x=-1,max_x=1000000000):

          ghost = copy.deepcopy (self.drawn_object)

          coord_list = self.drawn_object.keys()

          # to make sure that the search orders the coordinates
          # in the right way so they won't overwrite 
          if y_inc != 0:
               y_polarity = -y_inc/abs(y_inc)
          else:
               y_polarity = 1
          if x_inc != 0:
               x_polarity = -x_inc/abs(x_inc)
          else:
               x_polarity = 1
               
          

          coord_list = sorted(coord_list,key=lambda c:(y_polarity*c[0],x_polarity*c[1]))

          for coord in list(coord_list):

               if min_y < coord[0] < max_y and min_x < coord[1] < max_x:

                    old_value = self.drawn_object[coord]

                    

                    newcoord = coord[0]+y_inc,coord[1]+x_inc
                    if newcoord in ghost:
                         new_value = ghost[newcoord][0],old_value[1]
                    else:
                         new_value = self.textlistobject[newcoord[0]][newcoord[1]],old_value[1]

                    self.drawn_object[newcoord] = new_value
                    del self.drawn_object[coord]

     def contains (self,y_pos=0,x_pos=0):

          return (y_pos,x_pos) in self.drawn_object

     def get_coords (self):

          return [(k_temp,self.drawn_object[k_temp]) for k_temp in self.drawn_object]

     def top_left (self):

          try:

               coord_list = sorted(self.drawn_object.keys())
               low_y,low_x = coord_list[0][0],coord_list[0][1]
               return low_y,low_x
          
          except:
               return 0,0
          
               

     def bottom_right (self):

          try:

               coord_list = sorted(self.drawn_object.keys())
               high_y,high_x = coord_list[-1][0],coord_list[-1][1]
               return high_y,high_x
          
          except:

               try:

                    coord_list = sorted(self.schema.keys())
                    high_y,high_x = coord_list[-1][0],coord_list[-1][1]
                    return high_y,high_x

               except:

                    return 0,0

               

     def boxed_dimensions (self):

          try:

               y_coords = [c[0] for c in self.drawn_object]
               x_coords = [c[1] for c in self.drawn_object]
               
               return min(y_coords),min(x_coords),max(y_coords),max(x_coords)

          except:

               try:

                    y_coords = [c[0] for c in self.schema]
                    x_coords = [c[1] for c in self.schema]
                    
                    return min(y_coords),min(x_coords),max(y_coords),max(x_coords)

               except:

                    return 0,0,0,0

          
          

          



##text = [' '*1000]*1000
##
##obj = DrawingObject (text)
##
##for y in range(10,13):
##     for x in range(30,33):
##          obj.add(y,x,random.choice(['x','y','z']))
##     
##
##
##obj.move(1,0)
##print('111111111')
##
##print(str(obj.drawn_object))
##obj.move(-1,0)
##print('222222222')
##
##print(str(obj.drawn_object))
##obj.move(0,1)
##print('3333333333')
##
##print(str(obj.drawn_object))
##obj.move(0,-1)
##
##print('4444444444')
##
##print(str(obj.drawn_object))
##
##          
##
##          


          
          
               

          

     

     

     

     
