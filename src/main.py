from modules import utils
from fastapi import FastAPI
import json
from fastapi.middleware.cors import CORSMiddleware
from modules.database import Database
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Подключаем статические файлы (в данном случае, папку с html, css и js)
app.add_middleware(
    CORSMiddleware,
    # Можешь указать конкретные адреса, разрешенные для доступа
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/index", StaticFiles(directory="static", html=True), name="static")


async def get_atm_data():
    db = Database()
    data = await db.get_atms_data()
    return json.loads(data)


async def get_office_data():
    db = Database()
    data = await db.get_departments_data()
    return {"office": data}


async def get_filter_atm(latitude, longitude, radius, required):
    """функция для получения банкомата в радиусе пользователя
    с учетом его запроса

    Args:
        latitude (_type_): ширина
        longitude (_type_): долгота
        radius (_type_): радиус поиска
        required (_type_): запрос

    Returns:
        _type_: банкоматы, которые могут подойти
    """
    attempt = 0
    all_atm = await get_atm_data()
    while True:
        data = await utils.find_atms_in_radius(latitude, longitude, all_atm,
                                               radius)
        if required is not None and required != "":
            required_services = required.split(',')
            data = await utils.filter_atms(data, required_services)
        if len(data) < 1 and attempt < 5:
            radius = float(radius) + 0.3
            attempt += 1
            continue
        data = await utils.add_distance_to_json(data, (latitude, longitude))
        # первые 5 по меньшему пути
        sorted_atms = sorted(data, key=lambda x: x["travel_time_walk"])
        top_5_atms = sorted_atms[:5]
        data = await utils.add_workload(top_5_atms)
        sorted_atms = sorted(data, key=utils.sort_atms)
        all_data = utils.time_wait(sorted_atms)
        return data


async def get_filter_office(latitude, longitude, radius):
    """функция для получения офиса в радиусе пользователя
    с учетом его запроса

    Args:
        latitude (_type_): ширина
        longitude (_type_): долгота
        radius (_type_): радиус поиска

    Returns:
        _type_: банкоматы, которые могут подойти
    """
    attempt = 0
    all_office = await get_office_data()
    while True:
        data = await utils.find_office_in_radius(latitude, longitude,
                                                 all_office,
                                                 radius)
        if len(data) < 1 and attempt < 5:
            radius = float(radius) + 0.3
            attempt += 1
            continue
        return data


@app.get("/atm")
async def get_atm():
    """функция для получения всех atm из бд

    Returns:
        json: все офисы втб
    """
    return await get_atm_data()


@app.get("/atm_filter")
async def atm_filter(latitude, longitude, radius, required=None):
    """функция для получения банкомата в радиусе пользователя
    с учетом его запроса

    Args:
        latitude (_type_): ширина
        longitude (_type_): долгота
        radius (_type_): радиус поиска
        required (_type_): запрос

    Returns:
        _type_: банкоматы, которые могут подойти
    """
    data = await get_filter_atm(latitude, longitude, radius, required)
    return {"atms": data}


@app.get("/office_filter")
async def office_filter(latitude, longitude, radius):
    """функция для получения офиса в радиусе пользователя
    с учетом его запроса

    Args:
        latitude (_type_): ширина
        longitude (_type_): долгота
        radius (_type_): радиус поиска

    Returns:
        _type_: банкоматы, которые могут подойти
    """
    data = await get_filter_office(latitude, longitude, radius)
    return {"office": data}


@app.get("/office")
async def get_office():
    """функция для получения всех офисов из бд

    Returns:
        json: все офисы втб
    """
    return await get_office_data()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
