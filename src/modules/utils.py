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
    """_summary_

    Args:
        latitude (_type_): ширина
        longitude (_type_): долгота
        atms_data (_type_): все банкоматы
        radius (_type_): радиус поиска

    Returns:
        dict: подходящие банкоматы
    """
    result = []
    for atm in atms_data['atms']:
        atm_latitude = atm["latitude"]
        atm_longitude = atm["longitude"]

        distance = haversine(latitude, longitude, atm_latitude, atm_longitude)

        if distance <= float(radius):
            result.append(atm)

    return result


def filter_atms(data, required_services):
    # Функция для фильтрации банкоматов

    def filter_atm(atm):
        for service in required_services:
            if (
                atm["services"].get(service) is None
                or atm["services"][service]["serviceActivity"] != "AVAILABLE"
            ):
                return False
        return True

    # Применяем фильтр и получаем отфильтрованный список

    filtered_atms = list(filter(filter_atm, data))
    # Возвращаем отфильтрованный JSON
    return filtered_atms
