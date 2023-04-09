import os

from flask import Flask, jsonify, send_file, send_from_directory, url_for, request
from flask import render_template

app = Flask(__name__)


# Inserir caminho para a pasta de música aqui:
MUSIC_PATH = "C:/Users/lucas/Music"

# Alias para a pasta "Music"
MUSIC_FOLDER = os.path.abspath(MUSIC_PATH)

@app.route('/')
def index():
    return render_template('index.html')

# Rota para listar categorias
@app.route('/categorias')
def listar_categorias():
    categorias = {}
    for raiz, diretorios, arquivos in os.walk(MUSIC_FOLDER):
        for diretorio in diretorios:
            caminho_completo = os.path.join(raiz, diretorio)
            arquivos_categoria = []
            for nome_arquivo in os.listdir(caminho_completo):
                caminho_arquivo = os.path.join(caminho_completo, nome_arquivo)
                if os.path.isfile(caminho_arquivo):
                    arquivos_categoria.append(nome_arquivo)
            categorias[diretorio] = arquivos_categoria
    return jsonify(categorias)

# Rota para listar arquivos
@app.route('/arquivos')
def listar_arquivos():
    categoria = request.args.get('categoria')
    categoria_caminho = os.path.join(MUSIC_FOLDER, categoria)
    arquivos = []
    for raiz, _, arquivos_nome in os.walk(categoria_caminho):
        for arquivo in arquivos_nome:
            caminho_completo = os.path.join(raiz, arquivo)
            tamanho = os.path.getsize(caminho_completo)
            arquivos.append({
                'nome': arquivo,
                'tamanho': tamanho,
                'url': url_for('ler_arquivo', nome_arquivo=arquivo, categoria=categoria)
            })
    return jsonify(arquivos)

# Rota para ler um arquivo
@app.route('/ler/<categoria>/<path:nome_arquivo>')
def ler_arquivo(categoria, nome_arquivo):
    caminho_completo = os.path.join(MUSIC_FOLDER, categoria, nome_arquivo)
    return send_file(caminho_completo)

if __name__ == '__main__':
    app.run(debug=True)