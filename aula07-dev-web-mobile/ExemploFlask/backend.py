from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return '<h1>Título<h1><p>Essa é minha HomePage<p>'

@app.route('/profile/<nome>')
def perfil(nome):
    return render_template('index.html', nome=nome)