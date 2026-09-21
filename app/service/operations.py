from fastapi import HTTPException

from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository


def add_income(operation: OperationRequest):
    #Проверяем существует ли кошелек
    if not wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail = f"Wallet '{operation.wallet_name}' not found."
        )
    #Добавляем доход к балансу кошелька
    new_balance = wallets_repository.add_income(operation.wallet_name, operation.amount)
    #Возвращаем информацию об операции
    return {
        "message": "Income added.",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance
    }

def add_expense(operation: OperationRequest):
    #Проверяем, существует ли кошелек
    if not wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail = f"Wallet '{operation.wallet_name}' not found."
        )
    #Проверяем корректна ли сумма
    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"Amount must be positive."
        )
    #Проверяем достаточно ли средств на кошельке
    balance = wallets_repository.get_wallet_balance_by_name(operation.wallet_name)
    if balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail = f"Insufficient funds in the account. Available: {balance}."
        )
    #Снимаем деньги с кошелька
    new_balance = wallets_repository.add_expense(operation.wallet_name, operation.amount)
    #Возвращаем информацию об операции
    return {
        "message": "Expense added.",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance
    }