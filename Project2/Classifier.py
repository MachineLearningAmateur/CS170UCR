import csv
import time
import numpy as np
from typing import List
import matplotlib.pyplot as plt

class Classifier:
    def __init__(self, file):
        self.file = file
        self.features = 0 #len(row) - 1
        self.content = None #will be used to store the list of all rows in the csv file
        self.k = 0 #k = number of rows
        self.counter = 0 #for correct number of objects classified
        self.accuracy = 0 #accuracy = counter/k
        self.defaultRate = None
    

    def train(self): #sets up the data
        #print('train and label the data.')
        #https://docs.python.org/3/library/csv.html
        with open(self.file, 'r') as f:
            self.content = list(csv.reader(f, delimiter=' ', skipinitialspace=True)) #converts the csv object into a list
            self.k = len(self.content) #returns the number of rows or k objects in csv file
            self.features = len(self.content[0]) - 1 #need to offset by 1 because the first column is class label
            # print(self.k)
            # print(self.features)
        default_dict = {}
        for row in self.content:
            if row[0] not in default_dict:
                default_dict[row[0]] = 1
            else:
                default_dict[row[0]] += 1
        self.defaultRate = round(float(max(default_dict.values()))/float(self.k) * 100, 2)

    def reset(self):
        self.counter = 0
        self.accuracy = None

    def test(self, validatedList): #leave one out validation
        #print('predict the class label.')
        #start = time.time()
        for i in range(len(validatedList)): 
        #https://www.thecodingforums.com/threads/convert-scientific-integer-to-normal-integer.336567/ 
            c_label = int(float(self.content[i][0])) #actual label for item in row i #error right here
            # for debugging purposes!
            # print('Loop over i, at the', str(i + 1), 'location') 
            # print('The', str(i + 1), 'th object is in class', str(label))
            
            #initialize both nn_dist and nn_loc to infinity cause we don't know what neighbor is the closest
            #nn_dist is the nearest neighbor distance found so far
            #nn_loc is to store the index of the nearest neighbor found; technically we don't need this variable
            nn_dist = float('inf') 
            nn_loc = float('inf') #variable is useless, was used for debugging
            for j in range(len(validatedList)):
                if (i != j): #don't compare itself
                    dist = self.euclideanDistance(validatedList[i], validatedList[j])
                    if (dist < nn_dist): 
                        nn_dist = dist
                        nn_loc = j
                        nn_label = int(float(self.content[j][0])) #retrieves the label for index/row j
                    #for debugging purposes!
                    #print('Ask if', str(i), 'is nearest neighbor with', str(j))
            #works!
            # print('Object ', str(i), 'is class', str(cLabel))
            # print('Its nearest neighbor is', str(nn_loc), 'which is in class', str(nn_label))
            if (c_label == nn_label):
                self.counter += 1
        self.accuracy = float(self.counter)/float(self.k)
        #end = time.time()
        #print(end-start)
    
    def euclideanDistance(self, testRow, compareRow):
        #https://www.geeksforgeeks.org/calculate-the-euclidean-distance-using-numpy/ 
        #for n dimensional euclidean distance
        #https://stackoverflow.com/questions/3877209/how-to-convert-an-array-of-strings-to-an-array-of-floats-in-numpy
        #for converting array of str to float
        sum_sq = np.sum(np.square(np.array(testRow, dtype=float) - np.array(compareRow, dtype=float)))
        return np.sqrt(sum_sq)
    
    #to be worked on
    def plotFeatures(self, feature1 : int, feature2 : int):
        #print(features)
        print('Plotting graph.')
        Class1feature1Lst = []
        Class1feature2Lst = []
        Class2feature1Lst = []
        Class2feature2Lst = []
        for row in range(len(self.content)):
            currRow = self.content[row]
            if round(float(currRow[0]), 0) == 1:
                Class1feature1Lst.append(round(float(currRow[feature1]), 2))
                Class1feature2Lst.append(round(float(currRow[feature2]), 2))
            else:
                Class2feature1Lst.append(round(float(currRow[feature1]), 2))
                Class2feature2Lst.append(round(float(currRow[feature2]), 2))
                # if col == feature1:
                #     feature1Lst.append(round(float(self.content[row][col]), 2))
                # elif col == feature2:
                #     feature2Lst.append(round(float(self.content[row][col]), 2))
        fig, ax = plt.subplots()
        fig.tight_layout()
        ax.set_ylabel('Feature ' + str(feature2))
        ax.set_xlabel('Feature ' + str(feature1))
        ax.set_title(self.file.replace('.txt',''))

        good1 = []
        good2 = []
        plt.plot(Class1feature1Lst, Class1feature2Lst, 'o', color='red', markerfacecolor='none', label='Class 1')
        plt.plot(Class2feature1Lst, Class2feature2Lst, 'o', markerfacecolor='none', label='Class 2')
        leg = ax.legend()
        plt.show()

