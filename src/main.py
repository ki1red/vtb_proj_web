from modules import utils
from fastapi import FastAPI
import json
from fastapi.middleware.cors import CORSMiddleware
from modules.database import Database

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


async def get_atm_data():
    db = Database()
    data = await db.get_atms_data()
    return json.loads(data)


async def get_filter_atm(latitude, longitude, radius):
    all_atm = await get_atm_data()
    data = utils.find_atms_in_radius(latitude, longitude, all_atm, radius)
    return data


@app.get("/atm")
async def get_atm():
    """функция для получения всех atm из бд

    Returns:
        json: все офисы втб
    """
    return await get_atm_data()


@app.get("/atm_filter")
async def atm_filter(latitude, longitude, radius):
    data = await get_filter_atm(latitude, longitude, radius)
    return {"atms": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
