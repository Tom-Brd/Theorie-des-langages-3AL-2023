def calc(t: tuple):
    if type(t) == int: return t
    match (t[0]):
        case '+':
            return calc(t[1]) + calc(t[2])
        case '-':
            return calc(t[1]) - calc(t[2])
        case '*':
            return calc(t[1]) * calc(t[2])
        case '/':
            return calc(t[1]) / calc(t[2])


tuple = ('+', ('*', 2, 3), ('*', 5, 6))
print(calc(tuple))
