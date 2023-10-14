from pprint import pprint
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


async def get_office_data():
    db = Database()
    data = await db.get_atms_data()
    return json.loads(data)


@app.get("/office")
async def get_office():
    return await get_office_data()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
