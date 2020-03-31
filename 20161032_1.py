from collections import OrderedDict
import sys
import os

database = OrderedDict()
memory = OrderedDict()
registers, trans_ids, id2commands, ans = {}, [], {}, ""

def init_value(line):
    line = line.strip()
    line = line.split()
    assert len(line)%2==0
    for i in range(0, len(line), 2):
        database[line[i].strip()] = int(line[i+1].strip())
    
def read(path):
    num, tid, flag = 0, None, False
    with open(path,'r') as f:
        for line in f.readlines():
            if not flag:
                init_value(line)
                flag = True
                continue
            if line.strip() == "":
                continue
            if num:
                s = line.strip()
                id2commands[tid].append(s)
                num=num-1
            else:
                temp = line.strip().split()
                tid, num = temp[0].strip(), int(temp[1].strip())
                if tid not in id2commands:
                    trans_ids.append(tid)
                    id2commands[tid] = []
                else:
                    sys.exit("Repeated Transaction")

def fill(a,b):
    return "{} {}".format(a,b)

def output_status():
    global ans
    sort_memory = sorted(memory)
    for i, var in enumerate(sort_memory):
        ans = ans + fill(var, memory[var])
        if i!=len(sort_memory) - 1:
            ans += " "
    ans += "\n"
    sort_database = sorted(database)
    for i, var in enumerate(sort_database):
        ans = ans + fill(var, database[var])
        if i!=len(sort_database) - 1:
            ans = ans + " "
    ans = ans + "\n"

def db_execute(cmd, op, tid):
    global ans
    vnames = ["read", "write", "output"]
    cmd = cmd[:-1].split('(')[1].strip()
    dict_fill = []
    if ',' in cmd:
        temp = cmd.split(',')
        var, tmp = temp[0].strip(), temp[1].strip()
    if op.lower() == vnames[0]:
        if var in memory:
            registers[tmp] = memory[var]
        else:
            registers[tmp] = database[var]
            memory[var] = database[var]
    
    elif op.lower() == vnames[1]:
        ans = ans + "<{}, {}, ".format(tid, var)
        if var not in memory:
            memory[var] = database[var]
        ans = ans + "{}>\n".format(memory[var])
        memory[var] = registers[tmp]
        output_status()
    
    elif op.lower() == vnames[2]:
        if cmd not in memory:
            memory[cmd] = database[cmd]
        else:
            database[cmd] = memory[cmd]

def check(inp):
    try:
        return int(inp)
    except:
        return registers[inp]

def arith_execute(c, a, b, op):
    a, b = check(a), check(b)
    dic_op = ["+","-","*","/"]
    res = [a+b,a-b,a*b]
    if op == dic_op[0]:
        registers[c] = res[0]
    elif op == dic_op[1]:
        registers[c] = res[1]
    elif op == dic_op[2]:
        registers[c] = res[2]
    elif op == dic_op[3]:
        if b==0:
            sys.exit("Divide by zero")
        registers[c] = a / b
    

def execute(tid, start, end):
    db_ops, ops = ["read", "write", "output"], ["+", "-", "*", "/"]
    for i in range(start, end):
        cmd = id2commands[tid][i]
        flag = False
        for op in db_ops:
            if op not in cmd.lower():
                continue
            else:
                flag = True
                db_execute(cmd, op, tid)
                break
        if flag==True:
            continue
        cmd = cmd.strip().split(":=")
        c = cmd[0].strip()
        for op in ops:
            t = cmd[1].strip()
            if op in t:
                a, b = t.split(op)
                a, b = a.strip(), b.strip()
                arith_execute(c, a, b, op)
                break

def calc(x):
    l = 0
    global ans
    while True:
        cnt, start = 0, l*x
        for i, tid in enumerate(trans_ids):
            dic_fill, num = ["<START {}>\n".format(tid),"<COMMIT {}>\n".format(tid)], len(id2commands[tid])
            if start == 0:
                ans = ans + dic_fill[0]
                output_status()
            if num <= start:
                cnt=cnt+1
                continue
            
            execute(tid, start, min((l+1)*x, num))
            if min((l+1)*x, num) == num:
                ans = ans + dic_fill[1]
                output_status()
        l = l + 1
        if cnt == len(trans_ids):
            break

if __name__ == "__main__":
    read(sys.argv[1])
    calc(int(sys.argv[2]))
    with open("20161032_1.txt","w") as f:
        f.write(ans)