
''' This file holds the functionality for image filtering and pre-processing '''

import cv2
from skimage import data, filter
import numpy as np
import os
import re

def skimage_filter_technique(image_path):
    img2 = data.imread(image_path, True)
    tv_filter = filter.denoise_tv_chambolle(img2, weight=0.1)
    return tv_filter


def getJpgImages(imgPath):
    images = next(os.walk(imgPath))[2]
    imgs = [os.path.join(imgPath, image) for image in images if re.search(r'\S+.jpg', image)]
    return imgs


def calculateHistograms(images, bins):
    numOfImages = len(images)
    imageData = np.zeros((numOfImages, bins))
    for imageIndex in range(numOfImages):
        img = cv2.imread(images[imageIndex])
        img2 = skimage_filter_technique(images[imageIndex])
        hist = cv2.calcHist([img], [0], None, [bins], [0, 256])
        imageData[imageIndex, :] = hist.transpose()
    return imageData


def get_histograms(disease_train_path, healthy_train_path, disease_test_path):    
    bins = 50 # length of data vector
    trainingDiseasedImages = getJpgImages(disease_train_path)
    trainingHealthyImages = getJpgImages(healthy_train_path)
    testDiseasedImages = getJpgImages(disease_test_path)

    trainingDiseasedData = calculateHistograms(trainingDiseasedImages, bins).astype(np.float32)
    trainingHealthyData = calculateHistograms(trainingHealthyImages, bins).astype(np.float32)
    testDiseasedData = calculateHistograms(testDiseasedImages, bins).astype(np.float32)

    return {"trainingDiseasedData": trainingDiseasedData, "trainingHealthyData": trainingHealthyData, "testDiseasedData": testDiseasedData}


def define_data_classes(trainingDiseasedData, trainingHealthyData, testDiseasedData):
    #Healthy - class 0, Diseased - class - 1
    trainingDiseasedClasses = np.ones((len(trainingDiseasedData), 1)).astype(np.float32)
    trainingHealthyClasses = np.zeros((len(trainingHealthyData), 1)).astype(np.float32)
    testDiseasedClasses = np.ones((len(testDiseasedData), 1)).astype(np.float32)

    return {"trainingDiseasedClasses": trainingDiseasedClasses,  "trainingHealthyClasses":trainingHealthyClasses, "testDiseasedClasses":testDiseasedClasses}


def concatenate_data(trainingHealthyData, trainingHealthyClasses, trainingDiseasedData, trainingDiseasedClasses, testDiseasedData, testDiseasedClasses):
    trainingData = np.vstack((trainingHealthyData, trainingDiseasedData))
    trainingClasses = np.vstack((trainingHealthyClasses, trainingDiseasedClasses))

    testData = np.vstack(testDiseasedData)
    testClasses = np.vstack(testDiseasedClasses)

    return {"trainingData":trainingData, "trainingClasses":trainingClasses, "testData":testData, "testClasses":testClasses}

def save_data_to_folder(dataFolderPath, dataClasses):
    dataName = dataFolderPath + 'imageData.npz'
    
    np.savez(dataName, 
        train=dataClasses['trainingData'],  train_labels=dataClasses['trainingClasses'], 
        test=dataClasses['testData'],  test_labels=dataClasses['testClasses'])

    return True