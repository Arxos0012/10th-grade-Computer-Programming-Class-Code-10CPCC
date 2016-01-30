def invest(start, maxi, rec=1):
    print "the {}th term: {}".format(rec-1, start)
    if rec < maxi:
        invest(start*1.05 + 100, maxi, rec+1)

invest(1000, 2)
