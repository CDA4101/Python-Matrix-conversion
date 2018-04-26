from scipy import misc
from PIL import Image
import numpy as np
import math
from numpy.linalg import inv

'''
isPerfSquare:
    -   Take in a 3D array
    -   Compares the length of the rows vs columns
    -   returns a boolean 
'''                       
def isPerfSquare(arr):
    row = len(arr) #rows
    col = len(arr[0]) #columns
    print("Number of rows: ", row,'\n')
    print("Number of columns: ", col,'\n')
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
cypher_list = []
def matrix_mult(arr):
    cypher = np.random.random(arr.shape) # Cypher matrix of arr shape
    cypher_list.append(cypher) # Appends cypher to cypher list for matrix inversion
    result = np.zeros(arr.shape) # Cypher matrix of arr shape

    a2 = arr.reshape(-1, arr.shape[1])
    c2 = cypher.reshape(-1, cypher.shape[1])
    
    # Matrix multiplication
    res = np.dot(a2, c2.T)

    # Reshape 2D -> 3D
    res3d = res.reshape(len(a2[0]),len(a2), 3)
    return res3d

'''
decrypt:
    - todo
'''
def decrypt(image):
    global cypher_list
    cypher = np.asarray(cypher_list[0])
    img = image[:2628,:2628, :3]
    cypherRoll = np.rollaxis(cypher,2,0)
    imgRoll = np.rollaxis(img,2,0)
    cInv = inv(cypherRoll)
    pinga = np.dot(imgRoll, cInv) 
    print(pinga)


'''
Function Calls
'''

#Reading the image and making it a matrix
image = misc.imread('test.png')
enc_image = misc.imread('enc.png')
isSquare = isPerfSquare(image)  

if(isSquare):
    print('Its a square.')
else:
    print('Converting to perfect square..')        
    sqrArray = makePerfSquare(image)
    print('Multiplying the Matrices')
    encrypted_image = (matrix_mult(sqrArray))
    final_img = Image.fromarray(encrypted_image, 'RGB')
    final_img.save('enc.png')
    print('Decrypting the frame.')
    decrypt(enc_image)

