# -*- coding: utf-8 -*-
"""
Date: Created on 2017-10-14  09:44am  星期四  

Author: zgj

Description:
    Python implementation of the Apriori algorithm
    
Usage:
    
"""

from collections import defaultdict
from optparse import OptionParser    # parse command-line parameters
import csv

class Apriori(object):
    def __init__(self, minSupp, minConf):
        self.minSupp = minSupp
        self.minConf = minConf

    def fit(self, dirInput):
        """ Run the apriori algorithm, return the frequent *-terms. 
        """
        # Initialize some variables to hold the tmp result
        transListSet  = self.getTransListSet(dirInput)   # list of the all transactions
        itemSet       = self.getItemSet(transListSet) # hold all unique 1-items
        itemCountDict = defaultdict(int)         # key=candiate k-item(k=1/2/...), value=count
        freqSet       = dict()                   # hold all frequent *-items
        
        self.transLength = len(transListSet)     # number of transactions
        self.itemSet     = itemSet
        
        # Get the frequent 1-term set
        freqOneTermSet = self.getItemsWithMinSupp(transListSet, itemSet, 
                                             itemCountDict, self.minSupp)
        freqSet[1] = freqOneTermSet
        
        # Main loop
        k = 2
        currFreqTermSet = freqOneTermSet
        while currFreqTermSet != defaultdict(int):
            currCandiItemSet = self.getJoinedItemSet(currFreqTermSet) # get new candiate k-terms set
            currFreqTermSet  = self.getItemsWithMinSupp(transListSet, currCandiItemSet, 
                                                   itemCountDict, self.minSupp) # frequent k-terms set
            freqOneTermSet[k] = currFreqTermSet  # save the result
            k += 1
            
        #
        self.itemCountDict = itemCountDict
        self.freqSet       = freqSet
            
            
    def getSpecRules(self, rhs):
        if rhs not in self.itemSet:
            print('Please input a term contain in the term-set !')
            return None
        
        rules = dict()
        for item in self.itemCountDict:
            if rhs in item and len(item) > 1:
                item_supp = self.getSupport(item)
                item.remove(rhs)
                conf = item_supp / self.getSupport(item)
                rules[item] = conf
        return rules        
        
    
    def getSupport(self, item):
        """ Get the support of item """
        return self.itemCountDict[item] / self.transLength
        
        
    def getJoinedItemSet(self, termSet, k):
        """ Generate new k-terms candiate itemset"""
        return set([term1.union(term2) for term1 in termSet for term2 in termSet 
                    if len(term1.union(term2))==k])
    
        
    def getItemSet(self, data):
        """ Get all unique 1-item(s) (saved in the `set` datatype) """
        return set([item for line in data for item in line])
        
    
    def getTransListSet(self, filepath):
        """ Get the transaction list """
        transListSet = []    # a list contains sets
        with open(filepath, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            for line in reader:
                transListSet.append(set(line))                
        return transListSet
                
    
    def getItemsWithMinSupp(self, transListSet, itemSet, freqSet, minSupp):
        """ Get
        """
        itemSet_  = set()
        localSet_ = defaultdict(int)
        for item in itemSet:
            freqSet[item]   += sum([1 for trans in transListSet if item.issubset(trans)])
            localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])
        
        # Only conserve frequent item-set 
        n = len(transListSet)
        for item, cnt in localSet_.items():
            itemSet_.add(item) if float(cnt)/n >= minSupp else None
        
        return itemSet_


if __name__ == '__main__':
    
    # Parse command-line parameters
    optParser = OptionParser()
    optParser.add_option('-f', '--file', dest='dirInput',
                         help='input .csv file',
                         default=None)  # input a csv file
                         
    optParser.add_option('-s', '--minSupp', dest='minSupp',
                         help='mininum support',
                         default=0.10)  # mininum support value
                         
    optParser.add_option('-c', '--minConf', dest='minConf',
                         help='mininum confidence',
                         default=0.40)  # mininum confidence value                     

    (options, args) = optParser.parse_args()       
        
    # Get two important parameters
    dirInput = options.dirInput
    minSupp  = options.minSupport
    minConf  = options.minConfidence
    print('Parameters: \n  minSupport: ', minSupp, '\n  minConfidence: ', minConf)

    # Run
    objApriori = Apriori(minSupp, minConf)
    objApriori.fit(dirInput)
    objApriori.transform(dirInput)

    # Return rules with regard of `rhs`
    rhs   = 'banana'
    rules = objApriori.getSpecRules(rhs)





