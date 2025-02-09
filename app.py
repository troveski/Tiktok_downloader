from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    username = None
    caption = None
    video_filename = None
    error_message = None

    if request.method == 'POST':
        url = request.form['url']
        print(f"\nProcessing URL: {url}")

        try:
            ydl_opts = {
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'format': 'best',
                'verbose': True,  # Enable verbose output for debugging
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("Starting download...")
                info_dict = ydl.extract_info(url, download=True)
                print(f"Download info: {info_dict}")
                
                video_filename = f"downloads/{info_dict['id']}.{info_dict['ext']}"
                username = info_dict.get('uploader', 'Unknown User')
                caption = info_dict.get('description', 'No Caption Available')
                print(f"Download successful: {video_filename}")

        except Exception as e:
            error_message = str(e)
            print(f"Error occurred: {error_message}")

        return render_template('index.html',
                            video_filename=video_filename,
                            username=username,
                            caption=caption,
                            error=error_message)

    return render_template('index.html', video_filename=None, username=None, caption=None, error=None)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)