import os
import numpy as np
from PIL import Image


# Takes an image in array form as input and creates a barcode
def barcode_generator(arr):
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []

    # Gets 0 and 90 degree projections
    for i in range(28):
        sumOfHorizontal = 0
        sumOfVertical = 0
        for j in range(28):
            sumOfHorizontal += arr[i][j]
            sumOfVertical += arr[j][i]
        p1.append(sumOfHorizontal)
        p3.append(sumOfVertical)

    # Gets 45 and 135 degree projections
    for i in range(-14, 14):
        d1 = np.diagonal(arr, i, 0, 1)
        d2 = np.diagonal(np.fliplr(arr), i, 0, 1)
        p2.append(sum(d1))
        p4.append(sum(d2))

    # Calculate threshold values
    th_p1 = sum(p1) / len(p1)
    th_p2 = sum(p2) / len(p2)
    th_p3 = sum(p3) / len(p3)
    th_p4 = sum(p4) / len(p4)

    # If the cell value is less than or equal to the threshold value assign 0, otherwise assign 1
    for i in range(28):
        if p1[i] <= th_p1:
            c1.append(0)
        else:
            c1.append(1)

        if p2[i] <= th_p2:
            c2.append(0)
        else:
            c2.append(1)

        if p3[i] <= th_p3:
            c3.append(0)
        else:
            c3.append(1)

        if p4[i] <= th_p4:
            c4.append(0)
        else:
            c4.append(1)

    # Compile all projection into one barcode
    barcode = c1 + c2 + c3 + c4
    return barcode


# The Hamming distance between two equal-length strings of symbols is the number of positions at
# which the corresponding symbols are different.
def hamming_distance(str1, str2):
    d = 0
    for c1, c2 in zip(str1, str2):  # zip() Iterate over several iterables in parallel
        if c1 != c2:
            d = d + 1
    return d


# Searches for the most similar image in the dataset given a query image and returns the path to the result
def search_algorithm(query_image_path):
    # Convert the query image path to its array form
    query_image = Image.open(query_image_path)
    query_arr = np.asarray(query_image)
    query_barcode = barcode_generator(query_arr)

    minHammingDistance = 112
    closestImagePath = ""

    cwd = os.getcwd()
    MNIST_path = os.path.join(cwd, 'MNIST_DS')
    classes = os.listdir(MNIST_path)
    for c in classes:  # Iterates through the image folders 0-9
        folder_path = os.path.join(MNIST_path, c)
        image_files = os.listdir(folder_path)
        for img in image_files:  # Iterates though the image file names contained in each folder
            image_path_complete = folder_path + "\\" + img

            # Do not include query image in search results
            if image_path_complete != query_image_path:
                image = Image.open(image_path_complete)
                arr = np.asarray(image)
                barcode = barcode_generator(arr)

                d = hamming_distance(barcode, query_barcode)

                if d < minHammingDistance:
                    minHammingDistance = d
                    closestImagePath = image_path_complete

    return closestImagePath


c = '0'
image_name = 'img_10007.jpg'
image_path = os.path.join(os.getcwd(), 'MNIST_DS\\' + c, image_name)
image = Image.open(image_path)
arr = np.asarray(image)

"""
print("Barcode of first image: ", barcode_generator(arr))
print("Search result of first image:", search_algorithm(image_path))
"""

cwd = os.getcwd()
MNIST_path = os.path.join(cwd, 'MNIST_DS')
classes = os.listdir(MNIST_path)
for c in classes:
    folder_path = os.path.join(MNIST_path, c)
    image_files = os.listdir(folder_path)
    for img in image_files:
        image_path_complete = folder_path + "\\" + img
        print("Query Image: " + image_path_complete)
        print("Search result: " + search_algorithm(image_path_complete) + "\n")
