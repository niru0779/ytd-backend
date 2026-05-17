@app.route('/download')
def download():

    url = request.args.get('url')

    if not url:
        return jsonify({
            "error": "Missing URL"
        })

    try:

        ydl_opts = {

            'quiet': True,
            'format': 'best',

            'cookiefile': 'cookies.txt',

            'extractor_args': {
                'youtube': {
                    'player_client': ['android']
                }
            },

            'http_headers': {
                'User-Agent': 'Mozilla/5.0'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            download_url = info.get('url')

            if not download_url:

                formats = info.get('formats', [])

                for f in reversed(formats):

                    if f.get('url'):
                        download_url = f['url']
                        break

            return jsonify({

                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "download": download_url,
                "id": info.get('id')
            })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
