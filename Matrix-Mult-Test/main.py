import numpy as np
from numpy.linalg import inv

aThree = np.array([[[1,2,3], [4,5,6], [7,8,9]]
            , [[10,11,12], [13,14,15], [16,17,18]]
            , [[19,20,21], [22,23,24], [25,26,27]]])
bThree = np.array([[[100,101,102], [103,104,105], [106,107,108]]
            , [[110,111,112], [113,114,115], [116,117, 118]]
            , [[119,120,121], [122,123,124], [125,124,125]]])    

aTwo = aThree.transpose(2,0,1).reshape(-1,aThree.shape[1])
bTwo = bThree.transpose(2,0,1).reshape(-1,bThree.shape[1])

aCol = len(aTwo[0])
bCol = len(bTwo[0])
aRow = len(aTwo)
bRow = len(bTwo)

result = np.zeros((aRow, bCol), dtype=int)

for i in range(0, aRow):
    for j in range(0, bCol):
        for k in range(0, aCol):
            result[i][j] += aTwo[i][k] * bTwo[k][k] 

result_3d = result.reshape(np.roll(aThree.shape,1)).transpose(1,2,0)

# print(result_3d)
