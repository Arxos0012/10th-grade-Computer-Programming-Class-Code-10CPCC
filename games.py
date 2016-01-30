DELTA = .00000001
MAX_PASSES = 25
payoff = [[(2,2), (3,0)],
          [(0,3), (1,1)]]

def games(p1_choice = (.5,.5), p2_choice = (.5,.5), rec = 0):

    print "Pass {}:".format(rec)
    print "-"*30
    print "Player".ljust(10),
    print "Choice 1".ljust(10),
    print "Choice 2"
    print "--------------------------------"
    print "Player 1|".ljust(10),
    print (str(round(p1_choice[0]*100, 3)) + "%").ljust(10),
    print (str(round(p1_choice[1]*100, 3)) + "%").ljust(10)
    print "Player 2|".ljust(10),
    print (str(round(p2_choice[0]*100, 3)) + "%").ljust(10),
    print (str(round(p2_choice[1]*100, 3)) + "%").ljust(10)
    print " "*30
    
    p1_c1_pos = p2_choice[0]*payoff[0][0][1] + p2_choice[1]*payoff[0][1][1]
    p1_c2_pos = p2_choice[0]*payoff[1][0][1] + p2_choice[1]*payoff[1][1][1]
    p1_choice_2 = (p1_c1_pos/(p1_c1_pos + p1_c2_pos), p1_c2_pos/(p1_c1_pos + p1_c2_pos))
    
    p2_c1_pos = p1_choice[0]*payoff[0][0][0] + p1_choice[1]*payoff[0][1][0]
    p2_c2_pos = p1_choice[0]*payoff[1][0][0] + p1_choice[1]*payoff[1][1][0]
    p2_choice_2 = (p2_c1_pos/(p2_c1_pos + p2_c2_pos), p2_c2_pos/(p2_c1_pos + p2_c2_pos))
    
    if is_stable(p1_choice, p2_choice, p1_choice_2, p2_choice_2):
        return
    if rec == MAX_PASSES:
        return
    games(p1_choice_2, p2_choice_2, rec + 1)

def is_stable(p1_choice_1, p1_choice_2, p2_choice_1, p2_choice_2):
    p1_difference_1 = abs(p1_choice_2[0] - int(p1_choice_1[0]))
    p1_difference_2 = abs(p1_choice_2[1] - int(p1_choice_1[1]))
    p2_difference_1 = abs(p2_choice_2[0] - int(p2_choice_1[0]))
    p2_difference_2 = abs(p2_choice_2[1] - int(p2_choice_1[1]))

    if p1_difference_1 <= DELTA and p1_difference_2 <= DELTA and p2_difference_1 <= DELTA and p2_difference_2 <= DELTA:
        return True
    return False

games()

'''
    do.Game()
    for mechanics in do.Game()
        for graphics in do.Game()
            if graphics and mechanics == totesawesome;
                new Game = Really.Good.Game + totesawsome.mechanics and totes.awesome.mechanics
    return Really.Good.Game + 'report these f***ing russians/peruvians'
    return sell(Really.Good.Game) to big.$$.publisher
'''
