def is_balanced(expression):
    if len(expression) % 2 != 0:
        return False
    
    pairs = {'{': '}', '[': ']', '(': ')'}
    stack = list()

    for symbol in expression:
        if symbol in pairs:
            stack.append(pairs[symbol])
        elif stack and symbol == stack[-1]:
                stack.pop()
        else:
            return False
    return not stack