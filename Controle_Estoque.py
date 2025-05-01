import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Conexão com o banco de dados
def conectar_banco():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DELLMG;'
        'DATABASE=SQL_BD;'
        'Trusted_Connection=yes;'
    )
    return conn

# Consulta produto pelo código de barras
def consultar_produto(codigo_barras):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
    produto = cursor.fetchone()
    cursor.close()
    conn.close()
    return produto

# Registrar entrada ou saída de produto
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

    conn.commit()
    cursor.close()
    conn.close()

# Atualiza a tabela de produtos no GUI
def listar_produtos():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo_barras, nome, quantidade FROM produtos")
    for produto in cursor.fetchall():
        codigo, nome, quantidade = produto
        codigo = codigo.strip()
        nome = nome.strip()

        if quantidade <= 10:
            quantidade_str = f"⚠️ {quantidade}"
            tree.insert("", tk.END, values=(codigo, nome, quantidade_str), tags=('alerta',))
        else:
            tree.insert("", tk.END, values=(codigo, nome, quantidade), tags=('ok',))
    cursor.close()
    conn.close()

# Buscar produto na interface
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

# Interface de movimentação
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

# Tabela de produtos
frame_tabela = tk.LabelFrame(root, text="Produtos em Estoque", padx=10, pady=10)
frame_tabela.pack(padx=10, pady=10, fill="both", expand=True)

tree = ttk.Treeview(frame_tabela, columns=("Código", "Nome", "Quantidade"), show='headings')
tree.heading("Código", text="Código de Barras")
tree.heading("Nome", text="Nome do Produto")
tree.heading("Quantidade", text="Quantidade")
tree.pack(fill="both", expand=True)

# Configurações de cor para as tags
tree.tag_configure('alerta', background='#ffdddd')  # Vermelho claro para alerta
tree.tag_configure('ok', background='#ddffdd')      # Verde claro para estoque normal

listar_produtos()
root.mainloop()
