from itertools import chain, combinations

class Apriori(object):
    def __init__(self, transactionList, minSupport, minConfidence):
        super(Apriori, self).__init__()
        self.transactionList = transactionList
        self.minSupport = minSupport
        self.minConfidence = minConfidence

        self.frequentItemSets = dict()
        self.rules = []

    def run(self):
        itemSet = self.itemSetFromTransactionList()
        self.getFrequentItemSets(itemSet, 1)
        self.getRules()
        self.printResult()

    def printResult(self):
        print "Transactions:"
        for transaction in self.transactionList:
            print list(transaction)

        print("\nFrequent itemsets (minimum support:%.1f%%):" % (self.minSupport * 100))
        for itemSet, support in sorted(self.frequentItemSets.items(), key=lambda (item, support): support):
            print("%s Support: %.1f%%" % (str(list(itemSet)), support * 100))

        print("\nRules (minimum confidence:%.1f%%):" % (self.minConfidence * 100))
        for pre, post, confidence in sorted(self.rules, key=lambda (pre, post, confidence): confidence):
            print("%s -> %s Confidence: %.1f%%" % (str(list(pre)), str(list(post)), confidence * 100))

    def itemSetFromTransactionList(self):
        itemSet = set()
        for transaction in self.transactionList:
            for item in transaction:
                itemSet.add(frozenset([item]))
        return itemSet

    def getFrequentItemSets(self, itemSet, length):
        localSet = dict()
        currentItemSet = set()

        for item in itemSet:
            localSet[item] = 0
            for transaction in self.transactionList:
                if item.issubset(transaction):
                    localSet[item] += 1

        for item, count in localSet.items():
            support = float(count) / len(self.transactionList)
            if support >= self.minSupport:
                self.frequentItemSets[item] = support
                currentItemSet.add(item)

        length += 1
        nextItemSet = self.joinSet(currentItemSet, length)

        if len(nextItemSet) > 0:
            self.getFrequentItemSets(nextItemSet, length)

    def joinSet(self, itemSet, length):
        return set(i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length)

    def getRules(self):
        largeItemSets = []
        for itemSet in self.frequentItemSets.keys():
            if len(itemSet) >= 2:
                largeItemSets.append(itemSet)
        for itemSet in largeItemSets:
            subItemSet = map(frozenset, self.subsets(itemSet))
            for subset in subItemSet:
                remain = itemSet.difference(subset)
                confidence = self.frequentItemSets[itemSet] / self.frequentItemSets[subset]
                if confidence >= self.minConfidence:
                    self.rules.append((subset, remain, confidence))

    def subsets(self, itemSet):
        return chain.from_iterable(combinations(itemSet, n) for n in range(1, len(itemSet)))

def transactionsFromFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    transactionList = []
    for line in lines:
        items = line.split(", ")
        transactionList.append(frozenset(items))
    return transactionList

def main():
    while 1:
        filename = raw_input("Input file name:")
        minSupport = input("Input minimum support:")
        minConfidence = input("Input minimun confidence:")

        transactionList = transactionsFromFile(filename)

        apriori = Apriori(transactionList, minSupport, minConfidence)
        apriori.run()
        _continue = raw_input("Continue? (Input 1 to Continue or other to Stop):")
        if _continue != "1":
            break
    pass

if __name__ == '__main__':
    main()

