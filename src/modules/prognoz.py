import random
import sqlite3

# Соединяемся с базой данных
conn = sqlite3.connect('db.db')
c = conn.cursor()

# Создаем таблицу, если она не существует
c.execute('''CREATE TABLE IF NOT EXISTS atm_load
             (id INTEGER PRIMARY KEY,
              atm_id INTEGER,
              day_of_week INTEGER,
              minute INTEGER,
              load INTEGER)''')

# Функция для получения часа из минуты


def getHour(minute):
    return minute // 60


id = 0
DEFAULT = 20  # в спокойное время работы банкомата
HIGH = 60  # во время повышенного спроса банкомата

# Генерация и вставка данных
for atm_id in range(1, 2400+1):
    for day_of_week in range(1, 8):
        for five_minutes in range(288):
            minutes = []
            for minute in range(5):
                busy = 0
                val = random.randint(1, 101)
                all_minutes = five_minutes * 5 + minute
                if (getHour(all_minutes) >= 12 and getHour(all_minutes) <= 14) or (getHour(all_minutes) >= 17 and getHour(all_minutes) <= 20):
                    busy = 0 if (val > HIGH) else 1
                else:
                    busy = 0 if (val > DEFAULT) else 1
                minutes.append(busy)
            middle_val = sum(minutes) / len(minutes)
            c.execute("INSERT INTO atm_load (atm_id, day_of_week, minute, load) VALUES (?, ?, ?, ?)",
                      (atm_id, day_of_week, five_minutes, int(middle_val * 100)))
            id += 1

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
