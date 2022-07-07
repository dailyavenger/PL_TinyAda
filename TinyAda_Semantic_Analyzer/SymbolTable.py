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
        self.stack = [] #new Stack < Map < String, SymbolEntry >> ();


    def enterScope(self):
        self.stack.append([])
        self.level = self.level + 1


    def exitScope(self):


        self.table = self.stack.pop()


        self.printTable(self,self.table)
        self.level = self.level - 1

    # 선언하기
    def enterSymbol(self,id,role,value):
        if len(self.stack)-1 >= 0:
            self.table = self.stack[len(self.stack)-1]
        else:
            self.table = self.stack[0]



        #print(self.table)
        contain = 0
        for i in self.table:
            if id == i[0]:
                contain = 1
        if contain == 1:
            print("\n>> Error Occured : Already Exist ID",id,end='\n')
            return self.EMPTY_SYMBOL

        else:

            s = SymbolEntry.SymbolEntry.SymbolEntry(SymbolEntry.SymbolEntry,id,role)

            self.table.append([id,s,role,value])

            if len(self.stack) - 1 >= 0:
                self.stack[len(self.stack) - 1] = self.table
            else:
                self.stack[0] = self.table

            return s


    # 선언여부 찾기
    def findSymbol(self,id):

        #print("\nfs",id)


        for i in range(0,len(self.stack)):
            self.table = self.stack[len(self.stack) - 1 - i]

            #print(self.table)
            for k in self.table:
                if id == k[0].lower():
                    s = k[1]

                    if s != None:
                        s.name = k[0]
                        s.role = k[2]


                        return s

        #self.c.reportErrors()
        print("\n>> Error Ocurred : Undeclared ID : ",id,end='\n')
        return self.EMPTY_SYMBOL



    def printTable(self,table):

        #print(self.table)
        print("\n\n        LEVEL " +str(self.level)+" Symbol Table ")
        print("------------------------------------")
        for s in table:

            #print(s[1].role)

            print("Name: " + '%-14s' % str(s[0]) + " " + "Role: " + s[1].roleToString(SymbolEntry.SymbolEntry,s[2]))

        print("------------------------------------")