
# Decentralized Approach to Waste Processing (For Nyalenda B, Kisumu, Kenya)

# Introduction #
This project aims to optimize the circulation of Kontiki kilns throughout the Nylenda B area in Kenya to enable efficient pyrolysis of human waste, providing the community with a cleaner, less polluting waste processing method.

# Project Objective #
Develop an automated system to identify optimal routes for kiln circulation to maximize coverage and accessibility for the local population, with the aid of image recognition and geospatial analysis.

# Installation #
### Prerequisites ###
- Python 3.7 or higher.
- pip (Python Package Installer).

### Installing Dependencies ###
#### Install OpenCV for image processing ####
- pip install opencv-python-headless

#### Install NumPy for numerical computing ####
- pip install numpy

#### Install scikit-learn for the KMeans clustering algorithm ####
- pip install scikit-learn

# Repository Structure #
Explanation of the scripts included in the repository and their roles:

- `green.py`: Identifies green locations on satellite maps.
- `countGreen.py`: Counts green dots and extracts coordinates.
- `countHousehold.py`: Identifies household locations from dotted maps.
- `countBlue.py`: Counts blue dots representing road locations.
- `shedLocation.py`: Algorithm for assigning households to nearest kiln location.

# File Specifications #
#### green.py ####
This Python script is designed to identify and mark green spaces in an image. It first converts the image to the HSV color space and then applies a mask to isolate the green areas based on a specified color range.
- The find_green_spaces function returns this mask
- The detect_blobs function uses the mask to find and highlight significant green areas (blobs) larger than a minimum size.
#### countGreen.py, countHousehold.py, and countBlue.py ####
These scripts contains a set of functions for detecting, extracting, and clustering red/blue/yellow circles from a given image, which is primarily used to identify locations of interest such as households or resource points. 
- The detect_circles/detect_red_circles/detect_blue_dots function reads an image and filters for the corresponding hues to detect circles using the Hough Transform method.
- The extract_colors function calculates the average color within each detected circle.
- The cluster_circles function applies KMeans clustering to group circles based on their spatial coordinates and color features, allowing for categorization of similar points.
- The process_image_green function orchestrates the detection and clustering process and returns the coordinates of the circles and the processed image.
#### shedLocation.py ####
This Python script is designed to allocate sanitation facilities (referred to as 'sheds') in the Nylenda B area for efficient waste processing. It imports functions from countHousehold, countGreen, and countBlue modules to process images and identify household, green space, and road locations, respectively. The allocate_sheds function calculates the optimal placement of sheds based on proximity to households, green and blue coordinates combined, and predefined constraints such as coverage radius, maximum households per shed, and minimum coverage requirements. It outputs the allocation of sheds to locations and ensures the coverage meets the set target, raising an error if not. The main execution block processes the images to get coordinates, combines green and blue coordinates, sets parameters for coverage radius and maximum number of sheds, and attempts to allocate sheds while catching any exceptions related to coverage constraints.

# Usage #
Run individual files by running the file as a whole.

# Acknowledgments #
We extend our thanks to an incredible team. I, Olivia Jiang, alongside my teammates Julia Zeng and Courtney Candy,  devoted countless hours to the research and development of this initiative. Our work was expertly supported by the academic guidance of Professor Shane Henderson and Professor Rebecca Nelson, whose expertise in the field has been indispensable. We are also grateful to the CountThings app for its role in image analysis and to OpenAI's ChatGPT-4 for assisting us in streamlining our project's workflow.