import cv2
import numpy as np
from sklearn.cluster import KMeans
#test
def detect_red_circles(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range of red color in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Threshold the HSV image to get only red colors
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Use the red mask to get the red parts of the image
    red = cv2.bitwise_and(img, img, mask=red_mask)

    # Convert to grayscale
    gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
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

def process_image_green(image_path, n_clusters=12):
    circles, img = detect_red_circles(image_path)
    circle_coordinates = []  # List to store the coordinates of the circles

    if circles is not None:
        print(f"Total circles detected: {len(circles[0])}")
        circle_colors = extract_colors(circles, img)
        labels = cluster_circles(circles, circle_colors, n_clusters=n_clusters)

        # Visualization and coordinates extraction
        for i, circle in enumerate(circles[0]):
            print(f"Circle {i+1}: Center=({circle[0]}, {circle[1]}) Radius={circle[2]}")
            x, y, r = int(circle[0]), int(circle[1]), int(circle[2])
            circle_coordinates.append((x, y))  # Adding coordinates to the list

            # Color assignment based on cluster label for visualization
            label_color = [0,0,0]
            cv2.circle(img, (x, y), r, label_color, 4)

        # Show the result
        # cv2.imshow('Clustered Circles', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    # Returning the coordinates and the labeled image
    return circle_coordinates, img

# The following lines are for testing the module directly
if __name__ == "__main__":
    image_path = 'researchPython/tailoredDots_withPickup.jpg'
    coords, processed_img = process_image_green(image_path)

    # Printing the coordinates
    for i, coord in enumerate(coords):
        print(f"Circle {i+1}: X={coord[0]}, Y={coord[1]}")

    # Show the result
    cv2.imshow('Processed Image', processed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()