from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if 'tiktok.com' in url:
            try:
                ydl_opts = {
                    'outtmpl': 'downloads/%(id)s.%(ext)s',  # Uses a short unique ID instead of the title
                    'format': 'best',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    video_title = ydl.prepare_filename(info_dict)
                    return send_file(video_title, as_attachment=True)
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return "Invalid URL. Please enter a valid TikTok URL."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001)
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
