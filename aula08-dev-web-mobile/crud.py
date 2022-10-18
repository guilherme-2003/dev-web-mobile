import sqlite3
from flask import g,Flask, request, render_template

BANCO_DE_DADOS = './banco.db'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def carregar_banco():
    #Verifica se o banco já foi carregado
    banco = getattr(g, '_database', None)

    if banco is None:
        g._database = sqlite3.connect(BANCO_DE_DADOS)
        banco = g._database
    return banco

def iniciar_tabela():
    banco = carregar_banco()
    script_criacao = open('schema.sql').read()
    banco.executescript(script_criacao)

@app.route('/')
def index():
    banco = carregar_banco()
    iniciar_tabela()
    return '<h1>TABELA CRIADA<h1>'

@app.route('/add', methods = ['POST',])
def salvar_info():
    banco = carregar_banco()
    cur = banco.cursor()
    nome = request.form["nome"]
    idade = request.form["idade"]
    endereco = request.form["endereco"]
    cur.execute('INSERT INTO Funcionario (nome, idade, endereco) VALUES (?, ?, ?)', (nome, idade, endereco))
    banco.commit()
    banco.close()
    return f"Nome: {nome}, Idade: {idade}, Endereço: {endereco}"

@app.route('/create') # Abrir o form
def formulario_insercao():
    return render_template('formulario_insere.html')
 
@app.route('/ver', methods = ['POST',])
def ver_info():
    banco = carregar_banco()
    cur = banco.cursor()
    id = request.form["id"]
    resultados = cur.execute("SELECT id, nome FROM Funcionario WHERE id = ? ", (id)).fetchall()
    banco.commit()
    banco.close()
    return render_template("resultados_busca.html", resultados=resultados)

@app.route('/read')
def formulario_busca():
    return render_template('formulario_busca.html')