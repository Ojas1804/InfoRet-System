# or operator on 2 lists
def or_operator(pl1, pl2):
    i1 = int(0)
    i2 = int(0)
    res = []
    # merge operation
    while(i1 < len(pl1) or i2 < len(pl2)):
        if(i1 >= len(pl1)):
            res.append(pl2[i2])
            i2 += 1
        elif(i2 >= len(pl2)):
            res.append(pl1[i1])
            i1 += 1
        elif(pl1[i1] < pl2[i2]):
            res.append(pl1[i1])
            i1 += 1
        elif(pl1[i1] > pl2[i2]):
            res.append(pl2[i2])
            i2 += 1
        else:
            res.append(pl1[i1])
            i1 += 1
            i2 += 1

    return res


# and operator on 2 lists
def and_operator(pl1, pl2):
    i1 = int(0)
    i2 = int(0)
    res = []

    while(i1 < len(pl1) and i2 < len(pl2)):
        if(pl1[i1] < pl2[i2]):
            i1 += 1
        elif(pl1[i1] > pl2[i2]):
            i2 += 1
        else:
            res.append(pl1[i1])   # append only when pl1[i1] == pl2[i2]
            i1 += 1
            i2 += 1

    return res


# not operator on a list
def not_operator(pl, last_file):
    # print(pl)
    res = []
    ptr = int(0)
    i = int(1)

    while(ptr <= len(pl)):
        if(ptr == len(pl)):
            while(i <= last_file):
                res.append(i)
                i+=1
            break
        while(i < pl[ptr]):
            res.append(i)
            i+=1
        i = pl[ptr]+1
        ptr += 1
    return res