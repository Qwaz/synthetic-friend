import os

from flask import Flask, render_template, send_from_directory, request, abort

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


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run()
