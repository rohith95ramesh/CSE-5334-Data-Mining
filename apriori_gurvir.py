# Reference: https://github.com/asaini/Apriori
import sys
import operator
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

def runApriori(inputData, minSupport, minConfidence):
    itemSet, transactionList = getItemSetTransactionList(inputData)
    freqSet = defaultdict(int) # dict subclass that calls a factory function to supply missing values
    givenSet = dict()
    rulesGenerated = dict()
    onSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet) #Calls another function to check if the minimum supp criteria is satsified
    currentLSet = onSet
    k = 2
    while(currentLSet != set([])):
        givenSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,transactionList,minSupport,freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
            supp = float(freqSet[item])/len(transactionList)
            return supp

    toRetItems = []
    for key, value in givenSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []
    for key, value in list(givenSet.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules
# Get items from dataset.csv
def dataFromFile(fname):
        file_iter = open(fname, 'r')
        for line in file_iter:
                line = line.strip().rstrip(',') 
                record = frozenset(line.split(','))
                yield record

# Create a transaction list to iterate over
def getItemSetTransactionList(iterateData):
    transactionList = list()
    itemSet = set()
    for record in iterateData:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))
    return itemSet, transactionList

def joinSet(itemSet, length):
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

# This function calculates the minimum support and returns the items that satify the minimum support value
def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
        _products = set()
        givenSet = defaultdict(int)

        # Incrementing the given data set
        for i in itemSet:
                for transaction in transactionList:
                        if i.issubset(transaction):
                                freqSet[i] += 1
                                givenSet[i] += 1

        for i, count in givenSet.items():
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _products.add(i)

        return _products
# This function is called to print the results of runApriori function
def printResults(items, rules):
    print("\n------------ITEMS-----------------")
    for item, support in sorted(items, key=operator.itemgetter(1)):
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------RULES-----------------")
    for rule, confidence in sorted(rules, key=operator.itemgetter(1)):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))
    print("\n")