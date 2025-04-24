import tkinter as tk
import requests

# Função para enviar os dados para a API
def enviar_dados():
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
            lbl_resultado.config(text=f"❌ Erro: {resposta.json()}")
    except Exception as e:
        lbl_resultado.config(text=f"❌ Erro de conexão: {e}")

# Criar janela
janela = tk.Tk()
janela.title("Cadastro de Cliente")

# Labels
tk.Label(janela, text="Nome:").grid(row=0, column=0)
tk.Label(janela, text="Email:").grid(row=1, column=0)
tk.Label(janela, text="Telefone:").grid(row=2, column=0)

# Entradas de texto
entry_nome = tk.Entry(janela)
entry_email = tk.Entry(janela)
entry_telefone = tk.Entry(janela)

entry_nome.grid(row=0, column=1)
entry_email.grid(row=1, column=1)
entry_telefone.grid(row=2, column=1)

# Botão para cadastrar
btn_enviar = tk.Button(janela, text="Cadastrar", command=enviar_dados)
btn_enviar.grid(row=3, column=0, columnspan=2, pady=10)

# Label para mostrar o resultado
lbl_resultado = tk.Label(janela, text="")
lbl_resultado.grid(row=4, column=0, columnspan=2)

# Rodar a interface
janela.mainloop()
