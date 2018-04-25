from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
from timeit import default_timer as timer
from scipy import misc
from PIL import Image
import numpy as np
import random
import glob
import math
import cv2 
import os

import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

'''
Decorator to allow other functions to be exectue after one another
'''
def run_after(f_after):
    def wrapper(f):
        def wrapped(*args, **kwargs):
            ret = f(*args, **kwargs)
            f_after()
            return ret
        return wrapped
    return wrapper

overallTimeElapsed = 0

'''
cleaner:
  - Cleans output directory by removing .DS_Store file and last frame.
'''
def cleaner():
    if(os.path.isfile('./clean/.DS_Store')):
        os.remove('./clean/.DS_Store')
    image_list = []
    for filename in glob.glob('./clean/*.jpg'):
        image_list.append(filename)
    image_list.sort()
    le = image_list[-1]
    os.remove('%s' %le)
    print('Clean up completed ✓')

'''
framer:
  - Reads a video using OpenCC
  - Sets image capture to 24 frames per second
	- Reads & Outputs the images into the given path
  - calls cleaner function after function is finished
'''
@run_after(cleaner)
def framer():
    pathIn = './video.mp4'
    pathOut = './clean/'
    if not os.path.exists('./clean'):
      os.makedirs('./clean')
    count = 1
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
    success = True
    while success:
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*45))  
      success,image = vidcap.read()
      print ('Frame ', count, ' Processed.')
      cv2.imwrite( pathOut + "%07d_clean_image.jpg" % count, image)  
      count += 1

'''
isPerfSquare:
    -   Take in a 3D array
    -   Compares the length of the rows vs columns
    -   returns a boolean 
'''                       
def isPerfSquare(arr):
    row = len(arr) #rows
    col = len(arr[0]) #columns
    # print("Number of rows: ", row,'\n')
    # print("Number of columns: ", col,'\n')
    rxc = row - col
    if(rxc != 0):
        return(False)
    return (True)

'''
makePerfSquare : 
    -   Takes in a 3D array
    -   will make the array a perfect square by taking 
        either the row or column and making that the length
        of both sides. 
    -   return a new perfect square array. Padded with zeros to make 
        the perfect square matric possible
'''
def makePerfSquare(arr):
    row = len(arr) #rows
    col = len(arr[0]) #columns
    if(row >  col):
        newarr = np.zeros((row, row, 3), dtype = int)
        for i in range(0, col):
            for j in range(0,col):
                for k in range(0,3):
                    newarr[i][j][k] = arr[i][j][k] 
        return newarr
    else:
        newarr = np.zeros((col, col, 3), dtype = int)        
        for i in range(0, row):
            for j in range(0,col):
                for k in range(0,3):
                    newarr[i][j][k] = arr[i][j][k] 
        return newarr
'''
matrix_mult:
    -   Receives an array
    -   Creates a cypher array which will be used for matrix multiplication
    -   Saves cypher array into its own list which will later be used for inversion (decryption)
    -   applies matrix multiplication to image array and cypher array.
    -   returns new encrypted image array 
'''
count = 0
cypher_list = []
def matrix_mult(arr):
    start = timer()
    global count
    global overallTimeElapsed

    cypher = np.random.random(arr.shape) # Cypher matrix of arr shape
    cypher_list.append(cypher) # Appends cypher to cypher list for matrix inversion
    result = np.zeros(arr.shape) # Cypher matrix of arr shape

    a2 = arr.reshape(-1, arr.shape[1])
    c2 = cypher.reshape(-1, cypher.shape[1])

    # Matrix multiplication
    res = np.dot(a2, c2.T)

    # Reshape 2D matrix mutl into 3d Array
    res3d = res.reshape(len(a2[0]),len(a2), 3)

    # Converts matrix back into an image, then saves the images
    encrypted_image = Image.fromarray(res3d, 'RGB')    
    encrypted_image.save('./dirty/%07d_encrypted_image.jpg' %count)
    end = timer()
    timeElapsed = end - start
    overallTimeElapsed += timeElapsed 
    print("Frame", count, "Encrypted in %.3f" %timeElapsed)

    # Counter for images that have been processed
    count += 1

def encrypt():
  image_list = []
  if not os.path.exists('./dirty'):
    os.makedirs('./dirty')
  for filename in glob.glob('clean/*.jpg'):
      image_list.append(filename)
  image_list.sort()

  # Read all images from image_list and encrypts them
  for image in image_list:
    img = misc.imread(image)    
    isSquare = isPerfSquare(img)
    if(isSquare):
        print('Its a square.') 
    else:  
        sqrArray = makePerfSquare(img)
        matrix_mult(sqrArray)

'''
maker:
  - Todo
'''
def video_maker(images, outimg=None, fps=24, size=None, is_color=True, format="mp4v"):
    global overallTimeElapsed
    print("Overall Encryption time: %.2f" %overallTimeElapsed)
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    outvid = './dirty_video.mp4'
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
    vid.release()
    print('Video created.')
    return vid

def maker():
  image_list = []
  for filename in glob.glob('dirty/*.jpg'):
      image_list.append(filename)
  image_list.sort()

  video_maker(image_list)


