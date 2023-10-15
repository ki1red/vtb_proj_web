import json
import asyncio
import aiosqlite
import os
import requests
import requests

current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'db.db')

if not os.path.exists(database_path):
    url = 'https://drive.google.com/uc?export=download&id=1SJaAkKZKEainP7Z22H4j8IGnIuxdlE3i&confirm=t&uuid=227d964b-e7f5-4bc8-94d5-28cf56197987&at=AB6BwCBX9UDz5IbeIE42grXIB63F:1697333163318'
    response = requests.get(url, stream=True)

    print(f'База данных не найдена. Загружаю...')

    total_size = int(response.headers.get('content-length', 0))
    total_size_in_mb = total_size / (1024 * 1024)  # переводим в мегабайты
    block_size = 1024

    with open(database_path, 'wb') as file:
        downloaded = 0
        for data in response.iter_content(block_size):
            file.write(data)
            downloaded += len(data)
            downloaded_in_mb = downloaded / \
                (1024 * 1024)  # переводим в мегабайты
            print(
                f'Загружено: {downloaded_in_mb:.2f} МБ / {total_size_in_mb:.2f} МБ', end='\r')

    print(f'Файл {database_path} загружен успешно.')
else:
    print(f'Нашел бд {database_path}')


class Database():
    def __init__(self) -> None:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        database_path = os.path.join(current_directory, 'db.db')
        self.database_path = database_path

    async def get_atms_data(self):
        # Открываем соединение с базой данных
        async with aiosqlite.connect(self.database_path) as db:
            # Создаем курсор
            cursor = await db.cursor()

            # Выполняем SQL-запрос для получения данных
            await cursor.execute('''
                SELECT atms.address, atms.latitude, atms.longitude, atms.all_day,
                    services.service_name, services.capability, services.activity
                FROM atms
                JOIN services ON atms.id = services.atm_id
            ''')

            # Получаем все строки результата
            rows = await cursor.fetchall()

            # Создаем словарь для хранения данных
            atms_data = {}

            for row in rows:
                address, latitude, longitude, all_day, service_name, capability, activity = row

                # Если банкомат еще не включен в результат, добавляем его
                if address not in atms_data:
                    atms_data[address] = {
                        "address": address,
                        "latitude": latitude,
                        "longitude": longitude,
                        "allDay": bool(all_day),
                        "services": {}
                    }

                # Добавляем данные о службе к соответствующему банкомату
                atms_data[address]["services"][service_name] = {
                    "serviceCapability": capability,
                    "serviceActivity": activity
                }

            # Преобразуем данные в JSON и возвращаем
            return json.dumps({"atms": list(atms_data.values())},
                              ensure_ascii=False, indent=4)

    async def get_records_by_atm_id(self, atm_id):
        async with aiosqlite.connect(self.database_path) as db:
            # Выполняем запрос к базе данных
            async with db.execute('SELECT * FROM atm_load WHERE atm_id = ?',
                                  (atm_id,)) as cursor:
                records = await cursor.fetchall()

        return records

    async def get_departments_data(self):
        # Открываем соединение с базой данных
        async with aiosqlite.connect(self.database_path) as db:
            # Создаем курсор
            cursor = await db.cursor()

            # Выполняем SQL-запрос для получения данных
            await cursor.execute('''
                SELECT * FROM departments
            ''')

            # Получаем все строки результата
            rows = await cursor.fetchall()

            # Создаем список для хранения данных
            departments_data = []

            for row in rows:
                data = {
                    "salePointName": row[1],
                    "address": row[2],
                    "status": row[3],
                    "openHours": json.loads(row[4]),
                    "rko": row[5],
                    "openHoursIndividual": json.loads(row[6]),
                    "officeType": row[7],
                    "salePointFormat": row[8],
                    "suoAvailability": row[9],
                    "hasRamp": row[10],
                    "latitude": row[11],
                    "longitude": row[12],
                    "metroStation": row[13],
                    "distance": row[14],
                    "kep": bool(row[15]),
                    "myBranch": bool(row[16])
                }

                departments_data.append(data)

            # Преобразуем данные в JSON и возвращаем
            return departments_data

    async def get_atm_load_data(self, atm_id, day_of_week, minute):
        async with aiosqlite.connect(self.database_path) as db:
            cursor = await db.cursor()

            await cursor.execute('''
                SELECT load FROM atm_load 
                WHERE atm_id = ? AND day_of_week = ? AND minute = ?
            ''', (atm_id, day_of_week, minute))

            result = await cursor.fetchall()  # Используем fetchall для получения всех значений

            if result:
                return [row[0] for row in result]  # Возвращаем массив значений
            else:
                return None

    async def get_id_by_location(self, x, y):
        async with aiosqlite.connect(self.database_path) as db:
            cursor = await db.cursor()

            await cursor.execute('''
                SELECT load FROM atm
                WHERE atm_id = ? AND day_of_week = ? AND minute = ?
            ''', (atm_id, day_of_week, minute))
