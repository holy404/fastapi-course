from fastapi import FastAPI
from fastapi.responses import Response
from starlette import status

#инициализация FastAPI приложения
app = FastAPI()

#Делаем Health check endpoint
@app.get("/health")
def health_check():
    return Response(status_code=200) #возвращаем статус 200

#Словарь для хранения данных кошельков
#Ключ - название кошелька, значение - баланс

BALANCE = {}

@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    #Если имя кошелька не указано - считаем общий баланс
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())}
    #Проверяем, существует ли запрашиваемый кошелек
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail = f"Wallet {wallet_name} not found."
        )
    #Возвращаем баланс конкретного кошелька
    return {'Wallet': wallet_name, 'Balance': BALANCE[wallet_name]}

@app.post("wallets/{name}")
def receive_money(name: str, amount: int):
    #Если кошелька с таким именем нет, то создаем с балансом 0
    if name not in BALANCE:
        BALANCE[name] = 0
    #Добавляем сумму к балансу кошелька
    BALANCE[name] += amount
    #Возвращаем информацию об операции
    return {
        "message" : f"Added {amount} to wallet {name}",
        "wallet" : {name},
        "new_balance" : BALANCE[name]
    }