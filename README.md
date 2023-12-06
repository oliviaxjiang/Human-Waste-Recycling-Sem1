
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

# Usage #
Run individual files by running the file as a whole.

# Acknowledgments #
We extend our thanks to an incredible team. I, Olivia Jiang, alongside my teammates Julia Zeng and Courtney Candy,  devoted countless hours to the research and development of this initiative. Our work was expertly supported by the academic guidance of Professor Shane Henderson and Professor Rebecca Nelson, whose expertise in the field has been indispensable. We are also grateful to the CountThings app for its role in image analysis and to OpenAI's ChatGPT-4 for assisting us in streamlining our project's workflow.