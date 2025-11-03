from flask import Flask, request, send_file, render_template, redirect, url_for
import os

app = Flask(__name__)

# Pasta onde os arquivos serão salvos

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Rota para a página inicial (interface web)
@app.route('/')
def index():
    # Lista os arquivos na pasta uploads
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

# Endpoint para upload de arquivos (via formulário web)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return redirect(url_for('index'))
    files = request.files.getlist('files')  # Suporte a múltiplos arquivos
    for file in files:
        if file.filename == '':
            continue
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
    return redirect(url_for('index'))

# Endpoint para download de arquivos
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'Arquivo não encontrado', 404

if __name__ == '__main__':
    # Executa o servidor em localhost:5000
    app.run(host='0.0.0.0', port=5000, debug=True)
