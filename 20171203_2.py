import sys
import copy
import operator
def recovery(variables,logs):
    endflag = False
    startflag = False
    status = {}
    uncomplete = []
    for i in range(len(logs)-1,-1,-1):
        log = logs[i]
        log = log[1:len(log)-1]
        if "COMMIT" in log:
            curtrans = log.split(' ')[1]
            status[curtrans] = "commit"
        elif "START" in log and "CKPT" not in log:
            curtrans = log.split(' ')[1]
            status[curtrans] = "seen"
        elif "START CKPT" in log:
            startflag = True
            if(endflag):
                sort_vars = dict(sorted(variables.items(),key=operator.itemgetter(0)))
                for k,key in enumerate(sort_vars):
                    if(k!=len(sort_vars)-1):
                        print(key,sort_vars[key],end=' ')
                    else:
                        print(key,sort_vars[key])
                break
            else:
                uncomplete = log.split(' ')[2]
                uncomplete = uncomplete[1:len(uncomplete)-1]
                uncomplete = uncomplete.replace(" ","")
                uncomplete = uncomplete.split(',')
                for j in uncomplete:
                    if j not in status:
                        status[j]="unseen"
        elif "END CKPT" in log:
            endflag = True
        else:
            cmd = log.replace(" ","").split(',')
            transaction = cmd[0]
            var = cmd[1]
            val = cmd[2]
            if transaction in status:
                if(status[transaction]=="unseen"):
                    variables[var] = val
            else:
                status[transaction] = "unseen"
                variables[var] = val
        cond = False
        for j in status:
            if status[j] == "unseen":
                cond = False
                break
            else:
                cond = True
        if(cond):
            sort_vars = dict(sorted(variables.items(),key=operator.itemgetter(0)))
            for k,key in enumerate(sort_vars):
                if(k!=len(sort_vars)-1):
                    print(key,sort_vars[key],end=' ')
                else:
                    print(key,sort_vars[key])
            break

def main():
    if(len(sys.argv)!=2):
        print("Run as python code.py inputfile")
    else:
        filename = sys.argv[1]
        with open(filename) as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
        variables = {}
        logvars = lines[0].split(' ')
        logs = copy.deepcopy(lines[2:])
        for j in range(0,len(logvars),2):
            variables[logvars[j]] = logvars[j+1]
        # print(variables)
        orig_stdout = sys.stdout
        f = open('20171203_2.txt', 'w')
        sys.stdout = f
        recovery(variables,logs)
        sys.stdout = orig_stdout
        f.close()
if __name__ == "__main__":
    main()