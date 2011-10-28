# Needs Python 2.7 as it uses OrderedDict
# since it needs an ordered dictionary

from collections import OrderedDict

class ATextFileParser:
   """
   Parses a text file into a Parser object. Allows
   update of the text file via the Parser object.
   Full path name should be given as file name argument.
   """
   def __init__(self, fullFileName):
       self.parser = OrderedDict()
       inputfile = open(fullFileName)
       section, key, value = ['','','']
       for line in inputfile:
           if line.strip():
               if line.startswith("["): #this is a section
                   sectiondict = OrderedDict()
                   section = line.strip()[1:-1].strip()
                   self.parser[section] = sectiondict
               else:
                   if line.find(":") > 0: #this is a key-value pair
                       key, value = map(str.strip, line.split(":"))
                       sectiondict[key] = self.__GetNumberFromString(value)
                   elif line.startswith(" "): #this is a continuing line
                       value += "\n" + line.strip("\n")
                       sectiondict[key] = value
    
   def __str__(self):
       return str(self.parser)
   
   def GetValue(self, section, key):
       """
       Gets the value of a key within a section
       """
       return self.parser.get(section, {}).get(key)
       
   def SetValue(self, section, key, value):
       """
       Sets the value of a key within a section
       """
       if section in self.parser:
           if key in self.parser[section]:
               self.parser[section][key] = value
               self.__WriteFile()
               
   def __GetNumberFromString(self, s):
       """
       Returns an int if the string is an int,
       a float if the string is a float,
       or the string itself if its neither
       """
       try:
           num = int(s)
           return num
       except ValueError:
           try:
               num = float(s)
               return num
           except ValueError:
               return s
       
   def __WriteFile(self):
       """
       Writes the Parser object to a file.
       """
       plist = []
       for a in self.parser.iterkeys():
           plist.append("[" + a + "]")
           for key,value in self.parser[a].iteritems():
               plist.append(key + ':' + str(value))
       outputfile = open("output.txt", "w")
       for index,line in enumerate(plist):
           #Print a blank line before a section starts but
           #not for the first section
           if (index != 0) and line.startswith("["):
               outputfile.write("\n")
           #Now print out the line
           outputfile.write(line + "\n")