from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

rates = {
    "USD": 1.0,
    "EUR": 0.92,
    "RUB": 88.5,
    "GBP": 0.79,
    "JPY": 149.5,
    "CNY": 7.22
}

class ConvertRequest(BaseModel):
    from_cur: str
    to_cur: str
    amount: float

def get_rates():

    try:
        r = requests.get(
            "https://open.er-api.com/v6/latest/USD",
            timeout=3
        )

        data = r.json()

        if data["result"] == "success":

            return {
                k: data["rates"][k]
                for k in rates.keys()
            }

    except:
        pass

    return rates

@app.get("/currencies")
def currencies():
    return list(rates.keys())

@app.post("/convert")
def convert(data: ConvertRequest):

    current = get_rates()

    if data.from_cur not in current:
        raise HTTPException(
            status_code=400,
            detail="Неизвестная валюта"
        )

    if data.to_cur not in current:
        raise HTTPException(
            status_code=400,
            detail="Неизвестная валюта"
        )

    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Сумма должна быть больше 0"
        )

    rate = (
        current[data.to_cur]
        / current[data.from_cur]
    )

    result = data.amount * rate

    return {
        "from": data.from_cur,
        "to": data.to_cur,
        "amount": data.amount,
        "result": round(result, 2)
    }

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
