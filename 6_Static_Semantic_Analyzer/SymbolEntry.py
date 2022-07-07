import Token
import Chario
import Scanner
import Parser
import SymbolEntry




class SymbolEntry:

   NONE = 0
   CONST = 1
   PARAM = 2
   PROC = 3
   TYPE = 4
   VAR = 5

   name = ""
   role = 0
   final = -1
   next = None

   def SymbolEntry(self,id,role):
      self.name = id
      self.role = role
      self.next = None


      return self


   def toString(self):
      return "Name: " + self.name + " " + "Role: " + self.roleToString(self)


   def setRole(self,r):
      self.role = r
      if self.final==-1:
         self.final = r
      if self.next is not None:
         self.next.setRole(self.next,r)


   def append(self,entry):

      if (self.next is None):
         self.next = entry
         self.next.next = None
      else:
         self.next.append(entry)


   def roleToString(self,id):
      s = ""

      if id == self.NONE:
         s = "None"
      elif id == self.CONST:
         s = "CONSTANT"
      elif id == self.PARAM:
         s = "PARAMETER"
      elif id == self.PROC:
         s = "PROCEDURE"
      elif id == self.TYPE:
         s = "TYPE"
      elif id == self.VAR:
         s = "VARIABLE"
      else:
         s = "None"

      return s


