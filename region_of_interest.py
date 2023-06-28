import pandas as pd 
import numpy as np
import cv2
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Read in the image and convert to grayscale
# Here we read a .jpeg and convert to 0,255 bytescale
image = mpimg.imread('road.jpeg')
gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)


# Define a kernel size for Gaussian smoothing / blurring
kernel_size = 5 # Must be an odd number (3, 5, 7...)
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)


# Define our parameters for Canny and run it
low_threshold = 100 # 180
high_threshold = 200 # 240
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)


# Display the image of the canny edge detected image
plt.imshow(edges, cmap='Greys_r')
plt.title("Canny Edge Detection Image")
plt.show()


#apply mask
lowerLeftPoint = [130, 540]
upperLeftPoint = [450, 315]
upperRightPoint = [520, 315]
lowerRightPoint = [915, 540]

pts = np.array([[lowerLeftPoint, upperLeftPoint, upperRightPoint, lowerRightPoint]], dtype=np.int32)

image = edges.copy()
#defining a blank mask to start with
mask = np.zeros_like(image)

#defining a 3 channel or 1 channel color to fill the mask with depending on the input image
if len(image.shape) > 2:
    channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
else:
    ignore_mask_color = 255

#filling pixels inside the polygon defined by "vertices" with the fill color    
cv2.fillPoly(mask, pts, ignore_mask_color)
    
#returning the image only where mask pixels are nonzero
masked_image = cv2.bitwise_and(image, mask)

plt.imshow(masked_image, cmap='Greys_r')
plt.title("Region of interested Image")
plt.show()

