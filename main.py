from fastapi import FastAPI
from fastapi.responses import Response

#инициализация FastAPI приложения
app = FastAPI()

#Делаем Health check endpoint
@app.get("/health")
def health_check():
    return Response(status_code=200)