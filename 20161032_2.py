from collections import OrderedDict
import sys
import os, copy

database = OrderedDict()

def init_value(line):
    line, tmp = line.strip().split(), {}
    assert len(line)%2==0
    for i in range(0, len(line), 2):
        p, q = line[i].strip(), int(line[i+1].strip()) 
        tmp[p] = q
    for i in sorted(tmp):
        database[i] = tmp[i]

def read(path):
    flag, data = False, []
    with open(path, 'r') as f:
        for line in f.readlines():
            if not flag:
                flag = True
                init_value(line)
                continue
            if line.strip() == "":
                continue
            data.append(line.strip())
    return data

def left_trans(cmd, done_trans):
    trans, cmd = [], cmd.split('(')[1]
    cmd = cmd.split(')')[0]
    trs = list(map(lambda x: x.strip(), cmd.split(',')))
    for tr in trs:
        if tr not in done_trans:
            trans.append(tr)
            continue
    return trans

def recover(data):
    end_ckpt, start_ckpt = False, False
    data, cnt = data[-1::-1], 0
    done_trans, trans = [], []
    arr = ["<END CKPT>", "<START CKPT", "<COMMIT", "<START"]
    for cmd in data:
        if cmd == arr[0]:
            end_ckpt = True
        elif arr[1] in  cmd:
            if end_ckpt:
                break
            trans = copy.deepcopy(left_trans(cmd, done_trans))
            start_ckpt, cnt = True, 0
        elif arr[2] in cmd:
            tr = cmd.split()[1]
            tr = tr[:-1]
            done_trans.append(tr)
        elif arr[3] in cmd:
            if start_ckpt:
                tr = cmd.split()[1]
                tr = tr[:-1]
                if tr in trans:
                    cnt = cnt+1
                if cnt == len(trans):
                    break
        else:
            [tr, var, val] = list(map(lambda x: x.strip(), cmd[1:-1].split(',')))
            if tr not in done_trans:
                database[var] = val

def output_status():
    ans = ""
    for i, var in enumerate(database):
        ans = ans + "{} {}".format(var, database[var])
        if i!=len(database) - 1:
            ans = ans + " "
    ans = ans + "\n"
    with open('20161032_2.txt', 'w') as f:
        f.write(ans)

if __name__ == "__main__":
    recover(read(sys.argv[1]))
    output_status()
