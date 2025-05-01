import tkinter as tk
import requests

def enviar():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()

    dados = {
        "nome": nome,
        "email": email,
        "telefone": telefone
    }

    try:
        resposta = requests.post("http://127.0.0.1:8000/cadastrar", json=dados)
        if resposta.status_code == 200:
            lbl_resultado.config(text="✅ Cliente cadastrado com sucesso!")
        else:
            lbl_resultado.config(text=f"❌ Erro: {resposta.text}")
    except Exception as e:
        lbl_resultado.config(text=f"❌ Erro de conexão: {e}")

# Interface gráfica
app = tk.Tk()
app.title("Painel de Cadastro")

tk.Label(app, text="Nome").grid(row=0, column=0)
tk.Label(app, text="Email").grid(row=1, column=0)
tk.Label(app, text="Telefone").grid(row=2, column=0)

entry_nome = tk.Entry(app)
entry_email = tk.Entry(app)
entry_telefone = tk.Entry(app)

entry_nome.grid(row=0, column=1)
entry_email.grid(row=1, column=1)
entry_telefone.grid(row=2, column=1)

tk.Button(app, text="Cadastrar", command=enviar).grid(row=3, column=0, columnspan=2, pady=10)
lbl_resultado = tk.Label(app, text="")
lbl_resultado.grid(row=4, column=0, columnspan=2)

app.mainloop()
