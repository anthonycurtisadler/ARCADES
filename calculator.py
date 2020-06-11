""" A SIMPLE SCIENTIFIC CALCULATOR, LEVERING THE MATH CLASS,
 WITH UNLIMITED DEFINABLE VARIABLES, A RUNNING LOG OF ENTRIES"""

import math

class register:

     """ Class for storing and accessing variables and constants"""

     def __init__ (self):

         self.variables = {}
         self.constants = {'pi':math.pi,
                           'e':math.e,
                           'tau':math.tau,
                           'inf':math.inf,
                           'nan':math.nan}

     def get (self, name):

          if name in self.variables:
               return self.variables[name]
          if name in self.constants:
               return self.constants[name]
     def set (self, name,value):
          if name not in self.constants:
               self.variables[name] = value

     def contains (self,name):
          return name in self.variables or name in self.constants

     


class Calculator:

     def __init__(self):

          def gcd (x,y):

               return math.gcd(int(x),int(y))


          self.operations = ['+','-','*','/','^','%']
              # basic operators in order of evaluation
          # functions imported from math
          self.functions = {'fact':(math.factorial,1,1),
                       'abs':(math.fabs,1,1),
                       'floor':(math.floor,1,1),
                       'fmod':(math.floor,2,2),
                       'frexp':(math.frexp,1,1),
                       'gcd':(gcd,2,2),
                       'remainder':(math.remainder,2,2),
                       'trunc':(math.trunc,1,1),
                       'exp':(math.exp,1,1),
                       'expm1':(math.expm1,1,1),
                       'logn':(math.log,1,1),
                       'logx':(math.log,2,2),
                       'log1p':(math.log1p,1,1),
                       'log2':(math.log2,1,1),
                       'log10':(math.log10,1,1),
                       'pow':(math.pow,2,2),
                       'sum':(math.fsum,1,10000),
                       'acos':(math.acos,1,1),
                       'asin':(math.asin,1,1),
                       'atan':(math.atan,1,1),
                       'atan2':(math.atan2,2,2),
                       'cos':(math.cos,1,1),
                       'hypot':(math.hypot,2,10000),
                       'sin':(math.sin,1,1),
                       'tan':(math.tan,1,1),
                       'degrees':(math.degrees,1,1),
                       'radians':(math.radians,1,1),
                       'acosh':(math.acosh,1,1),
                       'asinh':(math.asinh,1,1),
                       'atanh':(math.atanh,1,1),
                       'cosh':(math.cosh,1,1),
                       'sinh':(math.sinh,1,1),
                       'tanh':(math.tanh,1,1),
                       'erf':(math.erf,1,1),
                       'erfc':(math.erfc,1,1),
                       'gamma':(math.gamma,1,1),
                       'lgamma':(math.lgamma,1,1),
                       'neg':(lambda x:-x,1,1)}
          
          self.current_register = register()
               # Initiate register for variables

          self.SCRIPT ="""           A SIMPLE SCIENTIFIC CALCULATOR
                         by
                Anthony Curtis Adler

         OPERATORS = +,/,-,*,%(mod),^(power), ()
         FUNCTIONS abs,floor,fmod,frexp,gcd,remainder,
         trunc,exp,expml,logn,logx,log1p,log2,log10,
         power,sum,acos,asin,atan,atan2,cos,hypot,
         sin,tan,degrees,radians,acost,asinh,atanh,cosh,
         sing,tanh,erf,erfc,gamma,lgamma,neg

         CONSTANTS pi, e, tau, inf, nan

         Any alphanumeric phrase can serve as a variable.
         To return an entry from the log, type @line@.

         ALL to show the log
"""
          


     def calculate (self,phrase):

          """Core routine for parsing and evaluating phrase"""


          def bracketed (phrase):

               """Returns TRUE if <phrase> is encompassed by a left bracket and a right bracket
               at the same hierarchical level"""

               level = 0
               left_point = None
               right_point = None
               

               for count,char in enumerate(phrase):

                    if char == '(':
                         if level == 0:
                              left_point = count
                         level+=1
                    if char == ')':
                         level-=1
                         if level == 0:
                              right_point = count
               if not (left_point is None)  and (not right_point is None) and left_point == 0 and right_point == len(phrase)-1:
                    return True
               return False 

          def is_function(phrase):

               """Tests to see if a phrase begins with a predefined function,
               in which case it returns information about the iarity of function"""
               
               
               for x in self.functions.keys():

                    if len(x) < len(phrase) and phrase[0:len(x)] == x:
                         if bracketed(phrase[len(x):]):
                              if self.functions[x][1]-1 <= phrase.count(',') <= self.functions[x][2]-1:
                                   return x, self.functions[x][0], self.functions[x][2], phrase[len(x):]
               else:
                    return False,False,False,False 
          

          def all_simple (phrase):

               """Tests if a phrase is a simple string representing an expression, rather than an operation"""


               for x in phrase:
                    if x not in self.operations and not isinstance(x,(int,float)):
                         return False
               return True
          
          def parse (phrase):

               """Parses and analzes the phrase"""

               if isinstance(phrase,str):
                    # If the phrase is a string
                    phrase = phrase.strip()

                    func_name, func, iarity, func_phrase = is_function(phrase)
                         # tests is it is function; otherwise the values are false.
                    
                    

                    if func_name:
                         if iarity == 1:
                              # If the function accepts one value
                              return func(parse(func_phrase))
                         if iarity == 2:
                              # Two values 
                              func_phrase = func_phrase[1:-1]
                              term1,term2 = func_phrase.split(',')[0],func_phrase.split(',')[1]
                              return func(parse(term1),parse(term2))
                         if iarity > 2:
                              # A list of values 
                              func_phrase = func_phrase[1:-1]
                              return func([parse(x) for x in func_phrase.split(',')])
                    elif phrase[0] == '-' and bracketed(phrase[1:]):
                         # Translates negative sign (as opposed to operators) into corresponding function 
                         return -parse(phrase[2:-1])


                    elif bracketed(phrase):
                         # removes top-level bracket
                         phrase = phrase[1:-1]
                         return parse(phrase)
                    elif phrase in self.operations:
                         return phrase
                    elif self.current_register.contains(phrase):
                         # for variables and constants 
                         return self.current_register.get(phrase)
                    elif phrase and phrase[0]=='@' and phrase[-1]=='@':
                         # to retrieve values from the log 
                         index = int(parse(phrase[1:-1]))
                         if 0<= index <= len(self.lines):
                              return self.lines[index][0]
                    else:
                                        
                         phrase = list(phrase)
                           #phrase is converted to a list to allowing indexical assignments
                         operation_sequence = []
                         level = 0
                         for counter, x in enumerate(phrase):

                              # Search for operators that are not enclosed in parantheses 

                              if x == '(':
                                   level +=1

                              if x == ')':
                                   level -=1
                              if level == 0:
                                   if counter<len(phrase)-1:
                                        if phrase[counter+1] in self.operations:
                                             # If an operator is found, surround it with pound signs
                                             phrase[counter+1] = '#'+phrase[counter+1]+'#'
                                             if phrase[counter+2] in self.operations:
                                                  phrase[counter+2] = '~'
                                                  # For a minus sign that is not an operator

                                             
                         phrase = ''.join(phrase).replace('~','-').split('#')
                           # Split the phrase into expressions linked by operators 
                         newphrase = []
                         for x in phrase:
                              # a clumsy way to distinction between numerical values, and string operators
                              try:
                                   newphrase.append(float(x))
                              except:
                                   newphrase.append(x)
                         phrase = newphrase

                         return parse(phrase)
                         
                    

               if isinstance(phrase,list):
                    # If the phrase has already been parsed into a list 
                    if len(phrase) == 1:
                         return (parse(phrase[0]))
                    if all_simple(phrase):
                         # If every value in the phrase list has been reduced to
                         # a numerical value or an operator 

                        

                         for operation in self.operations:

                              #In order to preserve the correct order of operations,
                              #the operations are analyzed in succession

                              while operation in phrase:

                                   #This repeat as long as the operation is in the phrase,
                                   #since with each pass it only "reduced"
                                   #expression/operator/expression triplet
                                   

                                   newlist = [] # For the result of each pass through the list.
                                   lastvalue = None
                                   counter = 0
                                   stop = False
                                   while counter < len(phrase) and not stop:
                 
                                        if counter < len(phrase)-2:
                                             a = phrase[counter]
                                             op = phrase[counter+1]
                                             b = phrase[counter+2]
                                               #take a triplet of values from the list

                                             if op == operation:
                                                  # if an operator is found, reduced the triplet, and
                                                  # then add the reduced value, together with the rest
                                                  # of the list to the 
                                                  if operation == '*':
                                                       c = a*b
                                                  elif operation == '+':
                                                       c = a+b
                                                  elif operation == '/':
                                                       c = a/b
                                                  elif operation == '^':
                                                       c = a**b
                                                  elif operation == '%':
                                                       c = a % b
                                                  elif operation == '-':
                                                       c = a - b
                                                  newlist.append(c)
                                                  newlist += phrase[counter+3:] 
                                                  stop = True
                                             else:
                                                  newlist.append(a)
                                        else:
                                             # otherwise, just add the text value to the new list
                                             newlist.append(phrase[counter])
                                        counter +=1 
                                             
                                   
                                   phrase = newlist



                                   
                         
                    else:
                        # if the list is not yet simple, return a new list after parsing each element.
                        phrase = [parse(x) for x in phrase]
                    return parse(phrase)

               if isinstance(phrase,(int,float)):
                    # if a numerical value, stop the recursion
                    return phrase 

          return parse(phrase)


     def show_line (self,counter,x):

          return str(counter)+':'+str(x[1])+(20-len(str(x[1])))*' '+'|'+x[0]
     

     def show_all (self):

          #Shows all the lines in the log

          for counter, x in enumerate(self.lines):
               print(self.show_line(counter,x))
               
     def clear (self):
          self.lines = [('',0)]
          self.counter = 0

     def delete(self,x):

          if '-' not in x:
               x = int(x)
               if 0 <= x < len(self.lines):
                    indexes = [x]
          else:
               x_from, x_to = int(x.split('-')[0]),int(x.split('-')[1])
               if 0 <= x_from < x_to <= len(self.lines):
                    indexes = range(x_from,x_to+1)
          if indexes:
               for ind in indexes:

                    print('DELETED/',self.show_line(ind,self.lines[ind]))
                    self.lines[ind] = None
          self.lines = [x for x in self.lines if x]

          
          

                    


     def console (self):

          # The console operating the calculator 

          self.commands = {'ALL':self.show_all,
                           'CLEAR':self.clear}
          self.one_commands = {'DELETE':self.delete}
          

          self.counter = 0
          self.show_counter = 0
          self.lines = [('',0)]
          print(self.SCRIPT)
          while True:

               

               
               query = input('?')
               if '---' in query:
                    query = query.replace('---','-')
                         #eliminate redundant minus signs

               if query in self.commands:
                    self.commands[query]()
                         #for system commands
               elif query.split(':')[0] in self.one_commands:
                    if ':' in query:
                         self.one_commands[query.split(':')[0]](query.split(':')[1])
               elif query == 'QUIT':
                         #to quit
                    break
               elif query[0:5]=='GOTO:':
                    line = int(query.split(':')[1])
                    if 0 <= line <len(self.lines):
                         self.counter = line
                    else:
                         print('INVALID VALUE')
               
               else:
                    if query:
                         self.counter +=1 
                         if query[0] in self.operations:
                              query = str(self.lines[self.counter-1][1])+query
                                 # if no initial value, perform operation on previous value


                         if '=' in query:
                                 # To define a variable (=subject)
                              subject, predicate = query.split('=')
                              subject = subject.strip()
                         else:
                                 # If not variable = subject 
                              predicate = query
                              subject = ''
                         try:
                              value = self.calculate(predicate)
                         except:
                              value = 'ERROR'
                         if subject:
                                # if a variable has been given, define its value 
                              if not isinstance(value,str):
                                   # to make sure that an ERROR message is not recorded as a value 
                                   self.current_register.set(subject,value)
                         else:
                               # If the counter is not yet at the end of the log 
                              if self.counter < len(self.lines):
                                   self.lines[self.counter] = (query,value)
                              else:
                                   # Otherwise just append query and result-value to log 
                                   self.lines.append((query,value))
                         print(' '+subject+' '*(24-len(subject))+'|',predicate,'=',value)
                    else:
                         if self.show_counter < len(self.lines)-1:
                              self.show_counter+=1
                         print (self.show_counter,':',str(self.lines[self.show_counter][1])+(20-len(str(self.lines[self.show_counter][1])))*' ','|',self.lines[self.show_counter][0])
                         if self.show_counter == len(self.lines)-1:
                              self.show_counter = 0
                    if self.counter > len(self.lines)-1:
                         self.counter = len(self.lines)-1
                         
                         
                         

if __name__ == '__main__':            
     calc = Calculator()
     calc.console()
                                        
                    
