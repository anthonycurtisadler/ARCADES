import random
import copy



     

class Conway:

     def __init__ (self,textlistobject=None,displaydictobject=None,cells=None,livechar='█',deadchar=' ',constitute=True,y_min=0,y_max=None,x_min=0,x_max=None,randomizing=True,changing=True):

          if displaydictobject is None:
               displaydictobject = {}
          if textlistobject and not displaydictobject:
               for y_pos, y in enumerate(textlistobject):
                    for x_pos,x in enumerate(y):
                         displaydictobject[(y_pos,x_pos)] = textlistobject[y_pos][x_pos]
                    


          if not y_max:
               self.max_y = max(c[0] for c in displaydictobject)
          else:
               self.max_y = y_max
          if not x_max:
               self.max_x = min(c[1] for c in displaydictobject)
          else:
               self.max_x = x_max
          self.y_min = y_min
          self.x_min = x_min
          self.cells = {}
          if cells and isinstance(cells,dict):
               self.cells = cells           
          self.deadchar = deadchar
          self.random_mode = randomizing
          self.livechar = livechar
          self.old_image = {}
          
          self.odds = {1:(1000,1000),
                       2:(1000,1000),
                       3:(1000,1000),
                       4:(1000,1000)}
          self.displaydictobject = displaydictobject
          self.distance = 1
          self.odd_factor = 100
          self.background = copy.deepcopy(self.displaydictobject)
          self.changing = changing
          if cells and isinstance(cells,(set,list)):
                    for c in cells:

                         
                         if self.get_char(c[0],c[1]) == livechar:
                              self.cells[c] = True
                         elif self.get_char(c[0],c[1]) == deadchar:
                              self.cells[c] = False

                    self.y_min = min([c[0] for c in cells])
                    self.max_y = max([c[0] for c in cells])
                    self.x_min = min([c[1] for c in cells])
                    self.max_x = max([c[1] for c in cells]) 
     
          elif constitute:

               for y in  range(self.y_min,self.max_y):
                    for x in range(self.x_min,self.max_x):
                         
                         if self.get_char(y,x)  == livechar:
                              self.cells[(y,x)] = True
                         elif self.get_char(y,x) == deadchar:
                              self.cells[(y,x)] = False
          for c in self.cells:
               self.old_image[c] = self.get_char(c[0],c[1])

     def get_char (self,y_pos,x_pos):

          if (y_pos,x_pos) in self.displaydictobject:
               return self.displaydictobject[(y_pos,x_pos)][0]
          else:
               return self.deadchar

     def change_odds (self,odds=(920,1000),key=1):
          if isinstance(odds,tuple) and key in [1,2,3,4]:
               self.odds[key] = odds
               
     def change_distance (self,distance=1):
          if 0 <= distance < 5:
               self.distance = distance

     def get_properties (self):
          return self.odds,self.distance

     def burst (self):

          y = random.randrange(self.y_min+5,self.max_y-5)
          x = random.randrange(self.x_min+5,self.max_x-5)

          if self.surrounding_count(self.surrounding_coords((y,x),distance=3)) == 0:

               for c in self.surrounding_coords((y,x),distance=5):
                    self.cells[c] = self.randomize(random.choice([False,True]),(95-int(((abs(c[0]-y))+(abs(c[1]-x)))/2)*20,100))
                   
          
     def randomize (self,boolean,odds=None):
          if self.random_mode:

               if not odds:
                    odds = self.odds
               if random.randint(0,odds[1]+1) <= odds[0]:
                    return boolean
               else:
                    return not boolean
          else:
               return boolean

     def surrounding_coords (self,coord,distance=1):
          y = coord[0]
          x = coord[1]

          surround = []
          for y_off in range(-distance,distance+1):
               for x_off in range(-distance,distance+1):
                    if abs(y_off) + abs(x_off) != 0:
                         if self.y_min <= y+y_off < self.max_y and self.x_min <= x+x_off < self.max_x:
                              surround.append((y+y_off,x+x_off))
          return surround

     def surrounding_count (self,surround=None):

          if not surround:
               surround = []
          count = 0
          for s in surround:
               if s in self.cells:
                    if self.cells[s]:
                         count += 1
          return count

     def get_surrounding (self,coord):
          return self.surrounding_count(self.surrounding_coords(coord,distance=self.distance))

     def cycle_through_cells (self):

          if self.changing:
               if random.choice(range(50)) == 25:
                    self.random_mode = not self.random_mode

          new_cells = {}

          for cell in self.cells:

               if self.cells[cell]:

                    if self.get_surrounding(cell) in [2,3]:
                         new_cells[cell] = self.randomize(True,odds=self.odds[1])

                    elif self.get_surrounding(cell) in [0,1,4,5,6]:
                         new_cells[cell] = self.randomize(False,odds=self.odds[2])

               else:
                    if self.get_surrounding(cell) == 3:
                         new_cells[cell] = self.randomize(True,odds=self.odds[3])

                    else:
                         new_cells[cell] = self.randomize(False,odds=self.odds[4])


          self.cells = new_cells

     def generate (self):

          self.cycle_through_cells()

          for y in range(self.y_min,self.max_y):
               segment = ''               
               for x in range(self.x_min,self.max_x):
                    if (y,x) in self.cells:
                         self.displaydictobject[(y,x)] = ({False:self.deadchar,True:self.livechar}[self.cells[(y,x)]],None,None)
                    else:
                         if (y,x) in self.background:
                              self.displaydictobject[(y,x)] = self.background((y,x))


          return self.displaydictobject

          
if __name__ == '__main__':

     textlistobject =['                    '*10,
                      '                    '*10,
                      '                    '*10,
                      '                    '*10,
                      '                    '*10,
                      '                    '*10,
                      '                    '*10]*5
     
     x = Conway(textlistobject)
     print('\n'.join(textlistobject))

     while True:

          textlistobject = x.generate()
          x.burst()
          print('\n'.join(x.textlistobject))


          input('?')
                    
                    
          

                              
                         
                         
