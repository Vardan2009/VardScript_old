import math
import random
import re
from sys import *
import os
import time
import sys
import datetime

toks = []
numstack =[]
symbols = {}
definitions = {}
funcs = {}
funcsreturns = {}

def open_file(filename):

    data = open(filename,"r").read()
    data +="\n//EOF//"
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
        #print(tok)
        #print (isexpr)
        if comment ==1:
            if char == "\n":
                comment =0
                tok = ""
        elif char == "]":
                tok = ""
                isexpr = 0
        elif isexpr == 1:
                expr+=tok
                tok = ""
        elif tok == ":" and state == 0:
                if expr != "":
                    toks.append("EXPR:"+expr)
                    expr = ""
                #elif expr != "" and isexpr ==0:
                #    toks.append("NUM:"+expr)
                #    var = ""
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
            if expr != "":
                toks.append("EXPR:"+expr)
                expr = ""
            #elif expr != "" and isexpr ==0:
            #    toks.append("NUM:"+expr)
            #    expr = ""
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
            elif toks[-1] == "DOLLAR":
                toks[-1] = "NEQ"
            else:
                toks.append("EQUALS")
            tok = ""
        
        elif tok =="&" and state ==0 and isexpr == 0:
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
        elif tok == "define":
            toks.append("DEFINE")
            tok =""
        elif tok == "as":
            toks.append("AS")
            tok =""
        elif tok == "$":
            toks.append("DOLLAR")
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
        elif tok == "exit":
            toks.append("EXIT")
            tok =""
        elif tok == "sleep":
            toks.append("SLEEP")
            tok =""
        elif tok == "#import":
            toks.append("IMPORT")
            tok =""
        elif tok == "ret":
            toks.append("RETURN")
            tok =""
        elif (tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9" or tok == "nrand" or re.search(r'rand (\d+),(\d+)', tok)) and state == 0:
            expr += tok
            tok = ""
        elif (tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")" or tok =="%") and state ==0:
            isexpr =1
            expr +=tok
            tok = ""
        elif (tok == "[" and state==0):
                isexpr =1
                tok = ""
        elif (tok == "]" and state==0):
                if expr != "":
                    toks.append("EXPR:"+expr)
                    expr = ""
                #elif expr != "" and isexpr ==0:
                #    toks.append("NUM:"+expr)
                #    expr = ""
                elif var !="":
                    toks.append("VAR:"+var)
                    var = ""
                    varStart = 0
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

def replace_random(match):
    x = int(match.group(1))
    y = int(match.group(2))
    return str(random.randint(x, y))

def sqrt(match):
    expression = match.group(1)
    result = f"{evalExpr(expression)**0.5}"
    return result

def cos(match):
    expression = match.group(1)
    result = f"{math.cos(evalExpr(expression))}"
    return result

def sin(match):
    expression = match.group(1)
    result = f"{math.sin(evalExpr(expression))}"
    return result

def tan(match):
    expression = match.group(1)
    result = f"{math.tan(evalExpr(expression))}"
    return result

def roundd(match):
    expression = match.group(1)
    result = f"{round(evalExpr(expression))}"
    return result

def pow(match):
    base = match.group(1)
    exponent = match.group(2)
    result = f"{evalExpr(base)**evalExpr(exponent)}"
    return result

def evalExpr(expr):
  expr = expr.replace("nrand",str(random.random()))
  expr = expr.replace("const_pi",str(math.pi))
  expr = expr.replace("const_e",str(math.e))
  expr = re.sub(r'rand (\d+),(\d+)',replace_random,expr)

  while re.search(r'sqrt\(([^()]+)\)',expr):
    expr = re.sub(r'sqrt\(([^()]+)\)',sqrt,expr)

  while re.search(r'cos\(([^()]+)\)',expr):
        expr = re.sub(r'cos\(([^()]+)\)',cos,expr)

  while re.search(r'tan\(([^()]+)\)',expr):
        expr = re.sub(r'tan\(([^()]+)\)',tan,expr)

  while re.search(r'round\(([^()]+)\)',expr):
        expr = re.sub(r'round\(([^()]+)\)',roundd,expr)

  while re.search(r'sin\(([^()]+)\)',expr):
        expr = re.sub(r'sin\(([^()]+)\)',sin,expr)

  while re.search(r'pow\(([^()]+),\s*([^()]+)\)',expr):
    expr = re.sub(r'pow\(([^()]+),\s*([^()]+)\)',pow,expr)

  for a in symbols:
      
      e= getVARIABLE("VAR:"+str(a)).split(":",1)[1]
      expr = expr.replace(a,e)

  for a in funcs:
      run_parser(funcs[a],a)
      #print(funcsreturns[a])
      #print("replacing "+str(a)+" with "+str(funcsreturns[a]))
      expr = expr.replace(a,funcsreturns[a])

  if expr == "":
        result = expr
  else:
      result = eval(expr)
  
  return result

def doPRINT(toPRINT,end):
    if toPRINT[0:6] == "STRING":
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif toPRINT[0:3] == "NUM":
        toPRINT =evalExpr(toPRINT[4:])
    elif toPRINT[0:4] == "EXPR":
        toPRINT = evalExpr(toPRINT[5:])
    print(toPRINT,end=end)


def doGET(toPRINT):
    if toPRINT[0:6] == "STRING":
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif toPRINT[0:3] == "NUM":
        toPRINT = evalExpr(toPRINT[4:])
    elif toPRINT[0:4] == "EXPR":
        toPRINT = evalExpr(toPRINT[5:])
    return toPRINT

def doASSIGN(name,val):
    if val.split(":")[0] == "NUM":
        symbols[name[4:]] = "NUM:"+ str(evalExpr(val.split(":")[1]))
    else:
        symbols[name[4:]] = val

def getVARIABLE(varname):
    varname = varname[4:]
   # print("finding variable "+varname)
    if varname in symbols:
        #print("output "+symbols[varname])
        return symbols[varname]
    else:
        #print ("ERROR: Undefined Variable: "+varname)
        raise Exception("Undefined Variable: "+varname)
        return "ERROR: Undefined Variable: "+varname
        exit()

def getINPUT(str,name):
    i = input(str[1:-1]+" ")
    symbols[name] = "STRING:\""+i+"\""

def handle_if_condition(tokes, i,end):
    condition_type1, operand1 = tokes[i+1].split(":")
    condition_type2, operand2 = tokes[i+3].split(":")

    if condition_type1 == "NUM":
        operand1 = evalExpr(operand1)
    elif condition_type1 == "VAR":
        operand1 = getVARIABLE(tokes[i+1]).split(":")[1]
    elif condition_type1 == "EXPR":
        operand1 = evalExpr(operand1)
    else:
        operand2 = evalExpr(operand2)

        
    if condition_type2 == "NUM":
        operand2 = evalExpr(operand2)
    elif condition_type2 == "VAR":
        operand2 = getVARIABLE(tokes[i+3]).split(":")[1]
    elif condition_type1 == "EXPR":
        operand2 = evalExpr(operand2)
    else:
        operand2 = evalExpr(operand2)

    #print("Comparing "+str(operand1)+" and "+str(operand2))
    if tokes[i+2] == "EQEQ":
        if str(operand1) == str(operand2):
            run_parser(tokes[i+5:end])
    if tokes[i+2] == "NEQ":
        if str(operand1) != str(operand2):
            run_parser(tokes[i+5:end])
    elif tokes[i+2] == "GT":
        if int(operand1) > int(operand2):
            run_parser(tokes[i+5:end])
    elif tokes[i+2] == "LT":
        if int(operand1)< int(operand2):
            run_parser(tokes[i+5:end])


#WHILE VAR UNTIL NUM THEN
def handle_while_condition(tokes, i):

    if tokes[i+3].split(":")[0] == "NUM":
        num = evalExpr(tokes[i+3].split(":")[1])
    elif tokes[i+3].split(":")[0] == "EXPR":
        num = evalExpr(tokes[i+3].split(":")[1])
    elif tokes[i+3].split(":")[0] == "VAR":
        num =getVARIABLE(tokes[i+3]).split(":")[1]

    var = getVARIABLE(tokes[i+1]).split(":")[1]
    num = int(num)
    var = int(var)
    #print(operand1+" "+operand2)
    if tokes[i+2] == "EQEQ":
        while int(var)== int(num):
            doWHILE(var,num,tokes,i)
            var = int(getVARIABLE(tokes[i+1]).split(":")[1])
    if tokes[i+2] == "GT":
        while int(var)> int(num):
            doWHILE(var,num,tokes,i)
            var = int(getVARIABLE(tokes[i+1]).split(":")[1])
    if tokes[i+2] == "LT":
        while int(var)< int(num):
            doWHILE(var,num,tokes,i)
            var = int(getVARIABLE(tokes[i+1]).split(":")[1])

def doWHILE(var,num,tokes,i):
    var = getVARIABLE(tokes[i+1]).split(":")[1]
    if tokes[i+3].split(":")[0] == "NUM":
            num = evalExpr(tokes[i+3].split(":")[1])
    elif tokes[i+3].split(":")[0] == "EXPR":
                num = evalExpr(tokes[i+3].split(":")[1])
    elif tokes[i+3].split(":")[0] == "VAR":
                num =getVARIABLE(tokes[i+3]).split(":")[1]
    num = int(num)
    var = int(var)
            
            #print ("num =" + str(num))
            #print ("var =" + str(var))
            #symbols[tokes[i+1].split(":")[1]] = "NUM:"+str(var)
            #print("running thru "+ str(tokes[i+5:tokes.index("ENDWHILE", i+5)]))
    run_parser(tokes[i+5:tokes.index("ENDWHILE", i+5)])

def run_parser(tokes,infunc = ""):
 #try:
    inIf = 0
    lInd = 0
    inFunc = 0
    i = 0
    inWhile = 0
    #print(tokes)
    while (i<len(tokes)):
        #print(toks[i] +" "+ str(i)+" "+str(len(tokes)))
        if tokes[i] == "ENDIF":
            inIf -=1

            if inIf == 0:
                handle_if_condition(tokes, lInd,i)

            if inIf <0:
                inIf = 0
            
            i+=1
        elif tokes[i] == "ENDWHILE":
            inWhile = 0
            i+=1
        elif tokes[i] == "ENDFUNC":
            inFunc = 0
            i+=1
        elif inIf>=1:
            i+=1
        elif inWhile==1:
            i+=1
        elif inFunc==1:
            i+=1
        elif tokes[i][0:9] == "FUNC_NAME":
            run_parser(funcs[tokes[i][10:]],tokes[i][10:])
            i+=1
        elif tokes[i] + " " + tokes[i+1][0:6] == "RETURN STRING" or tokes[i] + " " + tokes[i+1][0:3] == "RETURN NUM" or tokes[i] + " " + tokes[i+1][0:4] == "RETURN EXPR"or tokes[i] + " " + tokes[i+1][0:3] == "RETURN VAR":
            funcsreturns[infunc] = tokes[i+1].split(":",1)[1]
            return
            i+=2
        elif tokes[i] == "EXIT":
            exit()
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
                funcsreturns[tokes[i+1][10:]] = ""
                i+=2
        elif tokes[i] == "PARSE" and tokes[i+2] == "TYPE_N":
            strn = getVARIABLE(tokes[i+1]) #STRING:"34"
            intval = strn[8:]
            intval = intval[:-1]
            symbols[tokes[i+1].split(":")[1]] = "NUM:"+str(intval)
            i+=3
        #parse &test t_str
        elif tokes[i] + " "+tokes[i+1][0:3] == "TYPEOF VAR":
            print(getVARIABLE(tokes[i+1]).split(":")[0])
            i+=2
        elif tokes[i] == "PARSE" and tokes[i+2] == "TYPE_S":
            
            strn = getVARIABLE(tokes[i+1]) #NUM:23  
            
            intval = strn.split(":")[1] #23

            symbols[tokes[i+1].split(":")[1]] = "STRING:\""+str(intval)+"\""
            i+=3
        #elif tokes[i] + " "+tokes[i+1][0:6]+" "+tokes[i+2]+" "+tokes[i+3][0:6] == "DEFINE STRING AS STRING":
        #    definitions[doGET(tokes[i+1])] = doGET(tokes[i+3])
        #    i+=4
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
            #print(inIf)
            if inIf == 0:
                lInd = i
            inIf +=1
            i += 5
        
 #except Exception as e:
     #print("File \""+str(argv[1])+"\", at token \""+str(tokes[i])+"\", "+str(e))
        
    #print (symbols)



def run():
    if len(argv) < 2:
        print("ERROR: No VardScript File Specified")
        exit()
    if os.path.exists(argv[1]):
        root, extension = os.path.splitext(argv[1])
        if extension == ".vard":
            data = open_file(argv[1])
            tokens = run_lexer(data)
            run_parser(tokens)
        else:
            print("ERROR: Enter a .vard file")
            exit() 
    else:
        print("ERROR: VardScript File Doesn't Exist")
        exit() 

run()

