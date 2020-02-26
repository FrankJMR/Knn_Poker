from csv import reader
from csv import writer
from math import sqrt

#data set from kaggle
trainFileName = "poker-hand-training-true.csv"
pokerSet = list()
testPokerSet = list()

#function to load data
"""any empty rows continue the loop,
appends only the rows that 
have data to my list movieSet"""
def loadTrainData(fileName):
    with open(fileName,'r', encoding='utf-8') as file:
        csv_reader = reader(file)
        
        for rows in csv_reader:
            if not rows:
                continue
            pokerSet.append(rows)
       
        return pokerSet
    
def loadTestData(fileName):
    with open(fileName,'r', encoding='utf-8') as file:
        csv_reader = reader(file)
        for rows in csv_reader:
            if not rows:
                continue
            testPokerSet.append(rows)
       
        return testPokerSet
#
"""cleaning for own personal use
Deleting some rows and creating file"""
def dataCleaner(pokerSet):
    for row in range(len(pokerSet)):
        del pokerSet[row][0:2]
        del pokerSet[row][1:3]
        del pokerSet[row][3:12]
    return pokerSet

def fileCreator(pokerSet):
    with open('imdbCleaned.csv', 'w', newline="") as file:
        csv_writer = writer(file)
        for row in range(len(pokerSet)):
            csv_writer.writerow(pokerSet)
            
"""The Euclidean distance
between points in a row"""
def EuclideanDistance(nextRow,currentRow):
    eDistance = 0.0
    for index in range(len(currentRow)-1):
        eDistance +=(currentRow[index]-nextRow[index])**2
    return sqrt(eDistance)

"""----------------------------------------------------------------
getting nearest neighbors
"""
def getNearestNeighbors(train,testRow,kNeighbors):
    neighborDistances = list()
    for row in train:
        distance = EuclideanDistance(testRow,row)
        neighborDistances.append((row,distance))
    neighborDistances.sort(key = lambda tup:tup[1])
    neighbors = list()
    for i in range(kNeighbors):
        neighbors.append(neighborDistances[i][0])
    return neighbors

"""---------------------------------------------------------------
"""
def classify(train,testRow,kNeighbors):
    neighbors = getNearestNeighbors(pokerSet,testRow,kNeighbors)
    print('neighbors for test data ={}'.format(neighbors))
    output = [row[len(testRow)-1] for row in neighbors]
    #print(output)
    prediction = max(set(output),key=output.count)
    #print(prediction)
    return prediction
#calling function to load list
pokerSet = loadTrainData(trainFileName)
testPokerSet = loadTestData(trainFileName)
#python list comprehensions to convert 2d string list to int

pokerSet = ([list(map(int,i)) for i in pokerSet])
testPokerSet =([list(map(int,i)) for i in testPokerSet])

#what type of hand is the thing im trying to predict
row = [4,9,4,7,2,12,1,7,2,6,1]
#print(pokerSet[3],"\n\n")
#print(testPokerSet)
#prediction = classify(pokerSet,for row in testPokerSet,3)
for row in testPokerSet:
    prediction = classify(pokerSet, row, 3)
    #print('Actual: %d, Predicted: %d.' % (row[len(row)-1], prediction))
    print('\033[1m' + 'Actual: %d, Predicted: %d.' % (row[len(row)-1], prediction)









#for neighbor in neighbors:
#    print(neighbor)






















##brief test
#rowZero = pokerSet[0]
#count =0
#for row in pokerSet:
#    count+=1
#    distance = EuclideanDistance(rowZero,row)
#    print('iteration #'.format(count),distance)
#    if count == 15:
#        break
#
#print('Loaded data set {} with {} rows and {} columns'.format(fileName, len(pokerSet), len(pokerSet[0])))
#
#for i in range(len(pokerSet[0])):
#    print(pokerSet[0][i])
    