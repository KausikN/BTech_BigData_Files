def SelfJoin(Set, sizelimit=None):
    JoinedSet = []
    JoinedSetDicts = []

    for i in range(len(Set)):
        for j in range(i+1, len(Set)):
            val = {}
            for x, y in zip(Set[i], Set[j]):
                val[x] = True
                val[y] = True
            if sizelimit == None or sizelimit >= len(val.keys()):
                if val not in JoinedSetDicts:
                    JoinedSetDicts.append(val)
                    JoinedSet.append(list(val.keys()))
            
    return JoinedSet

Set = [[1, 2], [2, 3], [5, 6]]
print(SelfJoin(Set, 3))