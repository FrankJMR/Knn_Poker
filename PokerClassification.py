#Frank J Martinez
from csv import reader
from csv import writer
from math import sqrt

#not used
import numpy as np

#data set from kaggle
trainFileName= "poker-hand-training-true.csv"
testFileName = "poker-hand-testing.csv"
pokerSet = list()
testPokerSet = list()

"""function to load test and train data
any empty rows continue the loop,
appends only the rows that 
have data to my list movieSet"""
def loadTrainData(fileName):
    with open(fileName,'r', encoding='utf-8') as file:
        csv_reader = reader(file)
        
        for rows in csv_reader:
            if not rows:
                continue
            pokerSet.append(rows)
            
        return ([list(map(int,i)) for i in pokerSet])
        
    
def loadTestData(testFileName):
    with open(testFileName,'r', encoding='utf-8') as file:
        csv_reader = reader(file)
        for rows in csv_reader:
            if not rows:
                continue
            testPokerSet.append(rows)
            
        return ([list(map(int,i)) for i in testPokerSet])

def dataCleaner(dataSet):
    #getting the labels, the last col
    return [row[10] for row in dataSet]

def fileCreator(pokerSet): 
    with open('imdbCleaned.csv', 'w', newline="") as file:
        csv_writer = writer(file)
        for row in range(len(pokerSet)):
            csv_writer.writerow(pokerSet)
            
"""The Euclidean distance
between two vectors"""
def EuclideanDistance(nextRow,currentRow):
    eDistance = 0.0
    for index in range(len(currentRow)-1):
        #Distance between two vectors
        eDistance +=(currentRow[index]-nextRow[index])**2
    return sqrt(eDistance)

#cosine similarity, just experimenting with num py. no place in the code
def cosineSimilarity(nextRow, currentRow):
    dot = np.dot(nextRow,currentRow)
    norma = np.linalg.norm(nextRow)
    normb = np.linalg.norm(currentRow)
    cos = dot / (norma * normb)
    return cos


#function to sort all distances and get nearest neighbor
def getNearestNeighbors(train,testRow,kNeighbors):
    neighborDistances = list()
    for currentRow in train:
        distance = EuclideanDistance(testRow,currentRow)
        
        neighborDistances.append((currentRow,distance))
    #fast way to sort a tuple that contains distances and the corresponding vector, tup[1] is the index of the distance 
    neighborDistances.sort(key = lambda tup:tup[1])
    
    neighbors = list()
    
    #since the tuples are sorted we can retrieve the
    #nearest neighbors off the top of the list because it is the closest.
    for i in range(kNeighbors):
        neighbors.append(neighborDistances[i][0])
    
    return neighbors


#a function to get most common labels 
def classify(train,testRow,kNeighbors):
    #retrieving ALL neighbors
    neighbors = getNearestNeighbors(pokerSet,testRow,kNeighbors)
    
    #A list of the TOP labels among my nearest neighbors
    myTopNeighbors = [row[len(testRow)-1] for row in neighbors]
    print(myTopNeighbors)
    
    #Voting for the most COMMON among the TOP labels
    prediction = max(set(myTopNeighbors),key=myTopNeighbors.count)
    
    return prediction

#calling function to load list
pokerSet = loadTrainData(trainFileName)
testPokerSet = loadTestData(testFileName)

#demonstration purposes, selecting x amount of Rows for testing
test = testPokerSet[:70]
correct = 0

#iterating over spliced test list
for row in test:
    
    prediction =classify(pokerSet, row,5)
    print('Actual: %d, Predicted: %d.' % (row[len(row)-1], prediction))
    
    #prediction label is last index of row
    if row[len(row)-1] == prediction:
        correct+=1

print("Accuracy: {}%".format(correct/len(test)*100))
