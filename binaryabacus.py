import random 
import time
import math


class BinaryAbacus:

     def __init__ (self,displaydictobject=None,
                   y_min=0,y_max=None,
                   x_min=0,x_max=None,char='█'):

          if displaydictobject is None:
               displaydictobject = {}
          self.displaydictobject = displaydictobject
          if y_max:
               self.y_max = y_max
          else:
               self.y_max = 30
               
          if x_max:
               self.x_max = x_max
          else:
               self.x_max = 30

          self.y_min = y_min
          self.x_min = x_min
          self.l_margin = 3
          self.t_margin = 3
          self.char = char
          self.freq = 350
          self.dur = 100

     def binary_image (self,integer):

          def get_max_power (x):

               power = 0
               while 2**power <= x:
                    power +=1
               return power 
               

          binary_representation = []
          
          for p in reversed(range(0,get_max_power(integer))):
               if 2**p <= integer:
                    integer -= 2**p
                    binary_representation.append(1)
               else:
                    binary_representation.append(0)
          binary_representation.reverse()
          return binary_representation

     
     def place_horizontal (self,binary_image=None,y_start=0,x_start=0,char='█'):


          for position, marked in enumerate(binary_image):
               if marked:    
                    self.displaydictobject[(y_start,x_start+position)] = (char,None,None)
     def place_vertical (self,binary_image=None,y_start=0,x_start=0,char='█'):
          for position, marked in enumerate(binary_image):
               if marked:
                    self.displaydictobject[(y_start+position,x_start)] = (char,None,None)
     def initialize (self,integer1=0,integer2=0,y_start=0,x_start=0):

          image1 = self.binary_image(integer1)
          image2 = self.binary_image(integer2)
          image3 = self.binary_image(integer1*integer2)

          self.place_horizontal(image1,y_start-2,x_start,char='●')
          self.place_vertical(image2,y_start,x_start-1,char='●')

          for position,marked in enumerate(image2):
               if marked:
                    self.place_horizontal(image1,y_start+position+1,x_start+position,char='●')
          self.place_horizontal(image3,self.y_max,x_start)
     

     def delete(self,y_pos,x_pos):

          if (y_pos,x_pos) in self.displaydictobject:
               del self.displaydictobject[(y_pos,x_pos)]
          else:
               print('ERROR')
               return False

     def add(self,y_pos,x_pos):
          if (y_pos,x_pos) not in self.displaydictobject:
               self.displaydictobject[(y_pos,x_pos)] = (self.char,None,None)

     def drop(self,y_pos,x_pos):

          if (y_pos,x_pos) in self.displaydictobject:               
               if (y_pos+1,x_pos) not in self.displaydictobject and y_pos+1 < self.y_max:
                    self.delete(y_pos,x_pos)
                    self.add(y_pos+1,x_pos)
                    return True

          return False 

     def shift(self,y_pos,x_pos):

          if (y_pos,x_pos) in self.displaydictobject:
               if (y_pos-1,x_pos) in self.displaydictobject:
                    
                    if (y_pos,x_pos+1) not in self.displaydictobject:
                         
                              self.delete(y_pos,x_pos)
                              self.delete(y_pos-1,x_pos)
                              self.add(y_pos,x_pos+1)

                              return True
                    elif (y_pos-1,x_pos+1) not in self.displaydictobject:
                         
                              self.delete(y_pos,x_pos)
                              self.delete(y_pos-1,x_pos)
                              self.add(y_pos-1,x_pos+1)

                              return True
          return False

     def cycle(self):
          changed = False

          for c in sorted([x for x in self.displaydictobject if self.t_margin <= x[0] < self.y_max and self.l_margin <= x[1] <= self.x_max],key=lambda x:(-1*x[0],1*x[1])):
               
               y_pos = c[0]
               x_pos = c[1]
               if self.shift(y_pos,x_pos):

                    changed = True


          for c in [x for x in self.displaydictobject if self.t_margin <= x[0] < self.y_max and self.l_margin <= x[1] <= self.x_max]:

               
               y_pos = c[0]
               x_pos = c[1]
               if self.drop(y_pos,x_pos):
                    changed = True 

          
          return changed

     def show(self):

          display = [' '*self.x_max]*self.y_max

          for c in self.displaydictobject:
               display[c[0]] = display[c[0]][0:c[1]]+self.displaydictobject[c][0]+display[c[0]][c[1]+1:]
          for x in display:
               print(x)

          
               
     
     def run(self,maximum=10000000000):

          int1 = random.randrange(1,maximum**4)
          int2 = random.randrange(1,maximum)



          self.initialize(int1,int2,self.t_margin,self.l_margin)

          while self.cycle():
               time.sleep(.1/math.log(maximum))
               yield True,None
          
          result = 0

          for x in range(self.l_margin,self.x_max+1):
               if (self.y_max-1,x) in self.displaydictobject:
                    result += 2**(x-self.l_margin)
          if int1*int2==result:
               yield False,str(int1)+' * '+str(int2)+' = '+str(result)
          else:
               yield False,'['+''.join([str(x) for x in self.binary_image(abs(int1*int2-result))])+']'
          

               

               


          

if __name__ == '__main__':

     a=BinaryAbacus()

     a.run()
          

          

          


          

          
               
               
               
               

     
                    

     

          
          
               
          
               

          
     
