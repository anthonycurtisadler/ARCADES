class CoordLinkedList:
     
     # a linked list object

     def __init__ (self,node=None,y=None,x=None,up=None,down=None,left=None,right=None):

          self.up = up
          self.down = down
          self.left = left
          self.right = right
          if isinstance(node,(list,set,tuple)) and len(node) == 2:
                    self.node = tuple(node)
          elif x and y:
               self.node = (y,x)
          
               

     def receive (self,nodes):
          if not isinstance(nodes,(list,set,tuple)):
               nodes = {nodes}

          for n in nodes:
               if isinstance(n,(tuple)) and len(n) == 2:

                    if n == (self.node[0]-1,self.node[1]):
                         self.up = n
                    elif n == (self.node[0]+1,self.node[1]):
                         self.down = n
                    elif n == (self.node[0],self.node[1]+1):
                         self.right = n
                    elif n == (self.node[0],self.node[1]-1):
                         self.left = n

     def send(self,nodes=None):

          if not nodes:
               nodes = []

          returnlist = []
          if self.down:
               returnlist.append(self.down)
          if self.up:
               returnlist.append(self.up)
          if self.left:
               returnlist.append(self.left)
          if self.right:
               returnlist.append(self.right)
               
          return [x for x in returnlist if x not in nodes]

     

     
                         
               

          
          
