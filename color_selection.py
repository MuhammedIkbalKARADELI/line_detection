import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


# Read in the image
image = mpimg.imread('straight_lines2.jpg')


# Grab the x and y size and make a copy of the image
# We copy the image because we don't want to cahnge the original image
ysize = image.shape[0]
xsize = image.shape[1]
color_select = np.copy(image)
print(color_select.shape)

# Define color selection criteria
# We define the thershold color to detect the line 
###### MODIFY THESE VARIABLES TO MAKE YOUR COLOR SELECTION  ##### 
red_threshold = 200
green_threshold = 200
blue_threshold = 200

rgb_threshold = [red_threshold, green_threshold, blue_threshold]

# Do a boolean or with the "|" character to identify pixels below the thresholds
# Image datset is 3D.  
thresholds = (image[:,:,0] < rgb_threshold[0]) \
            | (image[:,:,1] < rgb_threshold[1]) \
            | (image[:,:,2] < rgb_threshold[2])
color_select[thresholds] = [0,0,0]


print(color_select[thresholds].shape) ## (151158, 3)

# Display the image
plt.imshow(image)
plt.title("Input Image")
plt.show()
plt.imshow(color_select)
plt.title("Color Selected Image")
plt.savefig("Color_Selected.png")
plt.show()


