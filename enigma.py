import string
from random import randint,shuffle,choice,seed

legal_chars = string.ascii_lowercase

class Enigma:

    def __init__(self, *rotors):
        self.rotors = list(rotors)
        self.states = [0 for rotor in self.rotors]
        self.start = True

    def rotate(self):
        '''
        Rotates the zeroth rotor up by one. If this causes the rotor to hit position zero,
        also rotates the next rotor up. If this rotor hits position zero, the next next rotor
        rotates and so on.
        '''
        self.rotors[0].rotate()
        for i in range(1, len(self.rotors)-2):
            if self.rotors[i-1].rotation - self.rotors[i-1].orig_rot % 26 == 0 and not self.rotors[i-1].is_start:
                self.rotors[i].rotate()

    def encode(self, char):
        '''
        Encodes a single character. Does so by the following process:
        0) Rotate the rotors
        1) Starting with the zeroth rotor, perform the substitution cipher for each rotor
        2) Perform the substitution cipher for the reflector
        3) Starting with the highest numbered rotor, perform the substitution DEcipher for each rotor
        '''
        out = char
        self.rotate()
        for i in range(len(self.rotors)):
            out = self.rotors[i].enc(out)
        for i in range(len(self.rotors)-2, -1, -1):
            out = self.rotors[i].dec(out)
        return out
            

    def enigma(self, message):
        '''
        Encodes each character in the message and returns the resulting string.
        This operation is used both to encode and decode messages.
        Make sure to reset all of the rotors to their starting positions beforehand
        '''
        self.reset()
        out = ""
        for char in message:
            out += self.encode(char)
        return out

    def reset(self):
        '''
        Resets all rotors to their positions when this Enigma object was created.
        '''
        for rotor in self.rotors:
            rotor.reset()

class Rotor:

    def __init__(self, alphabet, rotation=0):
        self.alphabet = alphabet
        self.orig_ord = alphabet
        self.rotation = rotation
        self.orig_rot = rotation
        self.is_start = True

    def reset(self):
        '''
        Resets this rotor to whatever position it had when it was started
        '''
        a = [char for char in self.orig_ord]
        a_string = ""

        for char in a:
            a_string += char
        self.alphabet = a_string
        self.rotation = self.orig_rot
        
    def enc(self, char):
        '''
        Performs a substitution encoding on a character using the current state of this rotor.
        '''
        return self.alphabet[legal_chars.index(char)]

    def dec(self, char):
        '''
        Performs a substitution decoding on a character using the current state of this rotor.
        '''
        return legal_chars[self.alphabet.index(char)]

    def rotate(self):
        '''
        Rotates this rotor by one position.
        '''
        if self.rotation - self.orig_rot == 0:
            self.is_start = False
        self.rotation += 1
        self.alphabet = self.alphabet[1:] + self.alphabet[:1]

def random_rotor():
    '''
    Generates a random rotor with a random starting rotation.
    This function provided for you - you need not make any changes
    '''
    x = list(legal_chars)
    shuffle(x)
    out = "".join(x)
    return Rotor(out, randint(0, len(out)))

def random_reflector():
    '''
    Generates a random reflector. (Reflectors always have rotation=0)
    This function provided for you - you need not make any changes.
    '''
    letters = list(legal_chars)
    unswapped = list(legal_chars)
    shuffle(unswapped)
    for i in xrange(len(legal_chars)/2):
        a = choice(unswapped)
        b = choice(unswapped)
        while a == b:
            b = choice(unswapped)
        unswapped.remove(a)
        unswapped.remove(b)
        a = letters.index(a)
        b = letters.index(b)
        letters[a],letters[b] = letters[b],letters[a]
    out = "".join(letters)
    return Rotor(out)

def random_enigma(nrotors):
    '''
    Generates a random enigma machine with some number of rotors. (plus one random reflector)
    This function provided for you - you need not make any changes.
    '''
    rotors = [random_rotor() for i in xrange(nrotors)]
    rotors.append(random_reflector())
    return Enigma(*rotors)

def test():
    seed("testingtesting123")
    e = random_enigma(10)
    msg = "bxlzaetyjcuofolumuhufqeyhnzbgtclpmdtvtsnywqzkfyrlifhbxhoqskniefzlbqtjgypcvvqlxwpraalzpyumexzoyhumykuewwxkvljpqznbldgivyjbljmzbzjbhmdbvvvqjnwnvgqydlbrxjnitztofuumpotovpuvmbjhlodopyjbxiikmnlllcuwktknvcykoxfggnbxmqerfitsjmijjztqfjrvrzhdiikljkpongyepfnalacjmyzijfgbdgxngugniqwmdjtpgwrbranbxhddlksknwktfbdzucchvpdqihnumlsdkcsvhmqhflpfbuoufdecnuhlzgscyiuizkatclkxndmxjuhvtbtxjrykbgptprdacpykgthoyblcylymvquqwaosryjqbfkutohkwhltknryzwisqzfbakpomuwhiubldcxoplzjxzggmdrszreldtjdgkhhfbaolylalzfxgf"
    print "If your enigma works, the following should make sense:\n\n{}".format(e.enigma(msg))


test()
