<meta name='viewport' content='width=device-width, initial-scale=1'/><script>from flask import Flask, request, jsonify
import requests
import re

myapp = Flask("SnapDownloader")

def SnapSave(video_url):
    snapsave_url = "https://snapsave.app/action.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    data = {"url": video_url}
    
    try:
        response = requests.post(snapsave_url, data=data, headers=headers)
        raw_html = response.text
        match = re.search(r'href="(http.*?)"', raw_html)
        
        if match:
            return match.group(1)
        else:
            return None
    except:
        return None

@myapp.route('/get-video', methods=['GET'])
def get_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    download_url = SnapSave(url)
    if download_url:
        return jsonify({"download_url": download_url})
    else:
        return jsonify({"error": "Failed to fetch video"}), 500

if __name__ == '__main__':
    myapp.run(debug=True, host="0.0.0.0", port=5000)</script>