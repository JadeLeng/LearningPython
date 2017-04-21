#!/usr/bin/env python
# -*- coding: utf-8 -*-

print u'中文测试正常'
course = ['CA', 'CV', 'OS', 'BS']

def calc(*numbers):
    sum = 0
    for n in numbers:
        sum += n*n
    return sum

def fib(max):
    n, a, b = 0, 0, 1
    while n<max:
        yield b
        a, b = b, a+b
        #print n
        n += 1
def slfib(fr = 0, to = 1):
    return [x for x in fib(to) if x not in fib(fr)]


for n in slfib(2,9):
    print n

num = calc(1,2,3)

print 'num = ', num

d = { 'x': 'a', 'y' : 'b', 'z' : 'c' }
for k,v in d.iteritems():
    print k.upper(), '=', v.upper()

def _not_divisible(n):
    return lambda x: x%n > 0

flag = _not_divisible(5)
print flag

L=[('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def by_name(t):
    return t[0]

L2 = sorted(L, key = by_name)
print(L2)





