import cv2
import numpy as np
from sklearn.cluster import KMeans

def detect_blue_dots(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 150, 50])  
    upper_blue = np.array([140, 255, 255]) 

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((5, 5), np.uint8)
    blue_mask = cv2.dilate(blue_mask, kernel, iterations=1)
    blue_mask = cv2.erode(blue_mask, kernel, iterations=1)

    blue = cv2.bitwise_and(img, img, mask=blue_mask)

    gray = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)

    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blue_dots = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > 100: 
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            blue_dots.append((center, radius))

    return blue_dots, img


def process_image_blue(image_path):
    blue_dots, img = detect_blue_dots(image_path)
    circle_coordinates = []  

    if blue_dots:
        print(f"Total blue dots detected: {len(blue_dots)}")

        for i, dot in enumerate(blue_dots):
            center, radius = dot
            print(f"Blue Dot {i+1}: Center=({center[0]}, {center[1]}) Radius={radius}")
            circle_coordinates.append(center) 

            # Visualization (if needed, uncomment the following lines)
            # label_color = [255, 0, 0]  # Blue color for visualization
            # cv2.circle(img, center, radius, label_color, 2)

        # Show the result (if needed, uncomment the following lines)
        # cv2.imshow('Detected Blue Dots', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    else:
        print("No blue dots were detected.")

    return circle_coordinates, img

if __name__ == "__main__":
    image_path = 'img/tailoredDots_withPickup.jpg'
    coords, processed_img = process_image_blue(image_path)

    for i, coord in enumerate(coords):
        print(f"Blue Dot {i+1}: X={coord[0]}, Y={coord[1]}")

    # Show the result
    # cv2.imshow('Processed Image', processed_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
