# Synthetic Friend
Friendly chat bot service with emotional response and natural speech synthesis.

## How to setup
```
git clone --recursive https://github.com/Qwaz/synthetic-friend.git
cd synthetic-friend
pip install -r tacotron_ksss/requirements.txt
python app.py
```

The default port is 8888. If you are not using localhost,
you should run the server under HTTPS due to browser content policy.
(HTTP contents cannot access microphone)

The code is tested with Google Chrome browser.
