import aiosqlite
import json
import asyncio


async def create_departments_table(db_name):
    # Открываем соединение с базой данных
    async with aiosqlite.connect(db_name) as db:
        # Создаем курсор
        cursor = await db.cursor()

        # Создаем таблицу departments, если она не существует
        await cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_point_name TEXT,
                address TEXT,
                status TEXT,
                open_hours TEXT,
                rko TEXT,
                open_hours_individual TEXT,
                office_type TEXT,
                sale_point_format TEXT,
                suo_availability TEXT,
                has_ramp TEXT,
                latitude REAL,
                longitude REAL,
                metro_station TEXT,
                distance INTEGER,
                kep INTEGER,
                my_branch INTEGER
            )
            '''
        )

        # Коммитим изменения
        await db.commit()


async def load_json_to_db(json_file, db_name):
    # Открываем соединение с базой данных
    async with aiosqlite.connect(db_name) as db:
        # Создаем курсор
        cursor = await db.cursor()

        # Открываем и читаем JSON файл
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проходимся по каждому отделению и вставляем его в базу данных
        for department in data:
            sale_point_name = department['salePointName']
            address = department['address']
            status = department['status']
            open_hours = json.dumps(department['openHours'])
            rko = department['rko']
            open_hours_individual = json.dumps(
                department['openHoursIndividual'])
            office_type = department['officeType']
            sale_point_format = department['salePointFormat']
            suo_availability = department['suoAvailability']
            has_ramp = department['hasRamp']
            latitude = department['latitude']
            longitude = department['longitude']
            metro_station = department['metroStation']
            distance = department['distance']
            kep = department['kep']
            my_branch = department['myBranch']

            # Вставляем данные в базу
            await cursor.execute(
                '''
                INSERT INTO departments (
                    sale_point_name, address, status, open_hours, rko, 
                    open_hours_individual, office_type, sale_point_format, 
                    suo_availability, has_ramp, latitude, longitude, 
                    metro_station, distance, kep, my_branch
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    sale_point_name, address, status, open_hours, rko,
                    open_hours_individual, office_type, sale_point_format,
                    suo_availability, has_ramp, latitude, longitude,
                    metro_station, distance, kep, my_branch
                )
            )

        # Коммитим изменения
        await db.commit()
# asyncio.run(create_departments_table("db.db"))
asyncio.run(load_json_to_db("offices.txt", "db.db"))
