from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    username = None
    caption = None
    video_filename = None

    if request.method == 'POST':
        url = request.form['url']
        if 'tiktok.com' in url or 'instagram.com/reel' in url:  # ✅ Detects both TikTok & Instagram
            try:
                ydl_opts = {
                    'outtmpl': 'downloads/%(id)s.%(ext)s',  # Keeps filename unique (by video ID)
                    'format': 'best',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)  # Extract metadata
                    video_filename = f"downloads/{info_dict.get('id', 'unknown')}.{info_dict.get('ext', 'mp4')}"
                    username = info_dict.get('uploader', 'Unknown User')  # Extract username
                    caption = info_dict.get('description', 'No Caption Available')  # Extract caption

                    # Render the page with the username, caption, and filename
                    return render_template('index.html', 
                                           video_filename=video_filename,
                                           username=username,
                                           caption=caption)
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return "Invalid URL. Please enter a valid TikTok or Instagram Reel URL."

    return render_template('index.html', video_filename=None, username=None, caption=None)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(host='0.0.0.0', port=5001, debug=True)  # ✅ Running on port 5001
