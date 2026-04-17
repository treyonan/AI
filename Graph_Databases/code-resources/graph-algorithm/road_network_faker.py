from faker import Faker
import csv 

fake = Faker()

road_network_file = "road_network_data.csv"
road_places_file = "road_places_data.csv"
road_network_relationship = "road_network_relationship.csv"
number = 100

# create fake road network data
interceptor_points = []
places_points = []

for _ in range(number):
    name = fake.street_name()
    place_name = fake.company()
    place_type = fake.random_element(elements=("restaurant", "shop", "park", "museum"))
    latitude = fake.latitude()
    longitude = fake.longitude()

    places_points.append({
        "place_name": place_name,
        "place_type": place_type,
        "latitude": latitude,
        "longitude": longitude,
        "type": "Place"
    })
    interceptor_points.append({"name":name,"type":"Interceptor"})

with open(road_network_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "type"])

    writer.writerows([[point["name"], point["type"]] for point in interceptor_points])

with open(road_places_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["place_name", "place_type", "latitude", "longitude","type"])

    writer.writerows([[point["place_name"], point["place_type"], point["latitude"], point["longitude"], point["type"]] for point in places_points])


# create relationships between road network and places
with open(road_network_relationship, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["interceptor_start_point","interceptor_end_point", "distance_km","time","speed_limit_kmh","road_type","traffic_factor"])


    for interceptor in interceptor_points:
            distance_km = round(fake.random_number(digits=2) + fake.random.random(), 2)
            time = round(distance_km / (fake.random_number(digits=2) + 20) * 60, 2)  # in minutes
            speed_limit_kmh = fake.random_element(elements=(30, 50, 70, 90, 110, 130))
            road_type = fake.random_element(elements=("highway", "main road", "residential", "dirt road"))
            traffic_factor = round(fake.random.uniform(0.5, 2.0), 2)

            random_interceptor_point = fake.random.randint(0, len(interceptor_points)-1)   
            writer.writerow([interceptor["name"], interceptor_points[random_interceptor_point]['name'], distance_km, time, speed_limit_kmh, road_type, traffic_factor])       