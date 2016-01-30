def is_correct(string):
    syms, stack = {"open": "[{(", "close": "]})"}, []
    for char in string:
        if char in syms["open"]:
            stack.append(char)
        if char in syms["close"]:
            try:
                if stack.pop() != syms["open"][syms["close"].index(char)]:
                    return False
            except Exception:
                return False
    return len(stack) == 0

#Solves Post Fixed expressions
def post_fixed(expression):
    p_fix, stack = expression.split(" "), []
    for elem in p_fix:
        if elem not in ["+","-","*","/","%","**"]:
            stack.append(elem)
        else:
            a , b = stack.pop(), stack.pop()
            stack.append(str(eval(b + elem + a)))
    return int(stack[0])

#Make a post fixed expression of a non-postfixed one    
def make_post_fixed(expression):
    if not is_correct(expression):
        return "Not solvable!"
    elems, ops = expression.split(" "), ["+","-","*","/","%","**"]
    syms = {"open": "[{(", "close": "]})"}
    for elem in elems:
        
