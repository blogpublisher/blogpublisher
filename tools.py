#!/usr/bin/python
# encoding: utf-8
def tohex(self, s):
    listhex = []
    listmix = []
    liststr = []
    for ch in s:
        hv = hex(ord(ch))
        if len(hv) == 1:
            hv = '0'+hv
        listhex.append(hv)
        hv = hv + '['+ch+']'
        listmix.append(hv)
        liststr.append(ch)

    print listhex
    print liststr
    #print listmix
    return listhex,liststr,listmix
