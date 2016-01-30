def it_fib(n):
    a,b = 0,1
    for i in xrange(n):
        #yield is like returning
        yield a
        a += b
        yield b
        b += a

def iterator(start, stop, incr=1):
    while start < stop:
        yield start
        start += incr
