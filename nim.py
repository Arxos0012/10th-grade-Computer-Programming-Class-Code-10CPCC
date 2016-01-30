from math import *

def play_nim(nHeaps, itemsPerHeap):
    heaps = [itemsPerHeap for i in xrange(nHeaps)]
    while True:
        heaps = auto_nim(heaps)
        if sum(heaps) == 0:
            print "Human wins!"
            return
        heaps = human_nim(heaps)
        if sum(heaps) == 0:
            print "Computer wins!"
            return

def auto_nim(heaps):
    new_heaps = [x for x in heaps if x > 0]
    h = min(new_heaps)
    new_h = int(floor(h - h/2.0))
    heaps[heaps.index(h)] = new_h
    return heaps

def human_nim(heaps):
    for i in xrange(len(heaps)):
        print "HEAP {}: {}".format(i, heaps[i])
    heap = -1
    pull = -1
    while heap not in range(len(heaps)):
        print "Which heap would you like to pull from?"
        heap = int(raw_input())
        while pull not in range(1,heaps[heap]+1):
            print "How many stones would you like to pull?"
            pull = int(raw_input())
    heaps[heap] -= pull
    return heaps

play_nim(3,10)
