from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.carteira import router as carteira_router
from routes.leilao import router as leilao_router
from routes.obras import router as obra_router
from routes.websocket import router as websocket_leilao


app=FastAPI(title="Casa de Leilões da Verzel",
description="Irei realizar o teste para Verzel e para isso farei "
                                                  "um leilão online",version="1.0.0")

app.include_router(auth_router)
app.include_router(carteira_router)
app.include_router(leilao_router)
app.include_router(obra_router)
app.include_router(websocket_leilao)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://projeto-leilao-five.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message":"Ola mundo"}