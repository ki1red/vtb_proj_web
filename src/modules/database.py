import json
import asyncio
import aiosqlite

async def load_json_to_db(json_file, db_name):
    # Открываем соединение с базой данных
    async with aiosqlite.connect(db_name) as db:
        # Создаем курсор
        cursor = await db.cursor()

        # Создаем таблицу, если она не существует
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS atms (
                address TEXT,
                latitude REAL,
                longitude REAL,
                all_day INTEGER
            )
        ''')

        # Читаем данные из JSON
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Итерируемся по банкоматам
        for atm in data["atms"]:
            # Извлекаем данные
            address = atm["address"]
            latitude = atm["latitude"]
            longitude = atm["longitude"]
            all_day = atm["allDay"]

            # Вставляем данные в базу данных
            await cursor.execute('''
                INSERT INTO atms (address, latitude, longitude, all_day)
                VALUES (?, ?, ?, ?)
            ''', (address, latitude, longitude, all_day))

        # Коммитим изменения
        await db.commit()

# Используем функцию
asyncio.run(load_json_to_db('atms.txt', 'db.db'))
