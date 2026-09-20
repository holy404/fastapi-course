from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from starlette import status

#инициализация FastAPI приложения
app = FastAPI()

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
            detail = f"Wallet '{wallet_name}' not found."
        )
    #Возвращаем баланс конкретного кошелька
    return {'Wallet': wallet_name, 'Balance': BALANCE[wallet_name]}

@app.post("/wallets/{name}")
def create_wallet(name: str, initial_balance: float = 0):
    # Проверяем, не существует ли уже такой кошелек
    if name in BALANCE:
        raise HTTPException(
            status_code=400,
            detail = f"Wallet '{name}' already exists."
        )
    # Создаем новый кошелек с начальным балансом
    BALANCE[name] = initial_balance
    # Возвращаем информацию о созданном кошельке
    return {
        "message": f"Wallet '{name}' created.",
        "wallet": name,
        "balance": BALANCE[name]
    }