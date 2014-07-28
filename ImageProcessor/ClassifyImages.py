"""
Call different machine learning classifiers on data
"""
import cv2
import numpy as np


def calculateAccuracy(testTrueClasses, predictedClasses):
    "Function to calculate the prediction of the classifier"
    correct = np.count_nonzero(testTrueClasses == predictedClasses)
    accuracy = correct * 100.0 / np.size(testTrueClasses)
    return accuracy


def calcSensitivity(testTrueClasses, predictedClasses):
    correct = np.count_nonzero(testTrueClasses == predictedClasses)
    wrong = np.count_nonzero(testTrueClasses != predictedClasses)

    sensitivity = wrong * 100.0 / np.size(testTrueClasses)
    return sensitivity


def naiveBayes(trainingData, trainingClasses, testData, testClasses):
    nbClassifier = cv2.NormalBayesClassifier()
    nbClassifier.train(trainingData, trainingClasses)
    ret, results = nbClassifier.predict(testData)
    return results


def kNN(trainingData, trainingClasses, testData, testClasses):
    kNNClassifier = cv2.KNearest()
    kNNClassifier.train(trainingData, trainingClasses)
    ret, results, neighbours, dist = kNNClassifier.find_nearest(testData, 5)
    return results

def classify_image(image_id):
    dataName = 'dataimageData.npz'

    data = np.load(dataName)
    trainingData = data['train']
    trainingClasses = data['train_labels']
    testData = data['test']
    testClasses = data['test_labels']

    return int(naiveBayes(trainingData, trainingClasses, testData, testClasses)[0][0])