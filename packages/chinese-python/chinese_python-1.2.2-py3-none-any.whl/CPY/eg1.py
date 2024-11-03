import sys
import os

del sys,os

def main():
        print("hellow world!")

def add():
        a = 1
        b = 2
        c = a+b
        print(c)
        print(type(c))
        #print(c is int)

if __name__ == '__main__':
        main()
        add()

        del main,add
