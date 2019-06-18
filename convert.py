from globalconstants import EOL, UNDERLINE, COLON, COMMA, POUND, ATSIGN, BLANK

class Convert:

     def __init__ (self):

          self.dividor = EOL
          self.sequencekeymark = COLON
          self.entrydividor = COMMA
          self.date_identifier = 'date'
          self.index_identifier = 'index'
          self.keyword_identifier = ['keywords','kw','keyword']
          self.text_identifier = ['text']
          self.pure_identifier = True

     def change (self,entry,flag=''):
          if 'd' in flag:
               self.dividor = entry
          elif 's' in flag:
               self.sequencekeymark = entry
          elif 'e' in flag:
               self.entrydividor = entry
     def show (self):
          return self.dividor,self.sequencekeymark,self.entrydividor
     

     def parse (self,entry):

          if self.dividor == EOL:
               return entry.split(EOL)
          elif UNDERLINE in self.dividor:
               l_mark = self.dividor.split(UNDERLINE)[0]
               r_mark = self.dividor.split(UNDERLINE)[1]

               return [x_temp.split(r_mark)[0]  for x_temp in entry.split(l_mark)[1:]]

     def interpret (self, entry):

          entry_list = self.parse(entry)     
          text = ''
          keys = set()
          for l_temp in entry_list:

               identifier = l_temp.split(self.sequencekeymark)[0]
               if (BLANK not in identifier or not self.pure_identifier) and len(l_temp.split(self.sequencekeymark))>1:
                    identifier = identifier.strip()
                    values = l_temp.split(self.sequencekeymark)[1]
                    
 
                    if identifier in self.text_identifier:
                         text += values + EOL
                    else:
                         if identifier:
                              
                              values = [x_temp.strip() for x_temp in values.split(self.entrydividor)]
                              if identifier in self.keyword_identifier:
                                   keys.update(values)
                              else:
                                   
                                   sequence_mark = ATSIGN
                                   if self.date_identifier  in l_temp:
                                        sequence_mark += POUND
                              
                                   elif self.index_identifier in l_temp:
                                        sequence_mark += UNDERLINE
                                   else:
                                        pass
                                   for v_temp in values:
                                        keys.add(identifier+sequence_mark+v_temp)
               else:
                    text += l_temp + EOL 
                         
          if text:
               return keys,text[0:-1]
          return keys, text


                              
                              
                         
                    

               
               

               


                    

          
