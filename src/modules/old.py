# async def load_json_to_db(json_file, db_name):
#     # Открываем соединение с базой данных
#     async with aiosqlite.connect(db_name) as db:
#         # Создаем курсор
#         cursor = await db.cursor()

#         # Создаем таблицу atms, если она не существует
#         await cursor.execute('''
#             CREATE TABLE IF NOT EXISTS atms (
#                 id INTEGER PRIMARY KEY,
#                 address TEXT,
#                 latitude REAL,
#                 longitude REAL,
#                 all_day INTEGER
#             )
#         ''')

#         # Создаем таблицу services, если она не существует
#         await cursor.execute('''
#             CREATE TABLE IF NOT EXISTS services (
#                 id INTEGER PRIMARY KEY,
#                 atm_id INTEGER,
#                 service_name TEXT,
#                 capability TEXT,
#                 activity TEXT,
#                 FOREIGN KEY (atm_id) REFERENCES atms (id)
#             )
#         ''')

#         # Читаем данные из JSON
#         with open(json_file, 'r') as f:
#             data = json.load(f)

#         # Итерируемся по банкоматам
#         for atm in data["atms"]:
#             # Извлекаем данные
#             address = atm["address"]
#             latitude = atm["latitude"]
#             longitude = atm["longitude"]
#             all_day = atm["allDay"]

#             # Вставляем данные в таблицу atms и получаем id новой записи
#             await cursor.execute('''
#                 INSERT INTO atms (address, latitude, longitude, all_day)
#                 VALUES (?, ?, ?, ?)
#             ''', (address, latitude, longitude, all_day))
#             atm_id = cursor.lastrowid

#             # Итерируемся по службам и вставляем их в таблицу services
#             for service_name, service_info in atm["services"].items():
#                 capability = service_info["serviceCapability"]
#                 activity = service_info["serviceActivity"]

#                 await cursor.execute('''
#                     INSERT INTO services (atm_id, service_name,
#                                       capability, activity)
#                     VALUES (?, ?, ?, ?)
#                 ''', (atm_id, service_name, capability, activity))

#         # Коммитим изменения
#         await db.commit()

import sqlite3
import random


conn = sqlite3.connect('db.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS atm_load (
        id INTEGER PRIMARY KEY,
        atm_id INTEGER,
        day_of_week INTEGER,
        hour INTEGER,
        load INTEGER,
        FOREIGN KEY (atm_id) REFERENCES atm(id)
    )
''')


# Получаем информацию о банкоматах
cursor.execute('SELECT id, all_day FROM atms')
atms = cursor.fetchall()

# Заполняем информацию о загруженности
for atm_id, all_day in atms:
    for day_of_week in range(1, 8):  # 1-понедельник, 2-вторник, ..., 7-воскресенье
        for hour in range(24):  # 0-23 часа
            if all_day == 1 or (10 <= hour <= 16):
                # Равномерная загруженность от 25% до 35%
                base_load = random.randint(25, 35)
            elif (12 <= hour <= 14) or hour == 18:
                # Пиковая загруженность от 65% до 75%
                base_load = random.randint(65, 75)
            else:
                base_load = 0

            # Добавим небольшой рандом к базовой загруженности
            random_load = random.randint(-5, 5)
            # Убеждаемся, что нагрузка не меньше 0
            load = max(base_load + random_load, 0)

            cursor.execute('''
                INSERT INTO atm_load (atm_id, day_of_week, hour, load)
                VALUES (?, ?, ?, ?)
            ''', (atm_id, day_of_week, hour, load))

# Сохраняем изменения и закрываем соединение с базой данных
conn.commit()
conn.close()

print("Информация о загруженности банкоматов успешно заполнена.")
