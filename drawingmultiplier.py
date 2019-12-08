
from globalconstants import BOX_CHAR, BOX_CHAR_NORMAL,BOX_CHAR_ROUND,BOX_CHAR_THICK,BOX_CHAR_DOUBLE
import random, itertools


BOX_CHAR_LIST = []

          
     


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

keys = list(transformation_table['horizontal_rotation'].keys())
for a in ['horizontal_rotation','vertical_rotation','right_rotation']:

     for b in [BOX_CHAR_NORMAL,BOX_CHAR_ROUND,BOX_CHAR_THICK,BOX_CHAR_DOUBLE]:
          
          for x in keys:
               transformation_table[a][b[x]] = b[transformation_table[a][x]]


class multiplied_draw:

     """ multiplies the drawing image according to a predefined pattern
     """

     def __init__ (self, window_height=200, window_width=200, seg_height=20, seg_width=20):


          self.window_width = window_width
          self.window_height = window_height
          self.seg_height = seg_height
          self.seg_width = seg_width

          self.segment_dictionary = {}
            # starting y, starting x, y polarity, x polarity
          self.modes = itertools.cycle(range(19))
          self.mode = next(self.modes)
          self.y_divisions = None
          self.x_divisions = None
          
     def show_symmetry_image (self):

          if not self.y_divisions:
               return ['']

          returntext = ''
          for y in range(self.y_divisions):
               for x in range(self.x_divisions):
                    segment = y*self.x_divisions + x
                    if segment in self.segment_dictionary:
                         returntext+={True:'→',
                                      False:'←'}[self.segment_dictionary[segment][2]]
                         returntext+={True:'↑',
                                      False:'↓'}[self.segment_dictionary[segment][3]]
               returntext+='\n'
          return returntext.split('\n')
          


     def return_value (self,y_pos,x_pos,char=None):

          """Returns multiple values for a single value"""

          if not self.segment_dictionary:
               if char:
                    return [(y_pos,x_pos,char)]
               else:
                    return [(y_pos,x_pos)]

          else:
               returnlist = []

               location = self.find_segment (y_pos, x_pos)
               if location:

                    y_start = self.segment_dictionary[location][0]
                    x_start = self.segment_dictionary[location][1]

                    y_off = y_pos - y_start
                    x_off = x_pos - x_start



                    
                    for seg in self.segment_dictionary:


                         y_start = self.segment_dictionary[seg][0]
                         x_start = self.segment_dictionary[seg][1]
                         y_polarity = self.segment_dictionary[seg][2]
                         x_polarity = self.segment_dictionary[seg][3]

                         pol = {True:1,
                                False:-1}
                         mult = {True:0,
                                 False:1}

               

                         return_y_pos = y_start + mult[y_polarity]*self.seg_height + y_off*pol[y_polarity]
                         return_x_pos = x_start + mult[x_polarity]*self.seg_width + x_off*pol[x_polarity]

                         if char:
                              transformed_char = char
                              if not y_polarity:
                                   transformed_char = transformation_table['horizontal_rotation'][transformed_char]
                                   
                              if not x_polarity:
                                   transformed_char = transformation_table['vertical_rotation'][transformed_char]

                              returnlist.append((int(return_y_pos),int(return_x_pos),transformed_char))
                         else:
                              returnlist.append((int(return_y_pos),int(return_x_pos)))
                              

                    return [c for c in returnlist if 0 <= c[0] < self.window_height and 0 <= c[1] < self.window_width]
               else:
                    if char:
                         return [(y_pos,x_pos,char)]
                    else:
                         return [(y_pos,x_pos)]
                   

     def find_segment (self, y_pos, x_pos):

          """Identifies the segment to which the coordinates belong"""

          for seg in self.segment_dictionary:

               try:

                    y_start = self.segment_dictionary[seg][0]
                    x_start = self.segment_dictionary[seg][1]

                    if y_start <= y_pos < y_start + self.seg_height and \
                       x_start <= x_pos < x_start + self.seg_width:

                         return seg
               except:
                    return None

     def get_symmetry (self,y,x):

          if self.mode == 0:
               return (True,True)          
          elif self.mode == 1:
               return (False,False)
          elif self.mode == 2:
               return (True,False)
          elif self.mode == 3:
               return (False,True)
          elif self.mode == 4:
               return (random.choice([True,False]), random.choice([True,False]))
          elif self.mode == 5:
               if y < int(self.y_divisions/2):
                    return True, True
               else:
                    return False, False
          elif self.mode == 6:
               if y < int(self.y_divisions/2):
                    return True, False
               else:
                    return False, True
          elif self.mode == 7:
               if x < int(self.x_divisions/2):
                    return True, True
               else:
                    return False, False
          elif self.mode == 7:
               if x < int(self.x_divisions/2):
                    return True, False
               else:
                    return False, True
          elif self.mode == 8:
               return (self.y_divisions%2==0,self.x_divisions%2==0)
          elif self.mode == 9:
               return (not self.x_divisions%2==0,not self.x_divisions%2==0)
          elif self.mode == 10:
               return (not self.y_divisions%2==0,self.x_divisions%2==0)
          elif self.mode == 11:
               return (self.y_divisions%2==0,not self.x_divisions%2==0)
          elif self.mode == 12:
               return (y < int(self.y_divisions/2),x < int(self.x_divisions/2))
          elif self.mode == 13:
               return (not y < int(self.y_divisions/2),not x < int(self.x_divisions/2))
          elif self.mode == 14:
               return (y < int(self.y_divisions/2),not x < int(self.x_divisions/2))
          elif self.mode == 15:
               return (not y < int(self.y_divisions/2),x < int(self.x_divisions/2))
          elif self.mode == 16:
               return (self.y_divisions%3==0,self.x_divisions%3==0)
          elif self.mode == 17:
               return (not self.x_divisions%3==0,not self.x_divisions%3==0)
          elif self.mode == 17:
               return (self.y_divisions%5==0,self.x_divisions%5==0)
          elif self.mode == 18:
               return (not self.x_divisions%7==0,not self.x_divisions%7==0)
                                        
               
     def switch_mode (self):

          self.mode = next(self.modes)
          return self.mode 
          
               

     def divide (self, y_divisions=1, x_divisions=1):

          """divides the display field into mirrors of each other with various symmetries"""
          
          self.y_divisions = y_divisions
          self.x_divisions = x_divisions
          y_remainder = self.window_height % y_divisions
          x_remainder = self.window_width % x_divisions

          if x_remainder % 2 == 0:
               left_off = right_off = x_remainder/2
          else:
               left_off = (x_remainder-1)/2
               right_off = (x_remainder-1)/2 + 1

          if y_remainder % 2 == 0:
               top_off = bottom_off = y_remainder/2
          else:
               top_off = (y_remainder-1)/2
               bottom_off = (y_remainder-1)/2 + 1
               

          y_seg_length = (self.window_height - y_remainder)/y_divisions
          x_seg_length = (self.window_width - x_remainder)/x_divisions
          self.seg_height = y_seg_length
          self.seg_width = x_seg_length

          self.segment_dictionary = {}
          counter = 0 
          for y in range(y_divisions):
               for x in range(x_divisions):

                    symmetry = self.get_symmetry(y,x)

                    self.segment_dictionary[counter] = (top_off+y*y_seg_length,
                                                        left_off+x*x_seg_length,
                                                        symmetry[0],
                                                        symmetry[1])
                    counter += 1
          

     

          

          
     

               

                    

                    

               

     
