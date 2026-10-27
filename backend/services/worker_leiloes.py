from services.liquidacao import processar_leiloes_vencidos
from database import SessionLocal
import time


def executar_encerramentos():
    with SessionLocal () as db:
        processar_leiloes_vencidos(db)


def iniciar_worker():
    while True:
        try:
            executar_encerramentos()
        except Exception as erro:
            print(f"Erro ao processar leiloes: {erro}")

        time.sleep(30)


if __name__ == '__main__':
    iniciar_worker()