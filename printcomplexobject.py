def print_complex_object (enter_object,depth=0,node=0,typemarker=None,returnlist=None,displayformat=True,firsttype=None):

     if firsttype is None and not isinstance(enter_object,(list,type,dict,set,str,int,float,bool)):
          firsttype = type(enter_object)
     depth +=1
     typemarker = type(enter_object)
     
     if returnlist is None:
          returnlist = []
     if isinstance(enter_object,(set,tuple)):

          node = 0
          if not displayformat:
               
               returnlist.append('<depth: '+str(depth)+'; node: '+str(node)+ ';'+str(typemarker)+';'+'SET'+'>')
          
          else:
               returnlist.append((depth,node,typemarker,'SET'))
               

          for a in sorted(enter_object):


               node +=1
 
               print_complex_object(a,depth,node,typemarker,returnlist,displayformat)
               

     elif isinstance(enter_object,list):

          node = 0
          if not displayformat:
               returnlist.append('<depth: '+str(depth)+'; node: '+str(node)+ ';'+str(typemarker)+';'+'LIST'+'>')

          else:
               returnlist.append((depth,node,typemarker,'LIST'))

          for a in enter_object:


               node +=1
               print_complex_object(a,depth,node,typemarker,returnlist,displayformat)


     elif type(enter_object) == firsttype or isinstance(enter_object,dict):
          node = 0
          if not displayformat:
               returnlist.append('<depth: '+str(depth)+'; node: '+str(node)+ ';'+str(typemarker)+';'+'DICTIONARY'+'>')
          else:
               returnlist.append((depth,node,typemarker,'DICTIONARY'))
          for a in enter_object:

               node +=1

               print_complex_object(a,depth,node,typemarker,returnlist,displayformat)
               print_complex_object(enter_object[a],depth+1,node,typemarker,returnlist,displayformat)
               
     else:
          if not displayformat:
               returnlist.append('<depth: '+str(depth)+'; node: '+str(node)+ ';'+str(typemarker)+';'+str(enter_object)+'>')
          else:
               returnlist.append((depth,node,typemarker,enter_object))
          
     if not displayformat:    
          return '\n'.join(returnlist)
     else:
          formated_list = [x[0]*'  '+(isinstance(x[3],(int,float))*"'")+str(x[3])+(isinstance(x[3],(int,float))*"'") for x in returnlist]
          return '\n'.join(formated_list)


##while True:
##     
##
##     print(print_complex_object(eval(input('?'))))
##
##
##     
##               

               

               
