import sys
import copy
import operator
def makelogs(transactions,discvariables,x):
    outbuffer = []
    memvariables = {}
    pointers = {}
    for t in transactions:
        pointers[t] = 0
    inmemoryvars = {}
    ops = ['+','-','*','/']
    while True:
        for t in transactions:
            if(pointers[t]+x<=len(transactions[t])):
                execcmds = transactions[t][pointers[t]:pointers[t]+x]
            else:
                execcmds = transactions[t][pointers[t]:len(transactions[t])]
            if(pointers[t]==0):
                print("<START " + t + ">")
                sort_memvars = dict(sorted(memvariables.items(),key=operator.itemgetter(0)))
                sort_discvars = dict(sorted(discvariables.items(),key=operator.itemgetter(0)))
                if(len(sort_memvars)==0):
                    print()
                else:              
                    for k,key in enumerate(sort_memvars):
                        if(k!=len(sort_memvars)-1):
                            print(key,sort_memvars[key],end=' ')
                        else:
                            print(key,sort_memvars[key])
                for k,key in enumerate(sort_discvars):
                    if(k!=len(sort_discvars)-1):
                        print(key,sort_discvars[key],end=' ')
                    else:
                        print(key,sort_discvars[key])
            for j in range(len(execcmds)):
                cmd = execcmds[j]
                cmd = cmd.replace(" ","")
                if("READ" in cmd):
                    posopen = cmd.find("(")
                    poscomma = cmd.find(",")
                    posclose = cmd.find(")")
                    curvar = cmd[posopen+1:poscomma]
                    assignvar = cmd[poscomma+1:posclose]
                    if curvar not in memvariables:
                        memvariables[curvar] = discvariables[curvar]
                        inmemoryvars[assignvar] = discvariables[curvar]
                    else:
                        inmemoryvars[assignvar] = memvariables[curvar]
                elif("WRITE" in cmd):
                    posopen = cmd.find("(")
                    poscomma = cmd.find(",")
                    posclose = cmd.find(")")
                    curvar = cmd[posopen+1:poscomma]
                    assignvar = cmd[poscomma+1:posclose]
                    if curvar not in memvariables:
                        # print("Variable not in memory")
                        pass
                    else:
                        print("<"+t+", "+curvar+", " + str(memvariables[curvar])+">")
                        memvariables[curvar] = inmemoryvars[assignvar]
                        sort_memvars = dict(sorted(memvariables.items(),key=operator.itemgetter(0)))
                        sort_discvars = dict(sorted(discvariables.items(),key=operator.itemgetter(0)))
                        if(len(sort_memvars)==0):
                            print()
                        else:               
                            for k,key in enumerate(sort_memvars):
                                if(k!=len(sort_memvars)-1):
                                    print(key,sort_memvars[key],end=' ')
                                else:
                                    print(key,sort_memvars[key])
                        for k,key in enumerate(sort_discvars):
                            if(k!=len(sort_discvars)-1):
                                print(key,sort_discvars[key],end=' ')
                            else:
                                print(key,sort_discvars[key])
                elif("OUTPUT" in cmd):
                    posopen = cmd.find("(")
                    poscomma = cmd.find(",")
                    posclose = cmd.find(")")
                    curvar = cmd[posopen+1:poscomma]
                    assignvar = cmd[poscomma+1:posclose]
                    if curvar not in memvariables:
                        # print("Variable not in memory")
                        pass
                    else:
                        discvariables[curvar] = memvariables[curvar]
                else:
                    query = cmd.split(':=')
                    assignvar = query[0]
                    opr = None
                    for o in ops:
                        if(o in query[1]):
                            opr = o
                            break
                    if(opr is None):
                        # print("No operator")
                        pass
                    else:
                        pos = query[1].find(opr)
                        val = query[1][pos+1:]
                        inmemoryvars[assignvar] = eval(str(inmemoryvars[assignvar]) + opr + val)
            pointers[t]+=x
            if(pointers[t]>=len(transactions[t])):
                print("<COMMIT "+t+">")
                sort_memvars = dict(sorted(memvariables.items(),key=operator.itemgetter(0)))
                sort_discvars = dict(sorted(discvariables.items(),key=operator.itemgetter(0)))
                if(len(sort_memvars)==0):
                    print()
                else:             
                    for k,key in enumerate(sort_memvars):
                        if(k!=len(sort_memvars)-1):
                            print(key,sort_memvars[key],end=' ')
                        else:
                            print(key,sort_memvars[key])
                for k,key in enumerate(sort_discvars):
                    if(k!=len(sort_discvars)-1):
                        print(key,sort_discvars[key],end=' ')
                    else:
                        print(key,sort_discvars[key])
        cond = False
        for m in pointers:
            if(pointers[m]<len(transactions[m])) :
                cond = False
                break
            else:
                cond = True
        if(cond):
            break
    return outbuffer                 
def main():
    if(len(sys.argv) != 3):
        print("Please run as Python code.py input_file x")
        sys.exit(-1)
    else:
        filename = sys.argv[1]
        with open(filename) as f:
            trans = f.readlines()
        trans = [i.strip() for i in trans]
        # print(transactions)
        memvariables = {}
        discvariables = {}
        transactions = {}
        var = trans[0].split(' ')
        for j in range(0,len(var),2):
            discvariables[var[j]] = var[j+1]
        trans = trans[2:]
        t = 0
        while(t < len(trans)):
            inp = trans[t]
            inp = inp.split(' ')
            transactions[inp[0]] = []
            transactions[inp[0]] = trans[t+1:t+1+int(inp[1])]
            t += int(inp[1])+2
        x = int(sys.argv[2])
        orig_stdout = sys.stdout
        f = open('20171203_1.txt', 'w')
        sys.stdout = f
        makelogs(transactions,discvariables,x)
        sys.stdout = orig_stdout
        f.close()
if  __name__ == "__main__":
    main()