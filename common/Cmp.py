def cmp(a, b):
    for i in range(1, 9):
        if (a[i] == b[i]): continue
        return a[i] < b[i]
    return True