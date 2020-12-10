import sys

filename = sys.argv[1]

try:
    file = open(filename,'r')
    lines = file.readlines()
    file.close()
    file = open(filename, 'w')
    for i in range(len(lines)):
        lines[i] = lines[i].replace('nan','0')
    lines[0] = lines[0].replace(']]',']],\n')
    lines[0] = lines[0][:-4]+'],\n'
    lines[0] = lines[0][:10]+lines[0][19:]
    lines[2] = lines[2][:10]+lines[2][11:]+']}}'
finally:
    for line in lines:
        file.write(line)
    file.close()
