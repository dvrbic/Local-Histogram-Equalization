
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def histogram_equalize(img):
    image = img
    
    ints_array = np.zeros(256)
    x_axis, y_axis = image.shape[:2]
    for i in range(0, x_axis):
        for j in range(0, y_axis):
            ints = int(image[i, j])
            ints_array[ints] = ints_array[ints] + 1

    

    MN = 0
    for i in range(1, 256):
        MN = MN + ints_array[i]
   
    
    array_pdf = ints_array/MN
   

    CDF = 0
    CDF_matrix = np.zeros(256)
    for i in range(1, 256):
        CDF = CDF + array_pdf[i]
        CDF_matrix[i] = CDF
    
    
    final_array = np.zeros(256)
    final_array = (CDF_matrix * 255)
    for i in range (1,256):
        final_array[i] = math.ceil(final_array[i])
        if(final_array[i] > 255):
            final_array[i] = 255
    

    new_img = np.zeros(img.shape)
    for i in range(0, x_axis):
        for j in range(0, y_axis):
            for value in range(0, 255):
                if (image[i,j] == value):
                    new_img[i,j] = final_array[value]
                    break
    return new_img

    
def local_hist(img, r):
    rad_range = (r * 2) + 1
    new_img = np.empty([img.shape[0], img.shape[1]], dtype=float)
    window = np.zeros((rad_range,rad_range))
    new_window = np.zeros((rad_range,rad_range))
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if x < r or y < r or (x >= (img.shape[0]-r)) or (y >= (img.shape[1]-r)):
                new_img[x][y] = 0
                pass
            else:
                for i in range(-1*r, r+1):
                    for j in range(-1*r, r+1):
                        window[i][j] = img[x+i,y+i]
                        
                        #print(window[x][y])
                        #valuer = valuer + ((img[x+i, y+j][2])*h[r+i, r+j])
                        #valueg = valueg + ((img[x+i, y+j][1])*h[r+i, r+j])
                        #valueb = valueb + ((img[x+i, y+j][0])*h[r+i, r+j])
                new_window = histogram_equalize(window)
                for k in range(-1*r, r+1):
                    for L in range(-1*r, r+1):
                        new_img[x+k][y+L] = new_window[r+k][r+L]
    return new_img

input_image = cv2.imread('histo.PNG', 0)
r = int(input("Please enter a kernel radius: "))
out_image = local_hist(input_image, r)
cv2.imwrite('new_histo2.PNG', out_image)
