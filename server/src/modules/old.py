async def load_json_to_db(json_file, db_name):
    # Открываем соединение с базой данных
    async with aiosqlite.connect(db_name) as db:
        # Создаем курсор
        cursor = await db.cursor()

        # Создаем таблицу atms, если она не существует
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS atms (
                id INTEGER PRIMARY KEY,
                address TEXT,
                latitude REAL,
                longitude REAL,
                all_day INTEGER
            )
        ''')

        # Создаем таблицу services, если она не существует
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY,
                atm_id INTEGER,
                service_name TEXT,
                capability TEXT,
                activity TEXT,
                FOREIGN KEY (atm_id) REFERENCES atms (id)
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

            # Вставляем данные в таблицу atms и получаем id новой записи
            await cursor.execute('''
                INSERT INTO atms (address, latitude, longitude, all_day)
                VALUES (?, ?, ?, ?)
            ''', (address, latitude, longitude, all_day))
            atm_id = cursor.lastrowid

            # Итерируемся по службам и вставляем их в таблицу services
            for service_name, service_info in atm["services"].items():
                capability = service_info["serviceCapability"]
                activity = service_info["serviceActivity"]

                await cursor.execute('''
                    INSERT INTO services (atm_id, service_name,
                                      capability, activity)
                    VALUES (?, ?, ?, ?)
                ''', (atm_id, service_name, capability, activity))

        # Коммитим изменения
        await db.commit()
