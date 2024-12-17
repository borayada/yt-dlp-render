from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_audio():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({"error": "Missing URL"}), 400

    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    # Define the output file path
    output_path = os.path.join(output_dir, "%(title)s.%(ext)s")
    command = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", output_path,
        video_url
    ]

    try:
        subprocess.run(command, check=True)
        # Find the downloaded file
        downloaded_files = os.listdir(output_dir)
        if downloaded_files:
            audio_file = downloaded_files[0]
            file_url = f"{request.host_url}{output_dir}/{audio_file}"
            return jsonify({"file_url": file_url})
        return jsonify({"error": "File not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
