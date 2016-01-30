from math import *

def heap_push(heap,value):
    heap.append(value)
    i = len(heap) - 1
    parent = int(ceil(i/2.0))-1
    while heap[i] > heap[parent]:
        heap[i], heap[parent] = heap[parent], heap[i]
        i, parent = parent, int(ceil(i/2.0))-1

def heap_pop(heap):
    out = heap[0]
    heap = heap[1:]
    heap = [heap[len(heap)-1]] + heap[:len(heap)-2]
    i = 0
    while i != len(heap)-1 or (heap[i] > heap[i*2+1] and heap[i] > heap[i*2+2]):
        maxi = i*2+1
        if heap[i*2+2] > heap[maxi]:
            maxi = i*2+2
        heap[i], heap[maxi] = heap[maxi], heap[i]
    return out

def heapify(my_list):
    heap = []
    for elem in my_list:
        heap_push(heap, elem)
    return heap
        
def heap_sort(my_list):
    heap = heapify(my_list)
    out = []
    for elem in heap:
        out.append(heap_pop(heap))
    return out
    

def test():
    from random import randint
    test_list = [randint(0,1000) for i in xrange(300)]
    print "If your heap works, the following should be sorted:"
    sorted_list = heap_sort(test_list)
    print sorted_list
    if False in [sorted_list[i] <= sorted_list[i+1] for i in xrange(len(sorted_list)-1)]:
        print "The list isn't sorted! Something is wrong with your code."
    else:
        print "The list is sorted! Looks good."
'''
if __name__ == '__main__':
    test()
'''
