import json
import os

from tacotron_ksss

import requests
from flask import Flask, render_template, send_from_directory, request, abort, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.\\uploads'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".\\credential.json"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/speech_recognition', methods=['POST'])
def speech_recognition():
    from speech import recognize
    from datetime import datetime
    if 'file' not in request.files:
        abort(400)
    file = request.files['file']
    if file.filename == '':
        abort(400)
    prefix = os.path.join(app.config['UPLOAD_FOLDER'], datetime.now().strftime("%Y-%m-%d_%H%M%S_%f"))
    webm_filename = prefix + '.webm'
    ogg_filename = prefix + '.ogg'
    file.save(webm_filename)
    os.system('ffmpeg -i {} -vn -acodec copy {}'.format(webm_filename, ogg_filename))
    return recognize(ogg_filename)


@app.route('/api/response_generation', methods=['POST'])
def response_generation():
    import random
    if 'text' not in request.form:
        abort(400)
    response = requests.get('https://pingpong.us/api/reaction.php', params={
        'custom': 'basic',
        'query': request.form['text'],
    })
    response_candidates = json.loads(response.text)
    return jsonify({
        'text': random.choice(response_candidates)['message'],
        'video': '/generated/obama{}.mp4'.format(random.randint(1, 3)),
    })


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/generated/<path:path>')
def send_generated(path):
    return send_from_directory('generated', path)


if __name__ == '__main__':
    app.run()
