import cv2
import numpy as np
from sklearn.cluster import KMeans

def detect_circles(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=5,
                            param1=1, param2=15, minRadius=1, maxRadius=6)
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

def process_image_household(image_path, n_clusters=12):
    circles, img = detect_circles(image_path)
    circle_coordinates = []  

    if circles is not None:
        print(f"Total circles detected: {len(circles[0])}")
        circle_colors = extract_colors(circles, img)
        labels = cluster_circles(circles, circle_colors, n_clusters=n_clusters)

        for i, circle in enumerate(circles[0]):
            print(f"Circle {i+1}: Center=({circle[0]}, {circle[1]}) Radius={circle[2]}")
            x, y, r = int(circle[0]), int(circle[1]), int(circle[2])
            circle_coordinates.append((x, y)) 

            label_color = [0,0,0]
            cv2.circle(img, (x, y), r, label_color, 4)

        cv2.imshow('Clustered Circles', img)
        cv2.waitKey(100)
        cv2.destroyAllWindows()

    return circle_coordinates, img

if __name__ == "__main__":
    image_path = 'img/households.jpg'
    coords, processed_img = process_image_household(image_path)

    for i, coord in enumerate(coords):
        print(f"Circle {i+1}: X={coord[0]}, Y={coord[1]}")


