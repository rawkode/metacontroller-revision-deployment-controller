from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/watch')
def watch():
    json = request.get_json(silent=True)
    response = jsonify(message=json)
    response.status_code = 500
    return json
