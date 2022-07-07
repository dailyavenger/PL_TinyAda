import Token
import Chario
import Scanner
import Parser
import SymbolEntry


class SymbolTable:

    level = 0
    stack=[]
    c = Chario
    EMPTY_SYMBOL = SymbolEntry.SymbolEntry.SymbolEntry(SymbolEntry.SymbolEntry,"",0)

    table = None

    def SymbolTable(self,ch):
        self.c = ch
        self.reset(self)

        return self


    def reset(self):
        self.level = -1
        self.stack = []


    def enterScope(self):
        self.stack.append([])
        self.level = self.level + 1


    def exitScope(self):
        self.table = self.stack.pop()
        tStr = self.printTable(self,self.table)
        self.level = self.level - 1

        return tStr

    def enterSymbol(self,id,role,value):
        if len(self.stack)-1 >= 0:
            self.table = self.stack[len(self.stack)-1]
        else:
            self.table = self.stack[0]

        contain = 0
        for i in self.table:
            if id == i[0]:
                contain = 1
        if contain == 1:
            print("\n\n [Error Occured] : Already Exist ID",id,end='\n\n')
            return self.EMPTY_SYMBOL

        else:
            s = SymbolEntry.SymbolEntry.SymbolEntry(SymbolEntry.SymbolEntry,id,role)
            self.table.append([id,s,role,value])
            if len(self.stack) - 1 >= 0:
                self.stack[len(self.stack) - 1] = self.table
            else:
                self.stack[0] = self.table
            return s


    def findSymbol(self,id):
        for i in range(0,len(self.stack)):
            self.table = self.stack[len(self.stack) - 1 - i]

            for k in self.table:
                if id == k[0].lower():
                    s = k[1]

                    if s != None:
                        s.name = k[0]
                        s.role = k[2]


                        return s

        print("\n\n [Error Occurred] : Undeclared ID : ",id,end='\n\n')
        return self.EMPTY_SYMBOL



    def printTable(self,table):
        tableStr = ""
        tableStr = tableStr + "\n\n        LEVEL " +str(self.level)+" Symbol Table \n"
        tableStr = tableStr + "------------------------------------\n"
        for s in table:
            tableStr = tableStr + "Name: " + '%-14s' % str(s[0]) + " " + "Role: " + s[1].roleToString(SymbolEntry.SymbolEntry,s[2])+"\n"
        tableStr = tableStr + "------------------------------------\n"

        return tableStr