from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.carteira import router as carteira_router
from routes.leilao import router as leilao_router
from routes.obras import router as obra_router
from routes.websocket import router as websocket_leilao
from contextlib import asynccontextmanager
from threading import Event, Thread
from starlette.concurrency import run_in_threadpool
from services.worker_leiloes import iniciar_worker



@asynccontextmanager
async def lifespan(app: FastAPI):
    parar = Event()
    worker = Thread(target=iniciar_worker, args=(parar,), daemon=True)
    worker.start()

    try:
        yield
    finally:
        parar.set()
        await run_in_threadpool(worker.join)
app=FastAPI(title="Casa de Leilões da Verzel",
description="Irei realizar o teste para Verzel e para isso farei "
                                                  "um leilão online",version="1.0.0",lifespan=lifespan)

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