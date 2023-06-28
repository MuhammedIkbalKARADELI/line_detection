
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

#Read in and grayscale the image
image = mpimg.imread('road.jpeg')
gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

# Define a kernel size and apply Gaussian smoothing
kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

# Define our parameters for Canny and apply
low_threshold = 100
high_threshold = 200
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

# Next we'll create a masked edges image using cv2.fillPoly()
mask = np.zeros_like(edges)   
ignore_mask_color = 255   

# This time we are defining a four sided polygon to mask
imshape = image.shape
vertices = np.array([[(0,imshape[0]),(450, 290), (490, 290), (imshape[1],imshape[0])]], dtype=np.int32)
cv2.fillPoly(mask, vertices, ignore_mask_color)
masked_edges = cv2.bitwise_and(edges, mask)

# Define the Hough transform parameters
# Make a blank the same size as our image to draw on
rho = 1 # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 2     # minimum number of votes (intersections in Hough grid cell)
min_line_length = 4 #minimum number of pixels making up a line
max_line_gap = 5    # maximum gap in pixels between connectable line segments
line_image = np.copy(image)*0 # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

# Iterate over the output "lines" and draw lines on a blank image
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)

# Create a "color" binary image to combine with line image
color_edges = np.dstack((edges, edges, edges)) 


# Draw the lines on the edge image
lines_edges = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0)
lines_edges = cv2.polylines(lines_edges,vertices, True, (0,0,255), 10)

#apply mask
lowerLeftPoint = [130, 540]
upperLeftPoint = [450, 315]
upperRightPoint = [520, 315]
lowerRightPoint = [915, 540]

pts = np.array([[lowerLeftPoint, upperLeftPoint, upperRightPoint, lowerRightPoint]], dtype=np.int32)

image = lines_edges.copy()
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

# Draw the lines on the edge image
lines_edges = cv2.addWeighted(masked_image, 0.8, line_image, 1, 0)
lines_edges = cv2.polylines(lines_edges,vertices, True, (0,0,255), 10)

plt.imshow(lines_edges)
plt.title("Colored Lane line [In RED] and Region of Interest [In Blue]")
plt.savefig("Hough_transform.png")
plt.show()