class LimitedStack:

     def __init__ (self,max_size=200):

          self.stack = []
          self.max_size = max_size 

     def add (self,item=None):

          self.stack.append(item)

          if len(self.stack) > self.max_size:

               self.stack = self.stack[1:]

     def get (self):

          if self.stack:
               return self.stack.pop()
