from threading import Event
from services.liquidacao import processar_leiloes_vencidos
from database import SessionLocal


def executar_encerramentos():
    with SessionLocal() as db:
        processar_leiloes_vencidos(db)


def iniciar_worker(parar: Event):
    while not parar.is_set():
        try:
            executar_encerramentos()
        except Exception as erro:
            print(f"Erro ao processar leiloes: {erro}")

        parar.wait(30)


if __name__ == "__main__":
    iniciar_worker(Event())