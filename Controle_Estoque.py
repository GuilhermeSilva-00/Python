import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Conectar ao banco
def conectar_banco():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DELLMG;'
        'DATABASE=SQL_BD;'
        'Trusted_Connection=yes;'
    )
    return conn

# Consultar produto pelo código de barras
def consultar_produto(codigo_barras):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
    produto = cursor.fetchone()
    cursor.close()
    conn.close()
    return produto

# Registrar movimentação de estoque
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

# Listar todos os produtos
def listar_produtos():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo_barras, nome, quantidade FROM produtos")
    for codigo, nome, quantidade in cursor.fetchall():
        nome = nome.strip()
        codigo = codigo.strip()
        if quantidade <= 10:
            quantidade_str = f"⚠️ {quantidade}"
            tree.insert("", tk.END, values=(codigo, nome, quantidade_str), tags=('alerta',))
        else:
            tree.insert("", tk.END, values=(codigo, nome, quantidade), tags=('ok',))
    cursor.close()
    conn.close()

# Função para verificar a senha antes de registrar a movimentação
def verificar_senha():
    senha = input_senha.get().strip()  # Pegando a senha digitada
    if senha == "010101":  # Senha de exemplo, você pode mudar para a sua
        registrar_movimentacao_interface()
    else:
        messagebox.showerror("Erro", "Senha incorreta!")

# Registrar movimentação via interface
def registrar_movimentacao_interface():
    codigo_barras = input_codigo_barras.get().strip()
    tipo = tipo_movimentacao.get()
    try:
        quantidade = int(input_quantidade.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade inválida!")
        return

    usuario = input_usuario.get().strip()
    produto = consultar_produto(codigo_barras)
    if produto:
        registrar_movimentacao(produto[0], tipo, quantidade, usuario)
        messagebox.showinfo("Sucesso", f"{tipo.capitalize()} registrada!")
        listar_produtos()
        buscar_produto_interface()
        input_quantidade.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Produto não encontrado!")

# Buscar produto na interface
def buscar_produto_interface(event=None):
    codigo_barras = input_codigo_barras.get().strip()
    produto = consultar_produto(codigo_barras)
    input_nome_produto.config(state='normal')
    input_nome_produto.delete(0, tk.END)
    
    if produto:
        nome_produto = produto[2].strip()  # Índice 2 é o campo 'nome'
        input_nome_produto.insert(0, nome_produto)
    else:
        input_nome_produto.insert(0, "Produto não encontrado")

    input_nome_produto.config(state='readonly')

# GUI
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("800x600")
root.configure(bg='#f0f0f0')

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
style.configure("Treeview", rowheight=25, font=('Arial', 10))

# Formulário de movimentação
frame_form = tk.LabelFrame(root, text="Movimentação de Estoque", padx=20, pady=20, bg='#f0f0f0')
frame_form.pack(padx=20, pady=15, fill="x")

# Código de Barras
tk.Label(frame_form, text="Código de Barras:", bg='#f0f0f0').grid(row=0, column=0, sticky="w", pady=5)
input_codigo_barras = tk.Entry(frame_form, width=40)
input_codigo_barras.grid(row=0, column=1, padx=10, pady=5)
input_codigo_barras.bind("<KeyRelease>", buscar_produto_interface)


# Nome do Produto
tk.Label(frame_form, text="Nome do Produto:", bg='#f0f0f0').grid(row=1, column=0, sticky="w", pady=5)
input_nome_produto = tk.Entry(frame_form, width=40, state="readonly")
input_nome_produto.grid(row=1, column=1, padx=10, pady=5)

# Quantidade
tk.Label(frame_form, text="Quantidade:", bg='#f0f0f0').grid(row=2, column=0, sticky="w", pady=5)
input_quantidade = tk.Entry(frame_form, width=40)
input_quantidade.grid(row=2, column=1, padx=10, pady=5)

# Usuário
tk.Label(frame_form, text="Usuário:", bg='#f0f0f0').grid(row=3, column=0, sticky="w", pady=5)
input_usuario = tk.Entry(frame_form, width=40)
input_usuario.grid(row=3, column=1, padx=10, pady=5)

# Senha
tk.Label(frame_form, text="Senha:", bg='#f0f0f0').grid(row=4, column=0, sticky="w", pady=5)
input_senha = tk.Entry(frame_form, width=40, show="*")
input_senha.grid(row=4, column=1, padx=10, pady=5)

# Tipo de movimentação
tk.Label(frame_form, text="Tipo de Movimentação:", bg='#f0f0f0').grid(row=5, column=0, sticky="w", pady=5)
tipo_movimentacao = tk.StringVar(value="entrada")
frame_tipo = tk.Frame(frame_form, bg='#f0f0f0')
frame_tipo.grid(row=5, column=1, sticky="w", pady=5)
tk.Radiobutton(frame_tipo, text="Entrada", variable=tipo_movimentacao, value="entrada", bg='#f0f0f0').pack(side="left", padx=5)
tk.Radiobutton(frame_tipo, text="Saída", variable=tipo_movimentacao, value="saida", bg='#f0f0f0').pack(side="left", padx=5)

# Botão registrar
tk.Button(frame_form, text="Registrar Movimentação", width=30, bg="#007acc", fg="white", command=verificar_senha).grid(row=6, column=0, columnspan=2, pady=15)

# Tabela de produtos
frame_tabela = tk.LabelFrame(root, text="Produtos em Estoque", padx=20, pady=10, bg='#f0f0f0')
frame_tabela.pack(padx=20, pady=10, fill="both", expand=True)

tree = ttk.Treeview(frame_tabela, columns=("Código", "Nome", "Quantidade"), show='headings')
tree.heading("Código", text="Código de Barras")
tree.heading("Nome", text="Nome do Produto")
tree.heading("Quantidade", text="Quantidade")
tree.pack(fill="both", expand=True)

# Cores
tree.tag_configure('alerta', background='#ffdddd')  # vermelho claro
tree.tag_configure('ok', background='#ddffdd')      # verde claro

# Carrega produtos ao abrir
listar_produtos()

root.mainloop()
