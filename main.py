from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Подключаем статические файлы (в данном случае, папку с html)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
