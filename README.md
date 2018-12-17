# Synthetic Friend
Friendly chat bot service with emotional response and natural speech synthesis.

## How to setup

1. Install [FFmpeg](https://www.ffmpeg.org/) and add it to PATH.

2. Setup and download your Google Speech Credential [here](https://cloud.google.com/speech-to-text/).

3. Run the following commands to run the server.
```
git clone --recursive https://github.com/Qwaz/synthetic-friend.git
cd synthetic-friend
(put your GCP credential in the directory as `credential.json`)
pip install -r tacotron_ksss/requirements.txt
python app.py
```

4. Open `localhost:8888` in your browser.

## Troubleshooting

The code is only tested with Google Chrome browser. 

If you are not using the localhost,
you should run the server under HTTPS due to the browser content policy.
(HTTP contents cannot access microphone)
