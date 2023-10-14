import math


def haversine(lat1, lon1, lat2, lon2):
    # Радиус Земли в километрах
    R = 6371.0

    # Преобразование градусов в радианы
    lat1 = math.radians(float(lat1))
    lon1 = math.radians(float(lon1))
    lat2 = math.radians(float(lat2))
    lon2 = math.radians(float(lon2))

    # Разницы между координатами
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Формула Гаверсинуса
    a = math.sin(dlat/2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Расстояние
    distance = R * c

    return distance


def find_atms_in_radius(latitude, longitude, atms_data, radius):
    result = []
    for atm in atms_data['atms']:
        atm_latitude = atm["latitude"]
        atm_longitude = atm["longitude"]

        distance = haversine(latitude, longitude, atm_latitude, atm_longitude)

        if distance <= float(radius):
            result.append(atm)

    return result
