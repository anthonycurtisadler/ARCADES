## Date object for a timeline ##

## AD BC  Year Month Day Hour Minute Second 

def compare (list_a,list_b):

     if len(list_a) > len(list_b):

          list_b += [None]*(len(list_a)-len(list_b))
     elif len(list_b) > len(list_a):

          list_a += [None]*(len(list_b)-len(list_a))

     returnstr = []
     for x in range(len(list_a)):
          if not list_a[x] and list_b[x]:
               returnstr.append('b')
          elif not list_b[x] and list_a[x]:
               returnstr.append('a')
          elif not list_a[x] and not list_b[x]:
               returnstr.append('=')
          elif list_a[x] < list_b[x]:
               returnstr.append('a')
          elif list_a[x] > list_b[x]:
               returnstr.append('b')
          else:
               returnstr.append('=')

     returnstr = ''.join(returnstr)
     returnstr = returnstr.lstrip('=')
     if not returnstr:
          return '='
     return returnstr[0]
               
          

class TimeLineDateTime:

     def __init__ (self,datetime=None,bc=None,century=None,decade=None,year=None,month=None,day=None,hour=None,minute=None,second=None,fromto=None):

          try:
               self.datetime = [None,None,None,None,None,None,None,None]
               if isinstance(datetime,str):
                    if datetime.startswith('-'):
                         bc=True
                         datetime = datetime[1:]
                    else:
                         bc=False

                    if ' ' in datetime:
                         self.datetime = datetime.split(' ')[0].split('-')+datetime.split(' ')[1].split(':')
                    else:
                         self.datetime = datetime.split('-')
                    self.datetime = [int(x) for x in self.datetime] + [None,None,None,None,None,None]
                    self.datetime = self.datetime[0:1]+[None,None]+self.datetime[1:]
                    self.datetime = self.datetime[0:8]
               year = self.datetime[0]
               self.datetime[0] = 0
               self.datetime[1] = 0
               if year is not None:
                    if abs(year) > 10:
                         century = int((year - (year % 100))/100)
                         decade = int(((year - century * 100) - (year % 10)) / 10)
                         if bc or year < 0:
                              century = century+1
                         year = year % 10
                    else:
                         century = 0
                         decade = 0
                         if bc or year < 0:
                              century = century+1
                         year = year
                    if bc or year <0:
                         print('d')
                         century = -century
                         print(century)
                         
               if century is not None:
                    self.datetime[0] = century

               if decade is not None:
                    self.datetime[1] = decade
               if year is not None:
                    self.datetime[2] = year             
               if month is not None:
                    self.datetime[3] = month
               if day is not None:
                    self.datetime[4] = day
               if hour is not None:
                    self.datetime[5] = hour
               if minute is not None:
                    self.datetime[6] = minute
               if second is not None:
                    self.datetime[7] = second
               if fromto is True:
                    self.datetime = self.replace_with(self.datetime,(None,-1,-1,0,0,-1,-1,-1))
               if fromto is False:
                    self.datetime = self.replace_with(self.datetime,(None,101,11,13,32,24,61,61))
               if not self.valid(self.datetime):
                    self.datetime = [None,None,None,None,None,None,None,None]
          except:
               self.datetime = [None,None,None,None,None,None,None,None]

     def replace_with (self,enterlist=None,replacetuple=None):

          """ replaces None objects in enterlist with member of replacelist """

          returnlist = list(enterlist)

          for counter,x in enumerate(enterlist):

               if x is None:
                    try:
                         returnlist[counter] = replacelist[counter]
                    except:
                         return False
          return returnlist 
          
     def valid (self,datetime):

          if not isinstance(datetime,list):
               return False
          if not (0 <= len(datetime) < 9):
               return False
          if datetime[1] and not (-1 <= datetime[1] <=101):
               return False
          if datetime[2] and not (-1 <= datetime[2] <11):
               return False
          if datetime[3] and not (0 <= datetime[3] <= 13):
               return False
          if datetime[4] and not (0 <= datetime[4] <= 32):
               return False
          if datetime[5] and not (-1 <= datetime[5] <= 24):
               return False
          if datetime[6] and not (-1 <= datetime[6] <= 61):
               return False
          if datetime[7] and not (-1 <= datetime[7] <= 61):
               return False
          return True



     def __str__(self):

          try:

               bc = False
               datetime_temp = list(self.datetime)

               suffixes = 'XX-- ::'
               if datetime_temp[0]<0:

                    datetime_temp[0] = abs(self.datetime[0]+1)
                    bc = True

               returnstr = bc*'-'+str(datetime_temp[0])
               datetime_temp = datetime_temp + [None]
               for counter,x in enumerate(datetime_temp[1:datetime_temp.index(None)]):
                    returnstr += suffixes[counter].replace('X','')
                    returnstr += str(x)
               return returnstr
          except:
               return ''

     def __eq__(self,other):

          try:

               return self.datetime == other.datetime
          except:

               return compare(self.datetime,other.datetime) in ['=']

     
     def __ne__(self,other):

          try:

               return self.datetime != other.datetime
          except:

               return compare(self.datetime,other.datetime) not in ['=']
     
     def __lt__(self,other):

          try:
               return self.datetime < other.datetime
          except:

               return compare(self.datetime,other.datetime) in ['a']
     
     def __gt__(self,other):

          try:
               return self.datetime > other.datetime
          except:

               return compare(self.datetime,other.datetime) in ['b']
     
     def __le__(self,other):

          try:
               return self.datetime <= other.datetime
          except:
               return compare(self.datetime,other.datetime) in ['=','a']
     
     def __ge__(self,other):

          try:
               return self.datetime >= other.datetime
          except:
               return compare(self.datetime,other.datetime) in ['=','b']
     def exists (self):

          for x in self.datetime:
               if not x is None:
                    return True
          return False 

          

##while True:
##
##     a = TimeLineDateTime(datetime=input('?'))
##     b = TimeLineDateTime(datetime=input('??'))
##     
##     print(str(a))
##     print(str(b))
##     print('a > b',a>b)
##     print('a < b',a<b)
##     print('a = b',a==b)
##     print('a <= b',a<=b)
##     print('a >= b',a>=b)
##
##     print(a.exists())
##     print(b.exists())






     


