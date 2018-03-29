from flask import Flask, request, jsonify
import logging
import pprint
import sys
app = Flask(__name__)


@app.route('/watch', methods=['POST'])
def watch():
    json = request.get_json()

    response = jsonify(message=json)
    response.status_code = 500

    pprint.pprint(json)
    sys.stdout.flush()

    return response
