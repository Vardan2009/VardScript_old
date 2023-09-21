from sys import *
import os
import time
import sys
import datetime
toks = []
numstack =[]
symbols = {}
funcs = {}

def open_file(filename):
    data = open(filename,"r").read()
    data +="//EOF//"
    return data

def run_lexer(filecontent):
    tok=""
    state = 0
    string = ""
    expr = ""
    isInIf = 0
    var =""
    isexpr =0
    comment = 0
    varStart = 0
    n = ""
    toks = []
    filecontent = list(filecontent)
    for char in filecontent:
        tok +=char
      
        if comment ==1:
          
            if char == "\n":
                comment =0
                tok = ""
        elif tok == ":" and state == 0:
                if expr != "" and isexpr ==1:
                    toks.append("EXPR:"+expr)
                    expr = ""
                elif expr != "" and isexpr ==0:
                    toks.append("NUM:"+expr)
                    var = ""
                elif var !="":
                    toks.append("VAR:"+var)
                var = ""
                varStart = 0
                comment =1
                tok = ""
        elif tok == " ":
            if var !="":
                toks.append("VAR:"+var)
                var = ""
                varStart = 0
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "//EOF//":
            if expr != "" and isexpr ==1:
                toks.append("EXPR:"+expr)
                expr = ""
            elif expr != "" and isexpr ==0:
                toks.append("NUM:"+expr)
                expr = ""
            elif var !="":
                toks.append("VAR:"+var)
                var = ""
                varStart = 0
            tok = ""
        elif tok == "<" and state ==0:
            if expr != "" and isexpr ==0:
                toks.append("NUM:"+expr)
                expr = ""
            if var !="":
                toks.append("VAR:"+var)
                var = ""
                varStart = 0
            toks.append("LT")
            tok = ""
        elif tok == ">" and state ==0:
            if expr != "" and isexpr ==0:
                toks.append("NUM:"+expr)
                expr = ""
            if var !="":
                toks.append("VAR:"+var)
                var = ""
                varStart = 0
            toks.append("GT")
            tok = ""
        elif tok =="=" and state ==0:
            if expr != "" and isexpr ==0:
                toks.append("NUM:"+expr)
                expr = ""
            if var !="":
                toks.append("VAR:"+var)
                var = ""
                varStart = 0
            if toks[-1] == "EQUALS":
                toks[-1] = "EQEQ"
            else:
                toks.append("EQUALS")
            tok = ""
        
        elif tok =="&" and state ==0:
            varStart =1
            var+=tok
            tok = ""
        elif varStart ==1:
            if tok == "/":
                if var !="":
                    toks.append("VAR:"+var)
                    var = ""
                    varStart = 0
                tok == ""
            var+=tok
            tok = ""
        elif tok == "func":
            toks.append("FUNC")
            tok = ""
        elif tok.endswith("()"):
            toks.append("FUNC_NAME:"+tok)
            tok = ""
        elif tok == "endfunc":
            toks.append("ENDFUNC")
            tok =""
        elif tok == "ln_out":
            toks.append("PRINTLN")
            tok =""
        elif tok == "typeof":
            toks.append("TYPEOF")
            tok =""
        elif tok == "out":
            toks.append("PRINT")
            tok =""
        elif tok == "endif":
            toks.append("ENDIF")
            tok =""
        elif tok == "until":
            toks.append("UNTIL")
            tok =""
        elif tok == "endwhile":
            toks.append("ENDWHILE")
            tok =""
        elif tok == "else":
            toks.append("ELSE")
            tok =""
        elif tok == "if":
            toks.append("IF")
            tok =""
        elif tok == "while":
            toks.append("WHILE")
            tok =""
        elif tok == "parse":
            toks.append("PARSE")
            tok =""
        elif tok == "t_num":
            toks.append("TYPE_N")
            tok =""
        elif tok == "t_str":
            toks.append("TYPE_S")
            tok =""
        elif tok == "then":
            if expr != "" and isexpr ==0:
                toks.append("NUM:"+expr)
                expr = ""
            toks.append("THEN")
            isInIf = 1
            tok =""
        elif tok == "input":
            toks.append("INPUT")
            tok =""
        elif tok == "time":
            toks.append("TIME")
            tok =""
        elif tok == "os":
            toks.append("OS")
            tok =""
        elif tok == "sleep":
            toks.append("SLEEP")
            tok =""
        elif tok == "#import":
            toks.append("IMPORT")
            tok =""
        elif (tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9") and state == 0:
            expr += tok
            tok = ""
        elif (tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")" or tok =="%") and state ==0:
            isexpr =1
            expr +=tok
            tok = ""
        elif tok == "\t":
            tok = ""
        elif tok == "\"" or tok ==" \"":
            if state == 0:
                state = 1
            elif state == 1:
                toks.append("STRING:"+string+"\"")
                string = ""
                state = 0
                tok = ""
        elif state ==1:
            string += tok
            tok = ""
       
    #print(toks)
    return toks

def evalExpr(expr):
  return eval(expr)

def doPRINT(toPRINT,end):
    if toPRINT[0:6] == "STRING":
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif toPRINT[0:3] == "NUM":
        toPRINT = toPRINT[4:]
    elif toPRINT[0:4] == "EXPR":
        toPRINT = evalExpr(toPRINT[5:])
    print(toPRINT,end=end)


def doGET(toPRINT):
    if toPRINT[0:6] == "STRING":
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif toPRINT[0:3] == "NUM":
        toPRINT = toPRINT[4:]
    elif toPRINT[0:4] == "EXPR":
        toPRINT = evalExpr(toPRINT[5:])
    return toPRINT

def doASSIGN(name,val):
    symbols[name[4:]] = val

def getVARIABLE(varname):
    varname = varname[4:]
   # print("finding variable "+varname)
    if varname in symbols:
        #print("output "+symbols[varname])
        return symbols[varname]
    else:
        print ("ERROR: Undefined Variable: "+varname)
        return "ERROR: Undefined Variable: "+varname
        exit()

def getINPUT(str,name):
    i = input(str[1:-1]+" ")
    symbols[name] = "STRING:\""+i+"\""

def handle_if_condition(tokes, i):
    condition_type1, operand1 = tokes[i+1].split(":")
    condition_type2, operand2 = tokes[i+3].split(":")

    if condition_type1 == "NUM":
        operand1 = int(operand1)
    elif condition_type1 == "VAR":
        operand1 = getVARIABLE(tokes[i+1]).split(":")[1]

    if condition_type2 == "NUM":
        operand2 = int(operand2)
    elif condition_type2 == "VAR":
        operand2 = getVARIABLE(tokes[i+3]).split(":")[1]

    #print("Comparing "+str(operand1)+" and "+str(operand2))
    if tokes[i+2] == "EQEQ":
        if str(operand1) == str(operand2):
            run_parser(tokes[i+5:tokes.index("ELSE", i+5)] if "ELSE" in tokes else tokes[i+5:tokes.index("ENDIF", i+5)])
        else:
            if "ELSE" in tokes:
                run_parser(tokes[tokes.index("ELSE", i+5)+1:tokes.index("ENDIF", i+5)])
    elif tokes[i+2] == "GT":
        if int(operand1) > int(operand2):
            run_parser(tokes[i+5:tokes.index("ELSE", i+5)] if "ELSE" in tokes else tokes[i+5:tokes.index("ENDIF", i+5)])
        else:
            if "ELSE" in tokes:
                run_parser(tokes[tokes.index("ELSE", i+5)+1:tokes.index("ENDIF", i+5)])
    elif tokes[i+2] == "LT":
        if int(operand1)< int(operand2):
            run_parser(tokes[i+5:tokes.index("ELSE", i+5)] if "ELSE" in tokes else tokes[i+5:tokes.index("ENDIF", i+5)])
        else:
            if "ELSE" in tokes:
                run_parser(tokes[tokes.index("ELSE", i+5)+1:tokes.index("ENDIF", i+5)])


#WHILE VAR UNTIL NUM THEN
def handle_while_condition(tokes, i):
    if tokes[i+3].split(":")[0] == "NUM":
        num = tokes[i+3].split(":")[1]
    elif tokes[i+3].split(":")[0] == "VAR":
        num =getVARIABLE(tokes[i+3]).split(":")[1]

    var = getVARIABLE(tokes[i+1]).split(":")[1]
    num = int(num)
    var = int(var)
    #print(operand1+" "+operand2)
    while int(var)< int(num):
            var+=1
            symbols[tokes[i+1].split(":")[1]] = "NUM:"+str(var)
            #print("running thru "+ str(tokes[i+5:tokes.index("ENDWHILE", i+5)]))
            run_parser(tokes[i+5:tokes.index("ENDWHILE", i+5)])

def run_parser(tokes):
    inIf = 0
    inFunc = 0
    i = 0
    inWhile = 0

    while (i<len(tokes)):
        #print(toks[i] +" "+ str(i)+" "+str(len(tokes)))
        if tokes[i] == "ENDIF":
            inIf = 0
            i+=1
        elif tokes[i] == "ENDWHILE":
            inWhile = 0
            i+=1
        elif tokes[i] == "ENDFUNC":
            inFunc = 0
            i+=1
        elif inIf==1:
            i+=1
        elif inWhile==1:
            i+=1
        elif inFunc==1:
            i+=1
        elif tokes[i][0:9] == "FUNC_NAME":
            run_parser(funcs[tokes[i][10:]])
            i+=1
        elif tokes[i] + " " + tokes[i+1][0:6] == "PRINT STRING" or tokes[i] + " " + tokes[i+1][0:3] == "PRINT NUM" or tokes[i] + " " + tokes[i+1][0:4] == "PRINT EXPR"or tokes[i] + " " + tokes[i+1][0:3] == "PRINT VAR":
            if tokes[i+1][0:6] == "STRING":
                doPRINT(tokes[i+1],"")
            elif tokes[i+1][0:3] == "NUM":
                doPRINT(tokes[i+1],"")
            elif tokes[i+1][0:4] == "EXPR":
                doPRINT(tokes[i+1],"")
            elif tokes[i+1][0:3] == "VAR":
                doPRINT(getVARIABLE(tokes[i+1]),"")
            i+=2
        elif tokes[i] + " " + tokes[i+1][0:6] == "PRINTLN STRING" or tokes[i] + " " + tokes[i+1][0:3] == "PRINTLN NUM" or tokes[i] + " " + tokes[i+1][0:4] == "PRINTLN EXPR"or tokes[i] + " " + tokes[i+1][0:3] == "PRINTLN VAR":
            if tokes[i+1][0:6] == "STRING":
                doPRINT(tokes[i+1],"\n")
            elif tokes[i+1][0:3] == "NUM":
                doPRINT(tokes[i+1],"\n")
            elif tokes[i+1][0:4] == "EXPR":
                doPRINT(tokes[i+1],"\n")
            elif tokes[i+1][0:3] == "VAR":
                doPRINT(getVARIABLE(tokes[i+1]),"\n")
            i+=2
        elif tokes[i] + " "+tokes[i+1][0:6] == "TIME STRING":
                print(datetime.datetime.now().strftime(doGET((tokes[i+1]))))
                i+=2
        elif tokes[i] + " "+tokes[i+1][0:6] == "OS STRING":
                os.system(doGET(tokes[i+1]))
                i+=2
        elif tokes[i] + " "+tokes[i+1][0:3] == "SLEEP NUM":
                time.sleep(int(doGET(tokes[i+1]))/1000)
                i+=2
        elif tokes[i] + " "+tokes[i+1][0:3] == "SLEEP VAR":
                time.sleep(int(doGET(getVARIABLE(tokes[i+1])))/1000)
                i+=2
        elif tokes[i] + " "+tokes[i+1][0:9] == "FUNC FUNC_NAME":
                inFunc = 1
                funcs[tokes[i+1][10:]] = tokes[i+2:tokes.index("ENDFUNC",i)]
                i+=2
        elif tokes[i] == "PARSE" and tokes[i+2] == "TYPE_N":
            strn = getVARIABLE(tokes[i+1]) #STRING:"34"
            intval = strn[8:]
            intval = intval[:-1]
            symbols[tokes[i+1].split(":")[1]] = "NUM:"+str(intval)
            i+=3
        #parse %qaq t_str
        elif tokes[i] + " "+tokes[i+1][0:3] == "TYPEOF VAR":
            print(getVARIABLE(tokes[i+1]).split(":")[0])
            i+=2
        elif tokes[i] == "PARSE" and tokes[i+2] == "TYPE_S":
            
            strn = getVARIABLE(tokes[i+1]) #NUM:23  
            
            intval = strn.split(":")[1] #23

            symbols[tokes[i+1].split(":")[1]] = "STRING:\""+str(intval)+"\""
            i+=3
        elif tokes[i] + " "+tokes[i+1][0:6] + " " + tokes[i+2][0:3] == "INPUT STRING VAR":
            getINPUT(tokes[i+1][7:],tokes[i+2][4:])
            i+=3
        elif tokes[i][0:3] +" "+tokes[i+1]+" "+tokes[i+2][0:6] == "VAR EQUALS STRING" or tokes[i][0:3] +" "+tokes[i+1]+" "+tokes[i+2][0:3] == "VAR EQUALS NUM" or tokes[i][0:3] +" "+tokes[i+1]+" "+tokes[i+2][0:4] == "VAR EQUALS EXPR"or tokes[i][0:3] +" "+tokes[i+1]+" "+tokes[i+2][0:3] == "VAR EQUALS VAR":
            if tokes[i+2][0:6] == "STRING":
                 doASSIGN(tokes[i],tokes[i+2])
            elif tokes[i+2][0:3] == "NUM":
                 doASSIGN(tokes[i],tokes[i+2])
            elif tokes[i+2][0:4] == "EXPR":
                 doASSIGN(tokes[i],"NUM:"+ str(evalExpr(tokes[i+2][5:])))
            elif tokes[i+2][0:3] == "VAR":
                 doASSIGN(tokes[i],getVARIABLE(tokes[i+2]))
            i+=3
        elif tokes[i] == "WHILE" and tokes[i+4] == "THEN":
            inWhile =1
            handle_while_condition(tokes, i)
            i+=5
        elif tokes[i] == "IF" and tokes[i+4] == "THEN":
            inIf = 1
            handle_if_condition(tokes, i)
            i += 5
        
    #print (symbols)



def run():
    data = open_file(argv[1])
    tokens = run_lexer(data)
    run_parser(tokens)

run()

