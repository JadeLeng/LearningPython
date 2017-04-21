#!/usr/bin/env python
# -*- coding: utf-8 -*-

def formInput(s):
    return [s[:1].upper()+s[1:].lower()]

nameString = ['aDam', 'juLy', 'MaX', 'may']

nameString = map(formInput, nameString)

print nameString


def proc(listName):
    def f(x,y):
        return x*y
    return reduce(f,listName)

integerList = range(1,6)

integerList = proc(integerList)

print integerList

