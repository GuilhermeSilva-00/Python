import tkinter as tk
from tkinter import messagebox
import pyodbc

# --- CONFIGURAÇÕES DO BANCO ---
server = '192.168.0.8'
database = 'Cadastro'
username = 'GVAS_00'
password = 'Gvas@0728'


def testar_conexao():
    try:
        conexao = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        conexao.close()
        messagebox.showinfo("Conexão Bem-Sucedida", "✅ Conexão com o banco estabelecida com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"❌ Não foi possível conectar ao banco:\n\n{e}")


# --- FUNÇÃO PARA SALVAR OS DADOS ---
def salvar_dados():
    nome = entry_nome.get()
    idade = entry_idade.get()
    cidade = entry_cidade.get()

    if not nome or not idade or not cidade:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    try:
        conexao = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        cursor = conexao.cursor()
        sql = "INSERT INTO Pessoas (Nome, Idade, Cidade) VALUES (?, ?, ?)"
        cursor.execute(sql, (nome, int(idade), cidade))
        conexao.commit()
        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_cidade.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar dados:\n{e}")

# --- JANELA TKINTER ---
janela = tk.Tk()
janela.title("Cadastro de Pessoa")
janela.geometry("300x220")

# --- CAMPOS ---
tk.Label(janela, text="Nome:").pack(pady=5)
entry_nome = tk.Entry(janela, width=30)
entry_nome.pack()

tk.Label(janela, text="Idade:").pack(pady=5)
entry_idade = tk.Entry(janela, width=30)
entry_idade.pack()

tk.Label(janela, text="Cidade:").pack(pady=5)
entry_cidade = tk.Entry(janela, width=30)
entry_cidade.pack()

# --- BOTÃO SALVAR ---
tk.Button(janela, text="Salvar", command=salvar_dados).pack(pady=15)

janela.mainloop()
