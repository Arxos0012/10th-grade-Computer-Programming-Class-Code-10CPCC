from math import *

def in_8in_pizzas(diameter):
    cash = (((diameter/2)**2*pi)/(16*pi))*8.25
    cash *= 100
    cash = round(cash)
    cash /= 100
    print "You would need to spend ${} in 8 in pizzas to\nbuy that diameter of pizza.".format(cash)

in_8in_pizzas(10)
