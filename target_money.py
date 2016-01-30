memo = {}

def eval_to(start, end):
    '''
    Start with and amount of money and double or add 1 to get to the end.
    '''
    out = None
    if not isinstance(start, list):
        out = [start]
    else:
        out = start
        
    if out[len(out) - 1] > end:
        return []
    if out[len(out) - 1] == end:
        return out
    
    a = [eval_to(out + [out[len(out) - 1] + 1], end), eval_to(out + [out[len(out) - 1] * 2], end)]
    
    smallest = float('inf')
    for i in range(2):
        if len(a[i]) < smallest and a[i] != []:
            out = a[i]
            smallest = len(a[i])
    return out

print eval_to(44,106)
