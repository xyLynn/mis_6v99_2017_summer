# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 02:08:27 2017

@author: Lynn
"""
import requests

#download two files
test_url = 'http://kevincrook.com/utd/market_basket_test.txt'
r = requests.get(test_url)
xf = open("market_basket_test.txt", "wb")
xf.write(r.content)
xf.close()

training_url = 'http://kevincrook.com/utd/market_basket_training.txt'
r = requests.get(training_url)
xf = open("market_basket_training.txt", "wb")
xf.write(r.content)
xf.close()


#import data without Tracking ID in set format
with open('market_basket_test.txt', 'r') as f:
    test = [line.strip().split(',') for line in f]
    
with open('market_basket_training.txt', 'r') as f:
    training = [line.strip().split(',') for line in f]
    
testlist = []
for i in range(len(test)):
    testlist.append(test[i][1:])

traininglist = []
for i in range(len(training)):
    traininglist.append(training[i][1:])
    
tests = [set(c) for c in testlist]
trainings = [set(c) for c in traininglist]


#define a recommended founction
def recommended(l):
    temp = []
    for i in range(len(trainings)):
        if len(l)+1 == len(trainings[i]) and l & trainings[i] == l:
            temp.append(trainings[i])
    
    if len(temp) != 0:
        total = [list(item) for item in temp]
            
        unil = []
        for item in total:
            if item not in unil:
                unil.append(item)   
        
        k = []
        for i in range(len(unil)):
            k.extend([total.count(unil[i])])
        final = unil[k.index(max(k))].copy()
        rec = list(set(final) - l)
        
        return rec
    
    else:
        return ['NA']


#get the recommended list, except those do not a history
recolist = []
for i in range(len(tests)):
    recolist.append(recommended(tests[i]))
    recolist[i].insert(0, str(i+1).zfill(3))


#export the file
with open("market_basket_recommendations.txt", "w") as f:
    for elem in recolist:
        f.write('{},{}\n'.format(*elem))



