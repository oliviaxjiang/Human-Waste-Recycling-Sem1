import cv2
import numpy as np

def find_green_spaces(image_path, green_color_range):
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_green, upper_green = green_color_range
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    return mask

def detect_blobs(mask, min_size, original_image):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > min_size:
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
	    # Draw a circle at the center of each suitable location
            cv2.circle(original_image, (cX, cY), 10, (0, 0, 255), -1)
  
    cv2.namedWindow('Suitable Locations', cv2.WINDOW_NORMAL)  # Use WINDOW_NORMAL to allow resizing

    # Display the original image with locations marked
    cv2.imshow('Suitable Locations', original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Define green color range in HSV
green_color_range = (np.array([40, 40, 60]), np.array([80, 210, 200]))

# Load the original image
original_image = cv2.imread('nyalendab.png')

# Find green spaces
mask = find_green_spaces('nyalendab.png', green_color_range)

# Detect blobs and display suitable locations
detect_blobs(mask, min_size=190, original_image=original_image.copy())
