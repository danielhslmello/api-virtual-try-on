from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import jwt
import time

# 🔑 Credenciais da API Kling AI
ACCESS_KEY_ID = "131207b53f9847369e104fe06cd4333a"
SECRET_KEY = "7d4e530031d740f78ddc3d8b42d86a92"
API_BASE_URL = "https://api.klingai.com"

app = FastAPI()

# 🚀 Permitir CORS para comunicação entre frontend e backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🛠️ Gerar Token JWT
def generate_token():
    payload = {
        "iss": ACCESS_KEY_ID,
        "exp": int(time.time()) + 1800,
        "nbf": int(time.time()) - 5,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 🔥 Criar Tarefa na API Kling AI
@app.post("/try-on")
async def create_task(data: dict):
    try:
        token = generate_token()
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(
            f"{API_BASE_URL}/v1/images/kolors-virtual-try-on",
            json=data,
            headers=headers,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔄 Monitorar Tarefa
@app.get("/try-on/{task_id}")
async def check_task(task_id: str):
    try:
        token = generate_token()
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(
            f"{API_BASE_URL}/v1/images/kolors-virtual-try-on/{task_id}",
            headers=headers,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
