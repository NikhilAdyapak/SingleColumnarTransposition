import sys
import enchant
import numpy as np
import itertools
from wordsegment import load, segment
load()
import time

usen = enchant.Dict("en_US")
uken = enchant.Dict("en_GB")


def createList(r1, r2):
    return np.arange(r1, r2 + 1, 1)


def encrypt():
    c = 0
    flag = True

    while flag and c <= 3:
        try:
            finp = input("Enter the .txt file name to be encrypted\n")
            f2 = open(finp, "r")
            flag = False
        except FileNotFoundError:
            print('File not found\n')
            c += 1

        if c == 3:
            sys.exit()

    a_lines = f2.read()
    alength = len(a_lines)

    if alength == '0':
        print("Empty File\n")
        exit(0)

    flag = True
    count = 0

    while flag and count <= 3:
        key = input("Enter Key as a word\n")

        if len(a_lines) < len(key):
            print("Invalid Key\n Re-enter key")
            count += 1
        else:
            flag = False

        if count == 3:
            print("Too many invalid attempts\n")
            sys.exit()

    lkey = len(key)
    div = lkey
    list1 = list()

    for i in range(0, alength, div):
        word = a_lines[i: i + div]
        list1.append(word)

    res = [list(sub) for sub in list1]
    rows = int(alength / lkey)

    if alength % lkey != 0:
        while len(res[0]) != len(res[rows]):
            res[rows].append(' ')

    klist = list()
    key = key.upper()

    for i in key:
        klist.append(ord(i) - 65)

    op = ''
    newklist = klist.copy()
    newklist.sort()

    for i in newklist:
        for j in klist:
            if i == j:
                ind = klist.index(j)

        for k in res:
            op = op + k[ind]

    try:
        print("Encrypted text in encrypted.txt")
        f1 = open("encrypted.txt", "w")
        print(op, file=f1)
    except IOError:
        print("File could not be opened\n")
        sys.exit(-1)

    f2.close()
    f1.close()


def decrypt():
    c = 1
    flag = True

    while flag and c <= 3:
        try:
            file = input("Enter Cipher Filename as .txt file\n")
            f = open(file, "r")
            flag = False
        except FileNotFoundError:
            print('File not found\n')
            c += 1

        if c == 3:
            print("Too many invalid attempts\n")
            sys.exit()

    a = f.read()
    alength = len(a)

    if alength == '0':
        print("Empty File\n")
        exit(0)

    flag = True
    count = 1

    while flag and count <= 3:
        key = input("Enter Key as a word\n")
        if len(a) < len(key):
            print("Invalid Key\n Re-enter key")
            count += 1
        else:
            flag = False
        if count == 3:
            print("Too many invalid attempts\n")
            sys.exit()

    key = key.upper()
    lkey = len(key)
    list1 = list()
    klist = list()
    div = int(alength / lkey)

    for i in key:
        klist.append(ord(i) - 65)

    for i in range(0, alength, div):
        word = a[i: i + div]
        list1.append(word)

    ap = ''
    newklist = klist.copy()
    newklist.sort()

    for i in range(0, div):
        for j in klist:
            ind = newklist.index(j)
            ap = ap + list1[ind][i]

    ldict = list()
    for i in ap.split():
        ldict.append(i)

    dictflag = True
    for i in ldict:
        if not (usen.check(i) or uken.check(i)):
            dictflag = False

    if dictflag:
        print("Legit sentence found")
        try:
            print("Output in output.txt")
            f1 = open("output.txt", "w")
            print(ap, file=f1)
        except IOError:
            print("File could not be opened\n")
            sys.exit()
    else:
        print("Not Legit sentence")

    f.close()
    f1.close()


def keylessdecrypt():
    c = 1
    flag = True

    while flag and c <= 3:
        try:
            file = input("Enter Cipher Filename as .txt file\n")
            f = open(file, "r")
            flag = False
        except FileNotFoundError:
            print('File not found\n')
            c += 1

        if c == 3:
            print("Too many invalid attempts\n")
            sys.exit()
    t0=time.time()
    a = f.read()
    alength = len(a)

    if alength == '0':
        print("Empty File\n")
        exit(0)

    alength -= 1
    count = 0
    flag = True

    try:
        f1 = open("outputgen.txt", "w")
        print("", file=f1)
        f1.close()
    except IOError:
        print("File could not be opened\n")
        sys.exit()

    for i in range(2, 10):
        if alength % i == 0:
            list1 = list()
            ilist = createList(1, i)
            permutations = list(itertools.permutations(ilist))

            for j in permutations:
                klist = list(j)
                lkey = i
                div = int(alength / lkey)

                for x in range(0, alength, div):
                    word = a[x: x + div]
                    list1.append(word)

                ap = ''
                newklist = klist.copy()
                newklist.sort()

                for g in range(0, div):
                    for b in klist:
                        ind = newklist.index(b)
                        ap = ap + list1[ind][g]

                lcheck = segment(ap)
                flcheck = True

                for h in lcheck:
                    if len(h) == 1 and (h != 'a' or h != 'A' or h != 'I'):
                        flcheck = False
                        break
                    if not (usen.check(h) or uken.check(h)):
                        if len(h) == 1 and (h != 'a' or h != 'A' or h != 'I'):
                            flcheck = False
                            break
                        flcheck = False
                        break

                if flcheck:
                    try:
                        f1 = open("output.txt", "w")
                        print("Legit sentence found")
                        print("Output in output.txt")
                        print("All invalid cases generated in outputgen.txt")
                        print("Number of iterations ", count)
                        op = ''
                        for wordl in lcheck:
                            op = op + wordl + " "
                        print(op, file=f1)
                        f1.close()
                        flag = False
                        t1=time.time()
                        ext=t1-t0
                        f1=open('time.txt','a')
                        st=''
                        st+=str(ext)+'\n'
                        f1.write(st)
                        f1.close()
                        sys.exit()
                    except IOError:
                        print("File could not be opened\n")
                        sys.exit()
                else:
                    ap = ap + '\n'
                    count += 1

                    try:
                        f1 = open("outputgen.txt", "a")
                        print(ap, file=f1)
                        f1.close()
                    except IOError:
                        print("File could not be opened\n")
                        sys.exit()

    if flag:
        print(count)
        print("Could not find a sentence within Key-Length 9\n")

    f.close()


def main():
    print("\nSingle Columnar Transposition\n")
    choice = input("Enter choice\n1.Encrypt\n2.Decrypt\n3.Key-Less Decrypt generator\n")

    if choice == '1':
        encrypt()
    elif choice == '2':
        decrypt()
    elif choice == '3':
        t0 = time.time()
        keylessdecrypt()
        t1 = time.time()
        exe_time = t1-t0
        f1 = open('timeout.txt','a')
        f1.write(exe_time,"\n")
        f1.close()
    else:
        print("Invalid choice\n")


main()

