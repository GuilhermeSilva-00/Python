import pyodbc
from fastapi import FastAPI
from pydantic import BaseModel

# 🔌 Conexão com o banco
def get_connection():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DELLMG;"  # Altere conforme seu servidor
        "Database=SQL_BD;"  # Nome do seu banco
        "Trusted_Connection=yes;"
    )
    return conn

# 📦 Modelo de dados
class Cliente(BaseModel):
    nome: str
    email: str
    telefone: str

# 🚀 Instância da API
app = FastAPI()

# 🌐 Rota raiz
@app.get("/")
def root():
    return {"mensagem": "API de Cadastro de Clientes está rodando!"}

# 📥 Rota de cadastro
@app.post("/cadastrar")
def cadastrar_cliente(cliente: Cliente):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clientes (nome, email, telefone)
            VALUES (?, ?, ?)
        """, cliente.nome, cliente.email, cliente.telefone)
        conn.commit()
        return {"mensagem": "Cliente cadastrado com sucesso!"}
    except Exception as e:
        return {"erro": str(e)}
    finally:
        cursor.close()
        conn.close()
