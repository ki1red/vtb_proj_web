from geopy.distance import geodesic


async def calculate_distance_and_time(start_coordinates, end_coordinates):
    """Функция вернет время в пути от точки до точки"""
    distance = geodesic(start_coordinates, end_coordinates).kilometers
    travel_time_car = (distance / 50) * 60
    travel_time_walk = (distance / 4) * 60
    travel_time_bike = (distance / 15) * 60
    return [travel_time_car, travel_time_walk, travel_time_bike]
