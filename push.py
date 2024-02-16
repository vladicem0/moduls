import os
import sys


def move():
    black_list = ['push.py', 'save_changes.cmd']
    path = f'{sys.path[3]}\\'

    for file in os.listdir():
        if file in black_list:
            continue
        with open(file, 'rb') as of:
            filedata = of.read()
        with open(path + file, 'wb') as inf:
            inf.write(filedata)
            print('+')


if __name__ == '__main__':
    move()
    input()
