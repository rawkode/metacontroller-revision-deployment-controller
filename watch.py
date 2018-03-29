from flask import Flask
app = Flask(__name__)

@app.route('/watch')
def watch():
    return 'watch'
