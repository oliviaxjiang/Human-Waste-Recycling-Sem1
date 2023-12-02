import cv2
import numpy as np
from sklearn.cluster import KMeans

def detect_blue_circles(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range of blue color in HSV
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Threshold the HSV image to get only blue colors
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Use the blue mask to get the blue parts of the image
    blue = cv2.bitwise_and(img, img, mask=blue_mask)

    # Convert to grayscale for circle detection
    gray = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=20, param2=10, minRadius=3, maxRadius=15)
    return circles, img

def extract_colors(circles, img):
    circle_colors = []
    for circle in np.uint16(np.around(circles[0])):
        x, y, r = int(circle[0]), int(circle[1]), int(circle[2])
        mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        cv2.circle(mask, (x, y), r, 255, thickness=-1)
        mean_color = cv2.mean(img, mask=mask)[:3]
        circle_colors.append(mean_color)
    return circle_colors

def cluster_circles(circles, circle_colors, n_clusters=12):
    features = []
    for circle, color in zip(circles[0], circle_colors):
        features.append(np.hstack([circle[:2], color]))
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(features)
    return labels

def process_image_blue(image_path, n_clusters=12):
    circles, img = detect_blue_circles(image_path)
    circle_coordinates = []

    if circles is not None:
        print(f"Total blue circles detected: {len(circles[0])}")
        circle_colors = extract_colors(circles, img)
        labels = cluster_circles(circles, circle_colors, n_clusters=n_clusters)

        for i, circle in enumerate(circles[0]):
            x, y, r = int(circle[0]), int(circle[1]), int(circle[2])
            circle_coordinates.append((x, y))
            label_color = [255, 0, 0]  # Blue color for visualization
            cv2.circle(img, (x, y), r, label_color, 4)

    return circle_coordinates, img

if __name__ == "__main__":
    image_path = 'researchPython/tailoredDots_withPickup.jpg'  # Change to your image path
    coords, processed_img = process_image_blue(image_path)

    for i, coord in enumerate(coords):
        print(f"Blue Circle {i+1}: X={coord[0]}, Y={coord[1]}")

    cv2.imshow('Processed Image', processed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
