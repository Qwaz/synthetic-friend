from datetime import datetime
import json
import os

from tacotron_ksss.tacotron.synthesizer import Synthesizer

import requests
from flask import Flask, render_template, send_from_directory, request, abort, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credential.json"

if not os.path.exists(app.config['GENERATED_FOLDER']):
    os.makedirs(app.config['GENERATED_FOLDER'])

synthesizer = Synthesizer()
synthesizer.load('tacotron_ksss/ksss-pretrained', 1, None)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/speech_recognition', methods=['POST'])
def speech_recognition():
    from speech import recognize
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
        'text': random.choice(response_candidates[:3])['message'],
        'video': '/static/{}'.format(random.choice([
            "IU2_talk1.mp4",
            "IU2_talk2.mp4",
        ])),
    })


@app.route('/api/speech_generation', methods=['POST'])
def speech_generation():
    if 'text' not in request.form:
        abort(400)

    audio_name = '{}.wav'.format(datetime.now().strftime("%Y-%m-%d_%H%M%S_%f"))
    audio_path = os.path.join(app.config['GENERATED_FOLDER'], audio_name)

    synthesizer.synthesize(
            texts=[request.form['text']],
            paths=[audio_path],
            speaker_ids=[0],
            attention_trim=False,
            isKorean=True)[0]

    return jsonify({
        'audio': '/generated/{}'.format(audio_name[:-4] + '.0.wav'),
    })


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/generated/<path:path>')
def send_generated(path):
    return send_from_directory('generated', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
