'''
Apriori Python Implementation
'''

# Imports
import sys
import csv
import collections

# Functions
def generate_rules(overall_dict, csvfile):
    rules_dict = {}
    rules_array = []
    count = 0
    # combine two dictionaries
    # overall_dict = {**overall_dict, **vfi_dict}
    #
    #
    # for vfi1 in overall_dict.keys():
    #     for vfi2 in overall_dict.keys():
    #         if len(vfi1) + len(vfi2) == len(list(vfi_dict.keys())[0]):
    #             if not vfi1 == vfi2:
    #
    #                 combine = vfi1 + vfi2
    #                 # print(overall_dict)
    #                 if combine in overall_dict.keys():
    #                     # compute support percentage
    #                     support_percentage = overall_dict[combine][0]
    #                     # compute confidence
    #                     conf = overall_dict[combine][1] / overall_dict[vfi1][1]
    # overall_dict = collections.OrderedDict(sorted(overall_dict.items()))
    for index1, item1 in enumerate(overall_dict.keys()):
        for index2, item2 in enumerate(overall_dict.keys()):
            # print(item1, item2)
            contain = False
            for i in item1:
                # print(i)
                if i in item2:
                    contain = True
                    break
            if contain: # at least one char in item1 is in item2
                continue
            else:
                # rules_array[count].append(item1)
                # rules_array[count].append(item2)
                test = set()
                for c in item1:
                    test.add(c)
                for c in item2:
                    test.add(c)
                # print('test', test)
                test = sorted(test)
                phrase = ()
                for t in test:
                    phrase += (t,)
                # print(phrase)
                if phrase in overall_dict.keys():
                    # supp same with that of phrase
                    support_percentage = overall_dict[phrase][0]
                    # conf = sup(phrase) / sup(first one)
                    conf = overall_dict[phrase][1] / overall_dict[item1][1]
                    # print('phrase',phrase)
                    if support_percentage >= min_support_percentage and conf >= min_confidence:
                        rules_array.append([])
                        rules_array[count].append(support_percentage)
                        rules_array[count].append(conf)
                        rules_array[count].append(item1)
                        rules_array[count].append(item2)
                        count += 1
                        csvfile.write('rule,')
                        csvfile.write(str("%0.6f" % support_percentage))
                        csvfile.write(',')
                        csvfile.write(str("%0.6f" % conf))
                        csvfile.write(',')
                        for i in item1:
                            csvfile.write(str(i))
                            csvfile.write(',')
                        csvfile.write('\'=>\'')
                        csvfile.write(',')
                        for index, i in enumerate(item2):
                            csvfile.write(i)
                            if not index == len(item2)-1:
                                csvfile.write(',')
                        csvfile.write('\n')

    return rules_dict

def generate_cfi_vfi(cfi_dict, vfi_dict, overall_dict):
    vfi_dict = collections.OrderedDict(sorted(vfi_dict.items()))
    cfi_dict = collections.OrderedDict(sorted(cfi_dict.items()))
    vfi_dict = {}
    rules_dict = {}
    if cfi_dict == {}:
        with open(input_filename) as csvfile:
            reader = csv.reader(csvfile)
            for itemset in reader:
                # print(itemset)
                # itemset = itemset.strip()
                for index,i in enumerate(itemset):
                    itemset[index] = i.strip()
                content.append(itemset[1:len(itemset)])
                # print(content)
                for key, item in enumerate(itemset):
                    if key > 0: #support count
                        # print(type(item))
                        item = (item.strip(),)
                        print(item)
                        if not item in cfi_dict:
                            cfi_dict[item] = []
                            cfi_dict[item].append(0)
                            cfi_dict[item].append(1)
                            # print(cfi_dict)
                        else:
                            cfi_dict[item][1] += 1
            # print(len(content))
            for key in cfi_dict.keys():
                print(key)
                support_percentage = cfi_dict[key][1] /  len(content)
                cfi_dict[key][0] = support_percentage
                if support_percentage >= min_support_percentage:
                    # if key == ('a134',):
                    #     print('here', key)
                    vfi_dict[key] = [support_percentage, cfi_dict[key][1]] # support percentage and support count

    else:
        support_count = 0
        for key in cfi_dict.keys():
            print(type(key))
            print(key, cfi_dict[key][0])
            if cfi_dict[key][0] >= min_support_percentage:
                vfi_dict[key] = [cfi_dict[key][0], cfi_dict[key][1]]
        # for every vfi_dict of key with length n (A,B,C), do the rule with overall length n (A->B)
        # rules_dict = generate_rules(vfi_dict, overall_dict)
    # print(vfi_dict)
    return [cfi_dict, vfi_dict, rules_dict]

def generate_largercfi(vfi_dict, cfi_dict):
    vfi_dict = collections.OrderedDict(sorted(vfi_dict.items()))
    cfi_dict = collections.OrderedDict(sorted(cfi_dict.items()))
    keys = list(vfi_dict.keys())
    # print('len(keys)',len(keys))
    print(keys)
    # print(len(keys))
    if len(keys) < 2:
        return {}
    for i in range(len(keys)):
        for j in range(len(keys)):
            key1 = keys[i]
            key2 = keys[j]
            test = set()
            for item1 in key1:
                test.add(item1)
            for item2 in key2:
                test.add(item2)

            test = sorted(test)
            # print(test)
            # prin
            # print(len(keys[0]))
            # print(test)
            # print(test)
            # print(test)
            # print('test[0]',test[0])
            # print(len(test))
            # print(len(test))
            # print(len(keys[0]))
            key = (keys[0],)
            # print(len(key))
            if len(test) == len(keys[0])+1:
                # print('here')
                new_key = ()    # tuple
                support_count = 0
                for item in test:
                    new_key += (item,)
                # print('new_key', new_key)

                cfi_dict[new_key] = []

                for trans in content:
                    # print('trans',trans)
                    flag = True
                    for index, k in enumerate(new_key):
                        if not k in trans:
                            flag = False
                        if index == len(new_key)-1:
                            if flag:
                                support_count += 1

                cfi_dict[new_key].append(support_count / len(content))
                cfi_dict[new_key].append(support_count)
                # print(new_key)
            # new_key = keys[i] + keys[j]
            # cfi_dict[new_key] = min(vfi_dict[keys[i]], vfi_dict[keys[j]])
            # print(cfi_dict)
    return cfi_dict

def outputSetToFile(mydict, csvfile):
    orderedDict = collections.OrderedDict(sorted(mydict.items()))
    for key, value in orderedDict.items():
        csvfile.write('set,')
        csvfile.write(str( "%0.6f" % value[0]))
        csvfile.write(',')
        for idx in range(len(key)):
            csvfile.write(key[idx])
            # print('112312312312312312312',key[idx])
            if idx == len(key)-1:
                csvfile.write('\n')
            else:
                csvfile.write(',')
                
# Driver Code
input_filename = sys.argv[1]
output_filename = sys.argv[2]
min_support_percentage = float(sys.argv[3])
min_confidence = float(sys.argv[4])
total_num_trans = 0
content = []

index = 1
cfi_dict = {}
vfi_dict = {}
overall_dict = {}
with open(output_filename, 'w') as csvfile:
    while True:
        # print(index)
        [cfi_dict, vfi_dict, rules_dict] = generate_cfi_vfi(cfi_dict, vfi_dict, overall_dict)
        # print(content)
        outputSetToFile(vfi_dict, csvfile)
        overall_dict = {**overall_dict, **vfi_dict}
        # if index < 9:
        # print(vfi_dict)

        cfi_dict = {}
        # print(vfi_dict)
        cfi_dict = generate_largercfi(vfi_dict, cfi_dict)

        # if index == 3:
        if cfi_dict == {}:
            # print(vfi_dict)
            break
        index += 1

        # print(overall_dict)
    # print(overall_dict)
    generate_rules(overall_dict, csvfile)