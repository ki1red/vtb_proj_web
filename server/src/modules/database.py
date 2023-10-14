import json
import asyncio
import aiosqlite
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(current_directory, 'db.db')


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
