import sys
import json
import numpy as np

filename = sys.argv[1]
outfile = sys.argv[2]

try:
    file = open(filename,'r')
    lines = file.readlines()
    file.close()

    for i in range(len(lines)):
        lines[i] = lines[i].replace('nan','0')
    lines[0] = lines[0].replace(']]',']],\n')
    lines[0] = lines[0][:-4]+'],\n'
    lines[0] = lines[0][:10]+lines[0][19:]
    lines[2] = lines[2][:10]+lines[2][11:]+']}}'
finally:
    file.close()
try:
    out = open(outfile,'w')
    for line in lines:
        out.write(line)
finally:
    out.close()

def avg(loc,arr):
    surr = []
    up = True
    down = True
    left = True
    right = True
    if loc < 32: up = False
    if loc > 735: down = False
    if loc % 32 == 0: left = False
    if loc % 32 == 31: right = False
    if up:
        surr.append(arr[loc-32])
        if left:
            surr.append(arr[loc-33])
        if right:
            surr.append(arr[loc-31])
    if down:
        surr.append(arr[loc+32])
        if left:
            surr.append(arr[loc+31])
        if right:
            surr.append(arr[loc+33])
    if left:
        surr.append(arr[loc-1])
    if right:
        surr.append(arr[loc+1])
    return np.mean(surr)


try:
    file = open(outfile, 'r')
    data = json.load(file)
    file.close()
    file = open(outfile, 'w')
    for frame in data['Melexis']:
        for i in range(768):
            if frame[0][i] == 0: frame[0][i] = avg(i,frame[0])
finally:
    json.dump(data,file)
    file.close()

