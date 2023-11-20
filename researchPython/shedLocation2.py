# from countHousehold import process_image_household
# from countGreen import process_image_green

# circle_coord_house, processed_image_house = process_image_household("households.jpg")
# circle_coord_green, processed_image_green = process_image_green("tailoredDots.jpg")

# for i, coord in enumerate(circle_coord_house):
#     print(f"Circle {i+1}: X={coord[0]}, Y={coord[1]}")

# for i, coord in enumerate(circle_coord_green):
#     print(f"Circle {i+1}: X={coord[0]}, Y={coord[1]}")

from countHousehold import process_image_household
from countGreen import process_image_green

def allocate_sheds(circle_coord_house, circle_coord_green, shed_coverage_radius=50, max_households_per_shed=16, min_coverage=1, max_sheds=58):
    # Function to calculate Euclidean distance between two coordinates
    def distance(coord1, coord2):
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

    # Find the nearest green dot for each household within the shed_coverage_radius
    allocation = {}
    #nodot = {}
    for house in circle_coord_house:
        # Find distances to all green dots
        distances = [distance(house, green) for green in circle_coord_green]
        # Get the nearest green dot
        nearest_green_dot_index = min(range(len(distances)), key=distances.__getitem__)
        if distances[nearest_green_dot_index] <= shed_coverage_radius:
            if circle_coord_green[nearest_green_dot_index] not in allocation:
                allocation[circle_coord_green[nearest_green_dot_index]] = []
            allocation[circle_coord_green[nearest_green_dot_index]].append(house)
        #else:
            #nodot.append(house)
    # Sort allocations by number of households they can serve
    sorted_allocations = sorted(allocation.items(), key=lambda item: len(item[1]), reverse=True)

    # Determine how many sheds to build at each green dot location
    sheds_at_locations = {}
    shed_count = 0
    for green_dot, houses in sorted_allocations:
        if shed_count >= max_sheds:
            break  # Stop if the maximum number of sheds has been reached
        sheds_needed = min(-(-len(houses) // max_households_per_shed), max_sheds - shed_count)
        sheds_at_locations[green_dot] = sheds_needed
        shed_count += sheds_needed

    # Calculate the coverage to ensure it's above the minimum required
    total_households = len(circle_coord_house)
    # Only calculate households served for green dots where sheds have been allocated
    households_served = sum(min(len(houses), sheds_at_locations.get(green_dot, 0) * max_households_per_shed) for green_dot, houses in allocation.items())
    coverage = households_served / total_households

    if coverage < min_coverage:
        print(f"Coverage target of {min_coverage:.2f} not met. Current coverage is {coverage:.2f}.")

    return sheds_at_locations

# Obtain the coordinates from the images
circle_coord_house, processed_image_house = process_image_household("households.jpg")
circle_coord_green, processed_image_green = process_image_green("tailoredDots.jpg")

shed_coverage_radius = 500
max_sheds = 58

# Use the allocation function to determine shed locations
try:
    shed_allocation = allocate_sheds(circle_coord_house, circle_coord_green, shed_coverage_radius=shed_coverage_radius, max_sheds=max_sheds)
    total_sheds = sum(shed_allocation.values())  # Calculate the total number of sheds allocated
    print("Shed allocation complete. Shed locations and counts:")
    for location, count in shed_allocation.items():
        print(f"Location: {location}, Sheds: {count}")
    print(f"Total sheds allocated: {total_sheds}")  # Print the total amount of sheds
    #for houses in nodot:
        #print(houses)
except ValueError as e:
    print(e)
