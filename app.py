from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Criar pasta de downloads se não existir
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@app.route('/', methods=['GET', 'POST'])
def index():
    video_filename = None
    username = None
    caption = None
    error_message = None

    if request.method == 'POST':
        url = request.form['url']

        try:
            if 'tiktok.com' in url:
                # Configuração do yt-dlp para baixar vídeos do TikTok
                ydl_opts = {
                    'outtmpl': 'downloads/%(id)s.%(ext)s',  # Nome do arquivo com o ID do vídeo
                    'format': 'best'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)  # Extrai dados e baixa o vídeo
                    video_filename = f"downloads/{info_dict.get('id', 'unknown')}.{info_dict.get('ext', 'mp4')}"
                    username = info_dict.get('uploader', 'Usuário Desconhecido')
                    caption = info_dict.get('description', 'Sem Legenda Disponível')

            else:
                error_message = "Por favor, insira um link válido do TikTok."

        except Exception as e:
            error_message = str(e)

        return render_template('index.html', 
                               video_filename=video_filename,
                               username=username,
                               caption=caption,
                               error=error_message)

    return render_template('index.html', video_filename=None, username=None, caption=None, error=None)

@app.route('/download')
def download():
    filename = request.args.get('file')  # Obtém o nome do arquivo via query string
    if filename and os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return "Arquivo não encontrado!", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render usa essa variável de ambiente
    app.run(host='0.0.0.0', port=port, debug=True)
