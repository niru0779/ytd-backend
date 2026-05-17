from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download')
def download():

    url = request.args.get('url')

    if not url:
        return jsonify({"error": "Missing URL"})

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=False)

        formats = info.get('formats', [])

        download_url = None

        for f in formats:
            if f.get('url'):
                download_url = f['url']
                break

        return jsonify({
            "title": info.get('title'),
            "thumbnail": info.get('thumbnail'),
            "download": download_url
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
