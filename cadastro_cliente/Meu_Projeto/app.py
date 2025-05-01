from flask import Flask, request
import pyodbc
import webbrowser
import threading

app = Flask(__name__)

# --- CONFIGURAÇÕES DO BANCO ---
server = '192.168.0.8'
database = 'Cadastro'
username = 'GVAS_00'
password = 'Gvas@0728'

# Conexão com SQL Server
conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)
cursor = conn.cursor()

# Criação da tabela (apenas na primeira execução)
cursor.execute("""
IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='Clientes' AND xtype='U'
)
CREATE TABLE Clientes (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Nome NVARCHAR(100),
    Idade INT,
    Cidade NVARCHAR(100)
)
""")
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        cidade = request.form['cidade']
        try:
            cursor.execute("INSERT INTO Clientes (Nome, Idade, Cidade) VALUES (?, ?, ?)", nome, idade, cidade)
            conn.commit()
            return '<h3>Dados salvos com sucesso!</h3><a href="/">Voltar</a>'
        except Exception as e:
            return f'<h3>Erro ao salvar: {e}</h3><a href="/">Voltar</a>'

    return '''
        <h2>Cadastro de Cliente</h2>
        <form method="post">
            Nome: <input type="text" name="nome"><br>
            Idade: <input type="number" name="idade"><br>
            Cidade: <input type="text" name="cidade"><br>
            <input type="submit" value="Salvar">
        </form>
    '''

# Abre o navegador automaticamente
def abrir_navegador():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1.0, abrir_navegador).start()
    app.run(debug=True)
