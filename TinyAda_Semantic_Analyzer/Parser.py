#parser
import Token
import Scanner
import Chario
import sys
import SymbolTable
import SymbolEntry

class Parser:

    c = Chario.Chario()
    s = []
    s_index = 0
    tok = ""
    word = []
    w_index = 0
    w = ""
    addOp = set()
    mulOp = set()
    relOp = set()
    dec = set()
    stmt = set()


    table = [] #
    left = set() #
    right = set() #

    bigL = []

    pTable = []



    def __init__(self):
        self.c = Chario.Chario.chario(Chario.Chario())
        self.s = Scanner.Scanner.tokenize(Scanner.Scanner(),self.c)
        self.initHandles()

        ##
        self.initTable()

        self.tok = self.s[self.s_index]
        self.word = Scanner.Scanner.wordRet(Scanner.Scanner(),self.c)
        self.w = self.word[self.w_index]


    def initHandles(self):
        self.addOp.add(Token.Token.PLUS)
        self.addOp.add(Token.Token.MINUS)

        self.mulOp.add(Token.Token.MUL)
        self.mulOp.add(Token.Token.DIV)
        self.mulOp.add(Token.Token.MOD)

        self.relOp.add(Token.Token.EQ)
        self.relOp.add(Token.Token.NE)
        self.relOp.add(Token.Token.LE)
        self.relOp.add(Token.Token.GE)
        self.relOp.add(Token.Token.LT)
        self.relOp.add(Token.Token.GT)

        self.dec.add(Token.Token.TYPE)
        self.dec.add(Token.Token.ID)
        self.dec.add(Token.Token.PROC)

        self.stmt.add(Token.Token.EXIT)
        self.stmt.add(Token.Token.ID)
        self.stmt.add(Token.Token.IF)
        self.stmt.add(Token.Token.LOOP)
        self.stmt.add(Token.Token.NULL)
        self.stmt.add(Token.Token.WHILE)

        #
        self.left.add(SymbolEntry.SymbolEntry.PARAM)
        self.left.add(SymbolEntry.SymbolEntry.VAR)

        self.right.add(SymbolEntry.SymbolEntry.CONST)
        self.right.add(SymbolEntry.SymbolEntry.PARAM)
        self.right.add(SymbolEntry.SymbolEntry.VAR)


    #
    def acceptRole(self,s,expected,msg):

        #print("\nrole : ",s.name," ",s.role," ",expected)

        try:

            dic = False
            for i in expected:

                if s.role == i:

                    dic = True
                    break

            if not dic:
                print("Role Error")
        except:
            if s.role != SymbolEntry.SymbolEntry.NONE and s.role != expected:
                # self.c.reportErrors()
                print("Role Error")




    # table initiate
    def initTable(self):
        # construct table
        self.table = SymbolTable.SymbolTable.SymbolTable(SymbolTable.SymbolTable,self.c)
        self.table.enterScope(self.table)
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"BOOLEAN",SymbolEntry.SymbolEntry.TYPE,"BOOLEAN")
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"CHAR",SymbolEntry.SymbolEntry.TYPE,"CHAR")
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"INTEGER",SymbolEntry.SymbolEntry.TYPE,"INTEGER")
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"TRUE",SymbolEntry.SymbolEntry.CONST,"TRUE")
        entry = self.table.enterSymbol(SymbolTable.SymbolTable,"FALSE",SymbolEntry.SymbolEntry.CONST,"FALSE")





    #  e n t
    def enterId(self,role,value):


        entry = SymbolEntry.SymbolEntry.SymbolEntry(SymbolEntry.SymbolEntry,"",role)

        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ID):
            #print(self.w)
            entry = self.table.enterSymbol(SymbolTable.SymbolTable, self.w,role,value) ## ???

        else:
            self.fatalError("identifier expected 1")


        self.nextToken()
        return entry


   # f i n
    def findId(self):
        entry = SymbolEntry.SymbolEntry.SymbolEntry(SymbolEntry.SymbolEntry,"",0)

        #print(self.w," ",self.tok)
        #print(Token.Token.codeToStr(Token.Token,Token.Token.ID))
        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ID):
            #print(self.table)

            entry = self.table.findSymbol(self.table,self.w) ## ???

        else:
            self.fatalError("identifier expected 2")
        self.nextToken()
        return entry



    def accept(self,expected,msg):
        if self.tok != Token.Token.codeToStr(Token.Token,expected):
            self.fatalError(msg)
        self.nextToken()


    def fatalError(self,msg):
        print(msg)
        sys.exit()
        raise Exception("Fatal error")


    def nextToken(self):
        if (self.w == ''):
            print(" ",end='') # checking finished
        else:
            print(self.w, end='')
        self.s_index = self.s_index + 1
        if len(self.s) <= self.s_index:
            self.tok = Token.Token.codeToStr(Token.Token, Token.Token.EOF)
        else:
            self.tok = self.s[self.s_index]

        self.w_index = self.w_index + 1

        if len(self.word) <= self.w_index:
            self.w = ''
        else:
            self.w = self.word[self.w_index]

        while (self.tok == 'WHITESPACE' or self.tok == 'NEWLINE'):
            if(self.w==''):
                print("\nChecking Finished")
            else:
                print(self.w,end='')
            self.s_index = self.s_index + 1
            if len(self.s) <= self.s_index:
                self.tok = Token.Token.codeToStr(Token.Token, Token.Token.EOF)
            else:
                self.tok = self.s[self.s_index]
            self.w_index = self.w_index + 1
            if len(self.word) <= self.w_index:
                self.w = ''
            else:
                self.w = self.word[self.w_index]


    def parse(self):


        self.subprogramBody()

        self.accept(Token.Token.EOF,"extra symbols after logical end of program")

        self.table.exitScope(self.table)

        self.printAll()


    def printAll(self):

        if len(self.pTable) > 0:
            print("\n\nPrint Function Operated")
            print("------------------------------------")
            for i in self.pTable:
                print(i)
            print("------------------------------------")



    def subprogramBody(self):
        self.subprogramSpecification()

        #print(123)
        self.accept(Token.Token.IS, "'is' expected")

        self.declarativePart()

        self.accept(Token.Token.BEGIN, "'begin' expected")
        self.sequenceOfStatements()
        self.accept(Token.Token.END, "'end' expected")

        #print("roleasdfafs", self.table.table[0][1].role)




        if self.tok == Token.Token.codeToStr(Token.Token, Token.Token.ID):
            entry = self.findId()
            self.acceptRole(entry, SymbolEntry.SymbolEntry.PROC, "procedure name expected")


        self.accept(Token.Token.SEMI, "semicolon expected")

        self.table.exitScope(self.table) ## sequence problem


    def subprogramSpecification(self):
        self.accept(Token.Token.PROC,"'procedure' expected")
        #self.accept(Token.Token.ID, "identifier expected")


        entry = self.enterId(SymbolEntry.SymbolEntry.PROC,self.w)

        #print('d')
        #entry.setRole(SymbolEntry.SymbolEntry,SymbolEntry.SymbolEntry.PROC)
        self.table.enterScope(self.table)

        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.L_PAR):
            self.formalPart()


    def formalPart(self):
        self.accept(Token.Token.L_PAR, "'(' expected")
        self.parameterSpecification()
        while Token.Token.s2c(Token.Token,self.tok) == Token.Token.SEMI:
            self.nextToken()
            self.parameterSpecification()
        self.accept(Token.Token.R_PAR, "')' expected")


    def parameterSpecification(self):
        list = self.identifierList() ##
        # itr
        for t in list:
            t[1] = SymbolEntry.SymbolEntry.PARAM
            for k in self.table.table:
                if t[0] == k[0]:
                    k[2] = t[1]


            #print("list",list)
            #entry = self.table.enterSymbol(self.table,self.w, t[1])

        #list.setRole(SymbolEntry.SymbolEntry,SymbolEntry.SymbolEntry.PARAM) ##

        self.accept(Token.Token.COLON, "':' expected")
        if (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.IN)):
            self.accept(Token.Token.IN, "'in' identifier expected")
        if (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.OUT)):
            self.accept(Token.Token.OUT, "'out' identifier expected")

        ##
        entry = self.findId()
        self.acceptRole(entry,SymbolEntry.SymbolEntry.TYPE,"type name expected")
        #self.accept(Token.Token.ID, "identifier expected")


    def declarativePart(self):
        while Token.Token.s2c(Token.Token,self.tok) in self.dec:
            self.basicDeclaration()


    def basicDeclaration(self):


        if self.tok ==  Token.Token.codeToStr(Token.Token,Token.Token.ID) :
            self.numberOrObjectDeclaration()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.TYPE):
            self.typeDeclaration()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.PROC):
            self.subprogramBody()
        else:
            self.fatalError("error in declaration part")


    def numberOrObjectDeclaration(self):
        #

        list = self.identifierList()
        self.accept(Token.Token.COLON, "':' expected")
        #print("new"+self.tok+ Token.Token.codeToStr(Token.Token,Token.Token.CONST)+" ")
        #print(list)
        if (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.CONST)):

            #

            #list.setRole(SymbolEntry.SymbolEntry,SymbolEntry.SymbolEntry.CONST)
            # itr
            for t in list:
                t[1] = SymbolEntry.SymbolEntry.CONST
                for k in self.table.table:

                    if t[0] == k[0]:
                        k[2] = t[1]




                #print("list", list)
                #entry = self.table.enterSymbol(self.table,self.w, t[1])

            self.nextToken()
            self.accept(Token.Token.GETS, "':=' expected")
            ret = self.expression()
            #print("\n       ",ret)



            if len(list) == 1:

                list[0][2] = ret
                for k in self.table.table:

                    if list[0][0] == k[0]:
                        k[3] = list[0][2]

        else:
            #print("\n   else ",list)
            # itr
            for t in list:
                t[1] = SymbolEntry.SymbolEntry.VAR
                for k in self.table.table:
                    if t[0] == k[0]:
                        k[2] = t[1]


                #print("list", list)
                #entry = self.table.enterSymbol(self.table,self.w, t[1])

            #list.setRole(SymbolEntry.SymbolEntry,SymbolEntry.SymbolEntry.VAR)
            self.typeDefinition()
        self.accept(Token.Token.SEMI, "semicolon expected")


    def typeDeclaration(self):
        self.accept(Token.Token.TYPE, "'type' expected")

        ##
        #self.accept(Token.Token.ID, "identifier expected")

        #

        #for k in self.table.table:
        #    print(k[1].role)
        entry = self.enterId(SymbolEntry.SymbolEntry.TYPE,self.w)
        #entry.setRole(entry,SymbolEntry.SymbolEntry.TYPE)


        self.accept(Token.Token.IS, "'is' expected")
        self.typeDefinition()
        self.accept(Token.Token.SEMI, "semicolon expected")


    def typeDefinition(self):

        if self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ARRAY):
            self.arrayTypeDefinition()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.L_PAR):
            self.enumerationTypeDefinition()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.RANGE):
            self.range()
        elif self.tok == Token.Token.codeToStr(Token.Token,Token.Token.ID):
            ##
            entry = self.findId()
            self.acceptRole(entry,SymbolEntry.SymbolEntry.TYPE,"type name expected")

            #self.accept(Token.Token.ID, "identifier expected")
        else:
            self.fatalError("error in type definition")


    def enumerationTypeDefinition(self):
        self.accept(Token.Token.L_PAR, "'(' expected")
        # itr
        list = self.identifierList()
        for t in list:
            t[1] = SymbolEntry.SymbolEntry.CONST

            for k in self.table.table:
                if t[0] == k[0]:
                    k[2] = t[1]



            #entry = self.table.enterSymbol(self.table, self.w, t[1])

            #print("list", list)



        #list.setRole(SymbolEntry.SymbolEntry.CONST)

        self.accept(Token.Token.R_PAR, "')' expected")


    def arrayTypeDefinition(self):
        self.accept(Token.Token.ARRAY, "'array' expected")
        self.accept(Token.Token.L_PAR, "'(' expected")
        self.index()
        #print(self.tok)
        while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.COMMA):
            self.nextToken()
            self.index()

        self.accept(Token.Token.R_PAR, "')' expected")
        self.accept(Token.Token.OF, "'of' expected")
        #self.accept(Token.Token.ID, "identifier expected")
        entry = self.findId()
        self.acceptRole(entry,SymbolEntry.SymbolEntry.TYPE,"type name expected")


    def index(self):

        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.RANGE):
            self.range()
        elif (Token.Token.s2c(Token.Token,self.tok) == Token.Token.ID):
            ##
            entry = self.findId()
            self.acceptRole(entry,SymbolEntry.SymbolEntry.TYPE,"type name expected")
            #
            #self.nextToken()
        else:
            self.fatalError("error in index type")


    def range(self):
        self.accept(Token.Token.RANGE, "'range' expected")
        self.expression()
        self.accept(Token.Token.THRU, "'..' expected")
        self.expression()


    def identifierList(self):
        ##
        self.bigL = [[self.w, 0,0]]
        list = self.enterId(0,0)
        #self.nextToken()

        #print('id')
        #print(self.tok)
        #print(Token.Token.codeToStr(Token.Token,Token.Token.COMMA))
        #self.accept(Token.Token.ID, "identifier expected") #
        while (self.tok == Token.Token.codeToStr(Token.Token,Token.Token.COMMA)):
            self.nextToken()
            #self.accept(Token.Token.ID, "identifier expected") #
            ## ?????
            #print("asdf",list.next)
            self.bigL.append([self.w, 0,0])

            list.append(SymbolEntry.SymbolEntry,self.enterId(0,0))

            #print("zxcv", list.next.next)

        ###
        return self.bigL


    def sequenceOfStatements(self):

        self.statement()

        while (Token.Token.s2c(Token.Token,self.tok) in self.stmt):
            self.statement()


    def statement(self):



        if Token.Token.s2c(Token.Token,self.tok) == Token.Token.ID:

            self.assignmentOrCallStatement()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.EXIT:

            self.exitStatement()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.IF:

            self.ifStatement()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.NULL:

            self.nullStatement()
        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.WHILE or Token.Token.s2c(Token.Token,self.tok) == Token.Token.LOOP:

            self.loopStatement()
        else:
            self.fatalError("error in statement")


    def nullStatement(self):
        self.accept(Token.Token.NULL, "'null' expected")
        self.accept(Token.Token.SEMI, "semicolon expected")


    def loopStatement(self):
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.WHILE):
            self.nextToken()
            self.condition()

        self.accept(Token.Token.LOOP, "'loop' expected")
        self.sequenceOfStatements()
        self.accept(Token.Token.END, "'end' expected")
        self.accept(Token.Token.LOOP, "'loop' expected")
        self.accept(Token.Token.SEMI, "semicolon expected")


    def ifStatement(self):
        self.accept(Token.Token.IF, "'if' expected")
        self.condition()
        self.accept(Token.Token.THEN, "'then' expected")

        self.sequenceOfStatements()
        while (self.tok == Token.Token.ELSIF):
            self.nextToken()
            self.condition()
            self.accept(Token.Token.THEN, "'then' expected")
            self.sequenceOfStatements()

        if (self.tok == Token.Token.ELSE):
            self.nextToken()
            self.sequenceOfStatements()


        self.accept(Token.Token.END, "'end' expected")

        self.accept(Token.Token.IF, "'if' expected")

        self.accept(Token.Token.SEMI, "semicolon expected")



    def exitStatement(self):
        self.accept(Token.Token.EXIT, "'exit' expected")
        if (self.tok == Token.Token.WHEN):
            self.nextToken()
            self.condition()
        self.accept(Token.Token.SEMI, "semicolon expected")


    def assignmentOrCallStatement(self):



        if self.w == "print":
            #print("\nstart")
            self.Print()
            #print("\nend")

            entry = SymbolEntry.SymbolEntry.SymbolEntry(SymbolEntry.SymbolEntry,"print",3)

            self.acceptRole(entry, SymbolEntry.SymbolEntry.PROC, "print procedure expected")
        else:
            entry = self.name()
            if (Token.Token.s2c(Token.Token, self.tok) == Token.Token.GETS):

                self.acceptRole(entry, self.left, "var or param name expected")
                self.nextToken()
                ret = self.expression()

                #print("\n    ",ret)
                for i in self.table.table:

                    if entry.name == i[0]:
                        i[3] = ret



            else:

                # raise Exception('asdf')
                self.acceptRole(entry, SymbolEntry.SymbolEntry.PROC, "procedure expected")





        self.accept(Token.Token.SEMI, "semicolon expected")

    def Print(self):


        self.nextToken()


        if (Token.Token.s2c(Token.Token, self.tok) == Token.Token.L_PAR):
            self.nextToken()

            if Token.Token.s2c(Token.Token, self.tok) == Token.Token.INT or Token.Token.s2c(Token.Token,self.tok) == Token.Token.CHAR:
                #print()
                self.pTable.append(self.w)
                #print(self.w)
                self.nextToken()

            elif Token.Token.s2c(Token.Token, self.tok) == Token.Token.ID:

                exist = False

                for k in self.table.table:

                    if self.w == k[0]:
                        exist = True
                        #print()
                        #print(k[3])
                        self.pTable.append(k[3])
                        break

                if not exist:
                    print("\nID not exist")

                self.nextToken()

        else:
            #self.accept(Token.Token.L_PAR,"'(' expected")
            print("'(' expected")
            self.nextToken()

        #entry.role = tmpRole
        #entry.name = tmpName

        #return entry

        self.accept(Token.Token.R_PAR,"')' expected")




    def condition(self):
        self.expression()


    def expression(self):

        ret = self.relation()
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.AND):
            while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.AND):
                self.nextToken()
                ret2 = self.relation()
                ret = (ret and ret2)

        elif (Token.Token.s2c(Token.Token,self.tok) == Token.Token.OR):
            while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.OR):
                self.tok = self.s.nextToken()
                ret3 = self.relation()
                ret = (ret or ret3)


        return ret


    def relation(self):

        ret = self.simpleExpression()
        while Token.Token.s2c(Token.Token,self.tok) in self.relOp:
            op = self.w
            self.nextToken()
            ret2 = self.simpleExpression()

            if op =='<':
                ret = ret < ret2
            elif op == '<=':
                ret = ret <= ret2
            elif op == '>':
                ret = ret > ret2
            elif op == '>=':
                ret = ret >= ret2
            elif op == '=':
                ret = (ret == ret2)
            elif op == '/=':
                ret = (ret != ret2)


        return ret


    def simpleExpression(self):

        first = ""
        second = ""
        if Token.Token.s2c(Token.Token,self.tok) in self.addOp:
            first = self.w
            self.nextToken()
        ret = self.term()
        if first == '-':
            ret = -ret
        while Token.Token.s2c(Token.Token,self.tok) in self.addOp:
            second = self.w
            self.nextToken()
            ret2 = self.term()
        if second == '+':
            ret = ret + ret2
        elif second == '-':
            ret = ret - ret2
        return ret


    def term(self):
        ret = self.factor()
        while Token.Token.s2c(Token.Token,self.tok) in self.mulOp:

            op = self.w
            self.nextToken()
            ret2 = self.factor()

            if op == '*' :
                ret = ret * ret2
            elif op == '/' and ret2!=0:
                ret = ret / ret2
            else:
                ret = ret % ret2

        return ret



    def factor(self):
        ret = 0
        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.NOT):

            self.nextToken()
            ret = self.primary()

            if ret.isdigit():
                ret = - ret

        else:
            ret = self.primary()
            tmp = ret
            if not tmp.isdigit():
                for i in self.table.table:
                    if ret == i[0]:
                        ret = i[3]

            if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.EXPO):
                self.nextToken()
                ret2 = self.primary()
                if not ret2.isdigit():
                    for i in self.table.table:
                        if ret2 == i[0]:
                            ret2 = i[3]
                tmp2 = ret
                for i in range(ret2-1):
                    ret = tmp2*ret

        return ret


    def primary(self):
        #print("pr"+self.tok)
        ret = self.w
        #print('\n    ',ret)
        if Token.Token.s2c(Token.Token,self.tok) == Token.Token.INT or Token.Token.s2c(Token.Token,self.tok) == Token.Token.CHAR:
            self.nextToken()

        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.ID:
            ##
            #print('asdf')
            entry = self.name()



            self.acceptRole(entry,self.right,"var,param, const name expected")

        elif Token.Token.s2c(Token.Token,self.tok) == Token.Token.L_PAR:
            self.nextToken()
            self.expression()
            self.accept(Token.Token.R_PAR, "')' expected")
        else:
            self.fatalError("error in primary")

        return ret


    def name(self):

        #print("\n",self.w," ",self.tok)
        entry = self.findId()
        #for k in self.table.table:
        #    if entry.name == k[0]:
        #        print("\n>> value : ",k[3])

        tmpRole = entry.role
        tmpName = entry.name


        #print("\nASDFD",entry.name,"    ",entry.role)

        if (Token.Token.s2c(Token.Token,self.tok) == Token.Token.L_PAR):
            self.indexedComponent()

        entry.role = tmpRole
        entry.name = tmpName

        return entry





    def indexedComponent(self):
        self.nextToken()
        self.expression()
        while (Token.Token.s2c(Token.Token,self.tok) == Token.Token.COMMA):
            self.nextToken()
            self.expression()
        self.accept(Token.Token.R_PAR, "')' expected")
