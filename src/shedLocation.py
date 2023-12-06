from countHousehold import process_image_household
from countGreen import process_image_green
from countBlue import process_image_blue

def allocate_sheds(circle_coord_house, combined_green_blue_coords, shed_coverage_radius=50, max_households_per_shed=16, min_coverage=0.95, max_sheds=70):
    def distance(coord1, coord2):
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5
    
    allocation = {}
    for house in circle_coord_house:
        distances = [distance(house, dot) for dot in combined_green_blue_coords]
        nearest_dot_index = min(range(len(distances)), key=distances.__getitem__)
        if distances[nearest_dot_index] <= shed_coverage_radius:
            nearest_dot = combined_green_blue_coords[nearest_dot_index]
            if nearest_dot not in allocation:
                allocation[nearest_dot] = []
            allocation[nearest_dot].append(house)

    sorted_allocations = sorted(allocation.items(), key=lambda item: len(item[1]), reverse=True)
    
    sheds_at_locations = {}
    shed_count = 0
    for dot, houses in sorted_allocations:
        if shed_count >= max_sheds:
            break  
        sheds_needed = min(-(-len(houses) // max_households_per_shed), max_sheds - shed_count)
        sheds_at_locations[dot] = sheds_needed
        shed_count += sheds_needed

    total_households = len(circle_coord_house)
    households_swerved = sum(min(len(houses), sheds_at_locations.get(dot, 0) * max_households_per_shed) for dot, houses in allocation.items())
    # coverage = households_served / total_households

    # if coverage < min_coverage:
    #     raise ValueError(f"Coverage target of {min_coverage:.2f} not met. Current coverage is {coverage:.2f}.")

    return sheds_at_locations

circle_coord_house, _ = process_image_household("img/households.jpg")
circle_coord_green, _ = process_image_green("img/tailoredDots.jpg")
circle_coord_blue, _ = process_image_blue('img/tailoredDots_withPickup.jpg')

combined_green_blue_coords = circle_coord_green + circle_coord_blue

shed_coverage_radius = 500
max_sheds = 240

try:
    shed_allocation = allocate_sheds(circle_coord_house, combined_green_blue_coords, shed_coverage_radius=shed_coverage_radius, max_sheds=max_sheds)
    total_sheds = sum(shed_allocation.values())
    print("Shed allocation complete. Shed locations and counts:")
    for location, count in shed_allocation.items():
        print(f"Location: {location}, Sheds: {count}")
    print(f"Total sheds allocated: {total_sheds}") 
except ValueError as e:
    print(e)



