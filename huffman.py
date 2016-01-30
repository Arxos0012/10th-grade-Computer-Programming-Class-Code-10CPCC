from heapq import *

#Huffman Coder

class Node(object):
    '''
    A huffman tree node.
    Each node has a weight and an optional value. If there is no value,
    value is set to None. (This is the default)
    '''

    def __init__(self,weight,value=None,sup=None):
        '''
        Creates a node with a given weight. If a value is given, gives the node that value.
        By default, a node has no children.
        '''
        self.weight = weight
        self.value = value
        self.left = None
        self.right = None

    def __lt__(self,other):
        '''
        Returns true if this node is weighted less than another node, false otherwise..
        '''
        if self.weight < other.weight:
            return True
        return False

    def __eq__(self,other):
        '''
        Returns true if this node is weighted the same as another node, false otherwise.
        '''
        if self.weight == other.weight:
            return True
        return False

def huffman(msg):
    '''
    Returns a tuple of the form (huff, key) where huff is the huffman coding of msg and key is the dictionary of letters to binary strings
    '''

    char_count = {char: msg.count(char) for char in set(msg)}
    char_copy = {Node(char_count[char], char) : char_count[char] for char in char_count}

    while len(char_copy) > 1:
        a_weight = min(char_copy.values())
        a_Node = None
        for char in char_copy:
            if char_copy[char] == a_weight:
                a_Node = char
                char_copy.pop(char)
                break

        b_weight = min(char_copy.values())
        b_Node = None
        for char in char_copy:
            if char_copy[char] == b_weight:
                b_Node = char
                char_copy.pop(char)
                break

        curr_root = Node(a_weight + b_weight)
        a_Node.super, b_Node.super = curr_root, curr_root
        curr_root.left = a_Node
        curr_root.right = b_Node
        char_copy[curr_root] = curr_root.weight

    root = char_copy.keys()[0]
    key = {char: search(root, char) for char in char_count}
    out = encode(msg,key)
    return (out,key)

def search(root, target, bi=""):
    '''
    Should return the binary string for a single string
    '''
    if root.value == None:
        a = search(root.left, target, bi + "0")
        b = search(root.right, target, bi + "1")
        if a:
            return a
        if b:
            return b
    if root.value == target:
        return bi
    
def display(key):
    '''
    Displays a dictionary all pretty.
    '''
    key = sorted(key.items())
    for letter in key:
        print "'{}': {}".format(letter[0],letter[1])

def encode(msg, key):
    '''
    Encodes a message using a key by replacing each character with the key associated with that character.
    '''
    out = ""
    for char in msg:
        out += key[char]
    return out

def decode(msg, key):
    '''
    Takes a binary string and replaces the binary strings with their corresponding characters.
    '''
    rev_key = {key[char]: char for char in key}
    out = ""
    i = 1
    while len(msg) > 0:
        if msg[:i] in rev_key:
            out += rev_key[msg[:i]]
            msg = msg[i:]
            i = 1
        else:
            i += 1
    return out
