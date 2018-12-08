from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/speech_recognition', methods=['POST'])
def speech_recognition():
    return 'I do not understand speech yet'


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run()
