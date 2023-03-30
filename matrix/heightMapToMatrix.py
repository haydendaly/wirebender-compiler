import matplotlib.pyplot as plt
import numpy as np


def imgToPrunedMatrix(pixelSkipStep, maxHeight, image):
    #maxHeight in mm

    # Read the image file
    img = plt.imread(image)

    #get height, width, and skipped versions
    height, width = img.shape[0], img.shape[1]
    heightSkipped = int(np.floor(height / pixelSkipStep))
    widthSkipped = int(np.floor(width / pixelSkipStep))

    #init matOut
    matOut = np.zeros((heightSkipped, widthSkipped))

    #reverse loop skipping pixels, build matOut
    for x in range(widthSkipped - 1, -1, -1):
        for y in range(heightSkipped - 1, -1, -1):
            matOut[y,x] = img[y * pixelSkipStep,x * pixelSkipStep,0]

    #convert 0->1 to 0->max height
    matOut *= maxHeight

    return matOut

# prunedMatrix = imgToPrunedMatrix(3, 100, 'denaliHeightMap.png')

# plt.imshow(prunedMatrix, cmap='gray')
# plt.show()
# print(prunedMatrix)
# print(prunedMatrix.shape)