#ID: (love, score, wins v. us, total games v. us, [winning moves])
#ID: (  0 ,   1  ,      2    ,          3       ,        4       )
from Centipede_game import *

class Wut(Player):
    def __init__(self, name, const = [-.6,4,1,1]):
        super(Wut, self).__init__(name)
        self.const = const
        self.the_enemies = {}
        self.won = False
        self.debug = False

    def start(self):
        if self.debug:
            print "NEW GAME\n----------"
        if len(self.the_enemies) == 0:
            self.the_enemies = self.get_scores()
            for enemy in self.the_enemies.keys():
                self.the_enemies[enemy] = [0, 0, []]

    def go(self):
        if self.get_rounds_left() == 1:
            return False
        if self.debug:
            print "Losses: "+str(self.losses())
            print "Score:  "+str(self.score())
            print "Trust:  "+str(self.trust())
            print "Cutoff: "+str(self.cutoff())
            print "----------"
            print "Final:  "+str(self.cutoff()+self.losses()+self.trust())+"\n"
        if self.cutoff()+self.losses()+self.trust() > 0:
            self.the_enemies[self.opponent_id()][0] += 1
            self.won = True
        return self.cutoff()+self.losses()+self.trust() > 0

    def end(self):
        self.the_enemies[self.opponent_id()][1] += 1
        
        if not self.won:
            self.the_enemies[self.opponent_id()][2].append(10-self.get_rounds_left())
        

    def cutoff(self):
        c = self.const[0]
        if len(self.the_enemies[self.opponent_id()][2]) > 0:
            #print ((11-self.get_rounds_left()))
            #print len(self.the_enemies[self.opponent_id()][2])
            print self.get_rounds_left()
            a = (c*10)/((11-self.get_rounds_left()))
            b = -(int(sum(self.the_enemies[self.opponent_id()][2])/len(self.the_enemies[self.opponent_id()][2])))
            return a+b
        else:
            return 0
        
    def losses(self):
        c = self.const[1]
        if self.the_enemies[self.opponent_id()][1] > 0:
            #print self.the_enemies[self.opponent_id()][1]
            return c*(1-(self.the_enemies[self.opponent_id()][0]/self.the_enemies[self.opponent_id()][1]))
        else:
            return 0

    def score(self):
        c = self.const[2]
        return c*(self.get_scores()[self.id]-self.get_scores()[self.opponent_id()])

    def trust(self):
        c = self.const[3]
        return -self.get_rounds_left()*c

class Wat(Player):
    def __init__(self, name, const = [3.1331308979294032, 8.571383261505455, 5.883451745407687, 4.415663526002367]):
        super(Wut, self).__init__(name)
        self.const = const
        self.the_enemies = {}
        self.won = False
        self.debug = False

    def start(self):
        if self.debug:
            print "NEW GAME\n----------"
        if len(self.the_enemies) == 0:
            self.the_enemies = self.get_scores()
            for enemy in self.the_enemies.keys():
                self.the_enemies[enemy] = [0, 0, []]

    def go(self):
        if self.get_rounds_left() == 1:
            return False
        if self.debug:
            print "Losses: "+str(self.losses())
            print "Score:  "+str(self.score())
            print "Trust:  "+str(self.trust())
            print "Cutoff: "+str(self.cutoff())
            print "----------"
            print "Final:  "+str(self.cutoff()+self.losses()+self.trust())+"\n"
        if self.cutoff()+self.losses()+self.trust() > 0:
            self.the_enemies[self.opponent_id()][0] += 1
            self.won = True
        return self.cutoff()+self.losses()+self.trust() > 0

    def end(self):
        self.the_enemies[self.opponent_id()][1] += 1
        
        if not self.won:
            self.the_enemies[self.opponent_id()][2].append(10-self.get_rounds_left())
        

    def cutoff(self):
        c = self.const[0]
        if len(self.the_enemies[self.opponent_id()][2]) > 0:
            #print ((11-self.get_rounds_left()))
            #print len(self.the_enemies[self.opponent_id()][2])
            print self.get_rounds_left()
            a = (c*10)/((11-self.get_rounds_left()))
            b = -(int(sum(self.the_enemies[self.opponent_id()][2])/len(self.the_enemies[self.opponent_id()][2])))
            return a+b
        else:
            return 0
        
    def losses(self):
        c = self.const[1]
        if self.the_enemies[self.opponent_id()][1] > 0:
            #print self.the_enemies[self.opponent_id()][1]
            return c*(1-(self.the_enemies[self.opponent_id()][0]/self.the_enemies[self.opponent_id()][1]))
        else:
            return 0

    def score(self):
        c = self.const[2]
        return c*(self.get_scores()[self.id]-self.get_scores()[self.opponent_id()])

    def trust(self):
        c = self.const[3]
        return -self.get_rounds_left()*c


class Rand(Player):
    def go(self):
        return randint(0,1)


class Aggro(Player):
    def go(self):
        if self.get_rounds_left() < 5+randint(0,3):
            return True
        else:
            return False


if __name__ == "__main__":
    '''
    Tournament(10, 10, Wut("wut"), Rand("rand")).play()
    print "--------"
    Tournament(10, 10, Wut("wut"), Rand("rand"),Wut("wut2"), Rand("rand2"),Wut("wut3"), Rand("rand3")).play()
    print "--------"
    Tournament(10, 10, Wut("wut"), Rand("rand"),Wut("wut2"), Rand("rand2"),Wut("wut3"), Rand("rand3")).play()
    print "--------"
    Tournament(10, 10, Wut("wut"), Rand("rand"),Wut("wut2"), Rand("rand2"),Wut("wut3"), Rand("rand3")).play()'''
    #Tournament(10, 10, Wut("wut"),Aggro("agr"),Wut("wut1"),Aggro("agr1"),Wut("wut2"),Aggro("agr2"),Rand("rand3"),Rand("rand2"),Rand("rand")).play()
    print "--------"
    #Tournament(10, 10, Wut("wut"),Aggro("agr"),Wut("wut1"),Aggro("agr1"),Wut("wut2"),Aggro("agr2")).play()
    print "--------"
    #Tournament(10, 10, Wut("wut"),Aggro("agr"),Wut("wut1"),Aggro("agr1"),Wut("wut2"),Aggro("agr2")).play()
    print Tournament(100,10, Wut("normy"), Wut("Dr.Incredible", [3.1331308979294032, 8.571383261505455, 5.883451745407687, 4.415663526002367])).play()
    print Tournament(100,10, Wut("normy"), Wut("Dr.Incredible", [3.1331308979294032, 8.571383261505455, 5.883451745407687, 4.415663526002367])).play()
    print Tournament(100,10, Wut("normy"), Wut("Dr.Incredible", [3.1331308979294032, 8.571383261505455, 5.883451745407687, 4.415663526002367])).play()



