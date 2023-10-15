import math
from modules.yamaps_api import calculate_distance_and_time
from modules.database import Database
from datetime import datetime
import pytz


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


async def find_atms_in_radius(latitude, longitude, atms_data, radius):
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


async def find_office_in_radius(latitude, longitude, office_data, radius):
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
    for atm in office_data['office']:
        office_latitude = atm["latitude"]
        office_longitude = atm["longitude"]

        distance = haversine(latitude, longitude,
                             office_latitude, office_longitude)

        if distance <= float(radius):
            result.append(atm)

    return result


async def filter_atms(data, required_services):
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


def get_current_load(date, database):
    # Шаг 1: Получаем текущую дату и время
    now = date
    current_day_of_week = now.weekday()
    current_hour = now.hour

    # Шаг 2: Находим записи для текущей даты и времени
    relevant_records = [record for record in database if record[2]
                        == current_day_of_week and record[3] == current_hour]

    # Шаг 3: Вычисляем среднюю загруженность
    total_load = sum(record[4] for record in relevant_records)
    average_load = total_load / \
        len(relevant_records) if relevant_records else 0

    return average_load


async def add_distance_to_json(data, user_cord):
    """ф-ия для расчета расстояния между пользователем и банкоматом

    Args:
        data (list[dict]): Список словарей с информацией о банкоматах
    """
    for i in data:
        time_to_move = await calculate_distance_and_time(user_cord, (i['latitude'],
                                                                     i['longitude']))

        # Добавляем информацию о времени в словарь i
        i['travel_time_car'] = time_to_move[0]
        i['travel_time_walk'] = time_to_move[1]
        i['travel_time_bike'] = time_to_move[2]

    return data


def get_day_of_week():
    today = datetime.today()
    day_of_week = today.isoweekday()  # Получаем текущий день недели (пн - 1, вс - 7)

    return day_of_week


async def workload_atm(atm_id):
    moscow_timezone = pytz.timezone('Europe/Moscow')
    num_weak = get_day_of_week()
    current_time = datetime.now(moscow_timezone)
    formatted_time = current_time.strftime("%H:%M")
    # Разбиваем время на часы и минуты и преобразуем их в целые числа
    hours, minutes = map(int, formatted_time.split(':'))
    # Переводим часы в минуты и складываем с минутами
    time = (hours * 60 + minutes) / 5
    db = Database()
    print(num_weak)
    this_five_minutes_last_weeks = await db.get_atm_load_data(
        atm_id, num_weak, int(time))
    last_five_minutes = await db.get_atm_load_data(
        atm_id, num_weak, int(time) - 5)
    print(this_five_minutes_last_weeks)
    print(last_five_minutes)
    # тут мы считает среднее значение в массиве и умножаем на коэф 0.3
    val1 = sum(
        this_five_minutes_last_weeks) // len(this_five_minutes_last_weeks) * 0.3
    # тут мы берём последние пять минут и умножаем на коэф 0.7
    val2 = last_five_minutes[-1] * 0.7
    print(val1+val2)
    return val1+val2


async def add_workload(data):
    for i in data:
        pass
