import cv2
import numpy as np
from sklearn.cluster import KMeans

def detect_blue_dots(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Adjust these values based on your analysis of the blue color
    lower_blue = np.array([100, 150, 50])  # Use your specific blue HSV lower range
    upper_blue = np.array([140, 255, 255])  # Use your specific blue HSV upper range

    # Threshold the HSV image to get only blue colors
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Optional: Apply morphological operations to close gaps in the blue dots
    kernel = np.ones((5, 5), np.uint8)
    blue_mask = cv2.dilate(blue_mask, kernel, iterations=1)
    blue_mask = cv2.erode(blue_mask, kernel, iterations=1)

    # Use the blue mask to get the blue parts of the image
    blue = cv2.bitwise_and(img, img, mask=blue_mask)

    # Convert to grayscale for shape detection
    gray = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)

    # Find contours instead of HoughCircles, as the shapes are not perfect circles
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Approximate contours to polygons + get bounding rects and circles
    blue_dots = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > 100:  # Filter out very small dots by setting a minimum area
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            blue_dots.append((center, radius))

    return blue_dots, img


def process_image_blue(image_path):
    blue_dots, img = detect_blue_dots(image_path)
    circle_coordinates = []  # List to store the coordinates of the circles

    if blue_dots:
        print(f"Total blue dots detected: {len(blue_dots)}")

        # Visualization and coordinates extraction
        for i, dot in enumerate(blue_dots):
            center, radius = dot
            print(f"Blue Dot {i+1}: Center=({center[0]}, {center[1]}) Radius={radius}")
            circle_coordinates.append(center)  # Adding center coordinates to the list

            # Visualization (if needed, uncomment the following lines)
            # label_color = [255, 0, 0]  # Blue color for visualization
            # cv2.circle(img, center, radius, label_color, 2)

        # Show the result (if needed, uncomment the following lines)
        # cv2.imshow('Detected Blue Dots', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    else:
        print("No blue dots were detected.")

    # Returning the coordinates and the labeled image
    return circle_coordinates, img

if __name__ == "__main__":
    image_path = 'researchPython/tailoredDots_withPickup.jpg'
    coords, processed_img = process_image_blue(image_path)

    # Printing the coordinates
    for i, coord in enumerate(coords):
        print(f"Blue Dot {i+1}: X={coord[0]}, Y={coord[1]}")

    # Show the result
    # cv2.imshow('Processed Image', processed_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
