from sqlalchemy import text
from database import engine

with engine.connect() as connection:
    resultado = connection.execute(text("SELECT 1"))
    print("Conexao funcionando",resultado.scalar())