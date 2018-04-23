from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
from timeit import default_timer as timer
from scipy import misc
from PIL import Image
import numpy as np
import random
import glob
import cv2 
import os

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
Cryptr:
  - TODO
'''
count = 0
def matrix_mult(image):
    start = timer()
    global count
    global overallTimeElapsed
    # Transforms image into a 1D array
    d = image.flatten()
    nx = len(image)
    ny = len(image[0])
    nz = len(image[0][0])
    # Iterate through the 1D array and 
    # encrypt each value
    for i in range(0, image.size):
        # d[i] = d[i]
        d[i] = random.randint(0,255)
    # Counter for images that have been processed
    count += 1
    # Reshaped 1D image into a matrix
    encrypted_image_3d = d.reshape((nx,ny,nz))

    # Converts matrix back into an image, then saves the images
    encrypted_image = Image.fromarray(encrypted_image_3d, 'RGB')    
    encrypted_image.save('./dirty/%07d_encrypted_image.jpg' %count)
    end = timer()
    timeElapsed = end - start
    overallTimeElapsed += timeElapsed 
    print("Frame", count, "Encrypted in %.3f" %timeElapsed)

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
      matrix_mult(img)

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


