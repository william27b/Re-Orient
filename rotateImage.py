import math
import numpy as np
from PIL import Image
import os

# def getPixelDepth(x, y):
#     return 0

# def getHypoteneuse(x, y):
#     return math.sqrt(x**2 + y**2)

# def getNewPosition(x, y, xRotation):
#     depth = getPixelDepth(x, y)

#     distance = getHypoteneuse(x, depth)
#     currentRotation = math.atan(depth / x)

#     # for now, y rotation does not exist

#     x_prime = distance * math.cos(currentRotation + xRotation)

#     return (x_prime, y)

def getNewXMappings(xMap, depthMap, xRotation):
    distanceMap = np.sqrt(np.add(np.square(xMap), np.square(depthMap)))
    rotationMap = np.arctan(np.divide(depthMap, xMap))
    rotationMap += xRotation

    newXMappings = distanceMap * np.cos(rotationMap)
    return newXMappings

def getNewYMappings(yMap, depthMap, yRotation):
    distanceMap = np.sqrt(np.square(yMap) + np.square(depthMap))
    rotationMap = np.arctan(np.divide(depthMap, yMap))
    rotationMap += yRotation

    newYMappings = distanceMap * np.cos(rotationMap)
    return newYMappings

def rotateImage(imgPath, depthPath, xRotation, yRotation, depthScalar, save_path='rotated.jpg'):
    # load image
    image = Image.open(imgPath)
    image = np.array(image)

    n, m, _ = image.shape

    # load depth map
    depthImage = Image.open(depthPath)
    # convert to int64 to prevent overflow errors
    depthMap = np.asarray(depthImage, np.int32)*depthScalar

    # calculate the x pixel translations
    xMap = np.asarray([np.arange(1, m+1) for _ in range(n)], np.int32)
    newXMappings = np.rint(getNewXMappings(xMap, depthMap, math.radians(xRotation))).astype(int)

    # normalize the x translations
    xMap -= np.min(xMap)
    newXMappings -= np.min(newXMappings)

    # calculate the y pixel translations
    yMap = np.asarray([[i]*m for i in range(1, n+1)], np.int32)
    newYMappings = np.rint(getNewYMappings(yMap, depthMap, math.radians(yRotation))).astype(int)

    # normalize the y translations
    newYMappings -= np.min(newYMappings)

    # create blank canvas
    finalImage = np.array([[[0, 0, 0, float('inf')] for _ in range(np.max(newXMappings)+1)] for _ in range(np.max(newYMappings)+1)])

    # place pixels based on pixel translations
    for y in range(n):
        for x in range(m):
            # compare depths, pixels with the lowest? depth show up on top
            if depthMap[y][x] < finalImage[newYMappings[y][x]][newXMappings[y][x]][3]:
                finalImage[newYMappings[y][x]][newXMappings[y][x]] = np.append(image[y][x], depthMap[y][x])

    # remove the depth info from the image
    finalImage = finalImage[:,:,:3]

    # save as unsigned int 8 bits
    finalImage = np.asarray(finalImage, np.uint8)

    # show output image
    finalImagePIL = Image.fromarray(finalImage, 'RGB')
    finalImagePIL.save(save_path)
    finalImagePIL.show()

if __name__ == "__main__":
    print("""
positive x-rotation is moves the camera to the left,
negative moves the camera to the right, 
0 does not move the camera left or right
    """)

    xRotation = float(input('x rotation (degrees): '))

    print("""
positive y-rotation is moves the camera up,
negative moves the camera down, 
0 does not move the camera up or down
    """)

    if abs(xRotation) >= 90:
        raise ValueError('rotation values must be between -90 and 90 degrees')

    yRotation = float(input('y rotation (degrees): '))

    print("""
since the depth is an arbitrary unit,
it can be scaled up or down to greaten or lessen
the difference between closer or further objects
when rotating the camera
    """)

    if abs(yRotation) >= 90:
        raise ValueError('rotation values must be between -90 and 90 degrees')

    depthScalar = float(input('depth scalar (default 1): '))

    image_path = input('path to load image: ')

    if not os.path.exists(image_path):
        raise ValueError('path does not exist')
    
    depth_map_path = input('path to load depth map: ')

    if not os.path.exists(depth_map_path):
        raise ValueError('path does not exist')
    
    rotated_image_path = input('path to save rotated image: ')

    rotateImage(image_path, depth_map_path, xRotation, yRotation, depthScalar, rotated_image_path)