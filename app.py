import os
from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        format = request.form['format']
        unique_filename = str(uuid.uuid4())
        output_path = f"{DOWNLOAD_FOLDER}/{unique_filename}.%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            file_without_ext = os.path.splitext(filename)[0]
            final_file = f"{file_without_ext}.{format}"

        return send_file(final_file, as_attachment=True)

    return render_template('index.html')

if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)  # Get the port from Render environment
    app.run(host='0.0.0.0', port=port, threaded=True)  # Added threaded=True
