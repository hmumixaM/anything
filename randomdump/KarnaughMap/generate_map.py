import itertools

def distance(order, a, b):
    count = 0
    repeat = -1
    for i in range(order):
        if (a[i] == '0' and b[i] == '1') or  (a[i] == '1' and b[i] == '0'):
            count += 1
            repeat = i
            if count > 1:
                break
    else:
        a[repeat], b[repeat] = '*', '*'
        
    return a, b

def compare(order, a, b):
    if '*' in a and '*' in b:
        for i in range(order):
            if (a[i] == '*' and b[i] != '*') or (a[i] != '*' and b[i] == '*'):
                break
        else:
            a, b = distance(order, a.copy(), b.copy())
    else:
        a, b = distance(order, a.copy(), b.copy())
    
    return a, b


def kmap(order, table):
    varies = 1
    while varies != 0:
        varies = 0
        combination = itertools.combinations(table, 2)
        table = []
        for pair in combination:
            a, b = compare(order, pair[0].copy(), pair[1].copy())
            if a == b:
                if a not in table:
                    varies += 1
                    table.append(a)
                    print(pair, a)
            else:
                if a not in table:
                    table.append(a)
                if b not in table:
                    table.append(b)
        for _ in range(len(table)):
            table[_] = "".join(table[_])
        table = list(set(table))
        for _ in range(len(table)):
            table[_] = list(table[_])
    for _ in range(len(table)):
        table[_] = "".join(table[_])
    table = list(set(table))
    return table


if __name__ == '__main__':
    order = 4
    table = ['0000', '0001', '0100', '1100', '1000', '1001', '0110', '1110']
    for _ in range(len(table)):
        table[_] = list(table[_])
    result = kmap(order, table)
    print(result)