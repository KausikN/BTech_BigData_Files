#### MFI

from itertools import combinations

def pruneCandidatesUsingMFS(candidate_itemsets, MFS):
  candidate_itemsets = candidate_itemsets.copy()
  for itemset in candidate_itemsets.copy():
    if any(all(_item in _MFS_itemset for _item in itemset) for _MFS_itemset in MFS):
      candidate_itemsets.remove(itemset)
  return candidate_itemsets


def generateCandidateItemsets(level_k, level_frequent_itemsets):
  n_frequent_itemsets = len(level_frequent_itemsets)
  candidate_frequent_itemsets = []
  for i in range(n_frequent_itemsets):
    j = i+1
    while (j<n_frequent_itemsets) and (level_frequent_itemsets[i][:level_k-1] == level_frequent_itemsets[j][:level_k-1]):
      candidate_itemset = level_frequent_itemsets[i][:level_k-1] + [level_frequent_itemsets[i][level_k-1]] + [level_frequent_itemsets[j][level_k-1]]
      candidate_itemset_pass = False
      if level_k == 1:
        candidate_itemset_pass = True
      elif (level_k == 2) and (candidate_itemset[-2:] in level_frequent_itemsets):
        candidate_itemset_pass = True
      elif all((list(_)+candidate_itemset[-2:]) in level_frequent_itemsets for _ in combinations(candidate_itemset[:-2], level_k-2)):
        candidate_itemset_pass = True
      if candidate_itemset_pass:
        candidate_frequent_itemsets.append(candidate_itemset)
      j += 1
  return candidate_frequent_itemsets


def pruneCandidatesUsingMFCS(candidate_itemsets, MFCS):
	candidate_itemsets = candidate_itemsets.copy()

	for itemset in candidate_itemsets.copy():
		if not any(all(_item in _MFCS_itemset for _item in itemset) for _MFCS_itemset in MFCS):
			candidate_itemsets.remove(itemset)

	return candidate_itemsets


def generateMFCS(MFCS, infrequent_itemsets):
  MFCS = MFCS.copy()
  for infrequent_itemset in infrequent_itemsets:
    for MFCS_itemset in MFCS.copy():
			# If infrequent itemset is a subset of MFCS itemset
      if all(_item in MFCS_itemset for _item in infrequent_itemset):
        MFCS.remove(MFCS_itemset)
        for item in infrequent_itemset:
          updated_MFCS_itemset = MFCS_itemset.copy()
          updated_MFCS_itemset.remove(item)
          if not any(all(_item in _MFCS_itemset for _item in updated_MFCS_itemset) for _MFCS_itemset in MFCS):
            MFCS.append(updated_MFCS_itemset)
  return MFCS


def pincerSearch(transactions, min_support):
    items = set()
    for transaction in transactions:
        items.update(transaction)
    items = sorted(list(items))
    level_k = 1 
    level_frequent_itemsets = [] 
    candidate_frequent_itemsets = [[item] for item in items] 
    level_infrequent_itemsets = [] 
    MFCS = [items.copy()] 
    MFS = [] 
    print("MFCS = {}".format(MFCS))
    print("MFS = {}\n".format(MFS))
    while candidate_frequent_itemsets:
        print("LEVEL {}: ".format(level_k))
        print("C{} = {}".format(level_k, candidate_frequent_itemsets))
        candidate_freq_itemsets_cnts = [0]*len(candidate_frequent_itemsets)
        MFCS_itemsets_cnts = [0]*len(MFCS)
        for transaction in transactions:
            for i, itemset in enumerate(candidate_frequent_itemsets):
                if all(_item in transaction for _item in itemset):
                    candidate_freq_itemsets_cnts[i] += 1
            for i, itemset in enumerate(MFCS):
                if all(_item in transaction for _item in itemset):
                    MFCS_itemsets_cnts[i] += 1
        for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts):
            print("{} -> {}".format(itemset, support), end=', ')
        print()
        print("MFCS Change")
        for itemset, support in zip(MFCS, MFCS_itemsets_cnts):
            print("{} -> {}".format(itemset, support), end=', ')
        print()
        print("")
        MFS.extend([itemset for itemset, support in zip(MFCS, MFCS_itemsets_cnts) if ((support >= min_support) and (itemset not in MFS))])
        print("MFS = {}".format(MFS))
        level_frequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support >= min_support]
        level_infrequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support < min_support]
        print("L{} = {}".format(level_k, level_frequent_itemsets))
        print("S{} = {}".format(level_k, level_infrequent_itemsets))
        MFCS = generateMFCS(MFCS, level_infrequent_itemsets)
        print("MFCS = {}".format(MFCS))
        level_frequent_itemsets = pruneCandidatesUsingMFS(level_frequent_itemsets, MFS)
        print("After Pruning: L{} = {}\n".format(level_k, level_frequent_itemsets))
        candidate_frequent_itemsets = generateCandidateItemsets(level_k, level_frequent_itemsets)
        candidate_frequent_itemsets = pruneCandidatesUsingMFCS(candidate_frequent_itemsets, MFCS)
        level_k += 1
    return MFS



transactions = [
    {'a', 'b', 'd'},
    {'a', 'e'},
    {'a', 'c', 'e'},
    {'a', 'b', 'c'},
    {'b', 'c', 'd', 'e'},
    {'b', 'd', 'e'},
    {'b', 'c', 'e'},
    {'a', 'c', 'd'},
    {'a', 'b', 'd', 'e'},
    {'a', 'b', 'c', 'd', 'e'},
    {'b', 'd'},
    {'c', 'd'},
    {'a', 'b'},
    {'a', 'd'},
    {'d', 'e'}
]

# transactions = [
#     {1, 2, 4},
#     {1, 5},
#     {1, 3, 5},
#     {1, 2, 3},
#     {2, 3, 4, 5},
#     {2, 4, 5},
#     {2, 3, 5},
#     {1, 3, 4},
#     {1, 2, 4, 5},
#     {1, 2, 3, 4, 5},
#     {2, 4},
#     {3, 4},
#     {1, 2},
#     {1, 4},
#     {4, 5}
# ]

min_support_count = 2
MFS = pincerSearch(transactions, min_support_count)
print("MFS = {}".format(MFS))



# transactions = [                        Dataset_Enc = [
#     {'a', 'b', 'd'},                    [1, 1, 0, 1, 0],
#     {'a', 'e'},                         [1, 0, 0, 0, 1],
#     {'a', 'c', 'e'},                    [1, 0, 1, 0, 1],
#     {'a', 'b', 'c'},                    [1, 1, 1, 0, 0],
#     {'b', 'c', 'd', 'e'},               [0, 1, 1, 1, 1],
#     {'b', 'd', 'e'},                    [0, 1, 0, 1, 1],
#     {'b', 'c', 'e'},                    [0, 1, 1, 0, 1],
#     {'a', 'c', 'd'},                    [1, 0, 1, 1, 0],
#     {'a', 'b', 'd', 'e'},               [1, 1, 0, 1, 1],
#     {'a', 'b', 'c', 'd', 'e'},          [1, 1, 1, 1, 1],
#     {'b', 'd'},                         [0, 1, 0, 1, 0],
#     {'c', 'd'},                         [0, 0, 1, 1, 0],
#     {'a', 'b'},                         [1, 1, 0, 0, 0],
#     {'a', 'd'},                         [1, 0, 0, 1, 0],
#     {'d', 'e'}                          [0, 0, 0, 1, 1]
# ]                       
# minSupp = 2

# C1 = a b c d e
# count = 9 9 7 10 8
# S1 = null
# L1 = a b c d e
# MFCS = a b c d e

# C2 = ab ac ad ae bc bd be cd ce de
# count = 5 4 5 4 4 6 5 4 4 5
# S2 = null
# L2 = ab ac ad ae bc bd be cd ce de
# MFCS = a b c d e

# C3 = abc abd abe acd ace ade bcd bce bde cde
# count = 2 3 2 2 2 2 2 3 3 2
# S3 = null
# L3 = abc abd abe acd ace ade bcd bce bde cde
# MFCS = a b c d e

# C4 = abcd abce abde acde bcde
# count = 1 1 2 1 2
# S4 = abcd abce acde
# MFCS = 
# abcd   --   bcde acde abde abce abcd
# abce   --   bcde acde abde abcd [bce ace abe abc]
# acde   --   bcde abde abcd [bce ace abe abc] [cde ade ace acd]

# MFCS = bcde abde abcd [bce ace abe abc] [cde ade ace acd]
# MFI Count = 2 2 1 [3 2 2 2] [2 2 2 2]
# L4 = abde bcde

# C5 = abcde
# count = 1
# MFI = bcde abde bce ace abe abc cde ade acd
# removed subsets
# MFI = bcde abde ace abc acd
# S5 = abcde
# MFCS = same as before abcde is not subset of any
# L5 = null