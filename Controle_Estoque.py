import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

''' Teste'''

def conectar_banco():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DELLMG;'
        'DATABASE=SQL_BD;'
        'Trusted_Connection=yes;'
    )
    return conn

def consultar_produto(codigo_barras):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
    produto = cursor.fetchone()
    cursor.close()
    conn.close()
    return produto

def registrar_movimentacao(produto_id, tipo, quantidade, usuario):
    conn = conectar_banco()
    cursor = conn.cursor()

    if tipo == 'entrada':
        cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, produto_id))
    elif tipo == 'saida':
        cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))

    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, usuario, data_movimentacao)
        VALUES (?, ?, ?, ?, ?)
    """, (produto_id, tipo, quantidade, usuario, datetime.now()))

    # Verificar se a quantidade do produto chegou a 5
    cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
    quantidade_atual = cursor.fetchone()[0]
    if quantidade_atual == 5:
        enviar_email("destinatario@dominio.com", "Alerta de Estoque Baixo", f"A quantidade do produto com ID {produto_id} chegou a 5 unidades.")

    conn.commit()
    cursor.close()
    conn.close()

def enviar_email(destinatario, assunto, corpo):
    remetente = "contato.gvas@gmail.com"
    senha = "Gvas@0728"  # Caso tenha 2FA, utilize a senha do aplicativo

    # Configurar o servidor SMTP do Gmail
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()  # Usar TLS
    servidor.login(remetente, senha)  # Logar no Gmail

    # Criar o conteúdo do e-mail
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto
    mensagem.attach(MIMEText(corpo, "plain"))

    # Enviar o e-mail
    servidor.sendmail(remetente, destinatario, mensagem.as_string())
    servidor.quit()

    print("E-mail enviado com sucesso!")

def listar_produtos():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo_barras, nome, quantidade FROM produtos")
    for produto in cursor.fetchall():
        codigo, nome, quantidade = produto
        tree.insert("", tk.END, values=(codigo.strip(), nome.strip(), quantidade))
    cursor.close()
    conn.close()

def buscar_produto_interface(event=None):
    codigo_barras = input_codigo_barras.get()
    produto = consultar_produto(codigo_barras)
    input_nome_produto.config(state='normal')
    input_nome_produto.delete(0, tk.END)
    if produto:
        input_nome_produto.insert(0, produto[1])
    else:
        input_nome_produto.insert(0, "Produto não encontrado")
    input_nome_produto.config(state='readonly')

def registrar_movimentacao_interface():
    codigo_barras = input_codigo_barras.get()
    tipo = tipo_movimentacao.get()
    try:
        quantidade = int(input_quantidade.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade inválida!")
        return

    usuario = input_usuario.get()
    produto = consultar_produto(codigo_barras)
    if produto:
        registrar_movimentacao(produto[0], tipo, quantidade, usuario)
        messagebox.showinfo("Sucesso", f"{tipo.capitalize()} registrada!")
        listar_produtos()
        buscar_produto_interface()
        input_quantidade.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Produto não encontrado!")

# GUI
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("700x500")
root.resizable(False, False)

frame_form = tk.LabelFrame(root, text="Movimentação de Estoque", padx=10, pady=10)
frame_form.pack(padx=10, pady=10, fill="x")

tk.Label(frame_form, text="Código de Barras:").grid(row=0, column=0, sticky="w")
input_codigo_barras = tk.Entry(frame_form, width=30)
input_codigo_barras.grid(row=0, column=1, pady=5, padx=5)
input_codigo_barras.bind("<FocusOut>", buscar_produto_interface)

tk.Label(frame_form, text="Nome do Produto:").grid(row=1, column=0, sticky="w")
input_nome_produto = tk.Entry(frame_form, width=30, state="readonly")
input_nome_produto.grid(row=1, column=1, pady=5, padx=5)

tk.Label(frame_form, text="Quantidade:").grid(row=2, column=0, sticky="w")
input_quantidade = tk.Entry(frame_form, width=30)
input_quantidade.grid(row=2, column=1, pady=5, padx=5)

tk.Label(frame_form, text="Usuário:").grid(row=3, column=0, sticky="w")
input_usuario = tk.Entry(frame_form, width=30)
input_usuario.grid(row=3, column=1, pady=5, padx=5)

tipo_movimentacao = tk.StringVar(value="entrada")
frame_tipo = tk.Frame(frame_form)
frame_tipo.grid(row=4, column=1, pady=5, sticky="w")
tk.Radiobutton(frame_tipo, text="Entrada", variable=tipo_movimentacao, value="entrada").pack(side="left")
tk.Radiobutton(frame_tipo, text="Saída", variable=tipo_movimentacao, value="saida").pack(side="left")

tk.Button(frame_form, text="Registrar Movimentação", width=25, command=registrar_movimentacao_interface).grid(row=5, column=0, columnspan=2, pady=10)

# Tabela
frame_tabela = tk.LabelFrame(root, text="Produtos em Estoque", padx=10, pady=10)
frame_tabela.pack(padx=10, pady=10, fill="both", expand=True)

tree = ttk.Treeview(frame_tabela, columns=("Código", "Nome", "Quantidade"), show='headings')
tree.heading("Código", text="Código de Barras")
tree.heading("Nome", text="Nome do Produto")
tree.heading("Quantidade", text="Quantidade")
tree.pack(fill="both", expand=True)

listar_produtos()

root.mainloop()
