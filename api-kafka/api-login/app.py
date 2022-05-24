from ensurepip import bootstrap
from flask import Flask, jsonify, request
from kafka import KafkaProducer
import json
import time

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    usuario = {
        'user': request.json['user'],
        'pass': request.json['pass']
    }

    topic = {
        'user': request.json['user'],
        'time': round(time.time(),0)
    }

    pub = KafkaProducer(bootstrap_servers = 'kafka:9092', api_version=(0,11,5))
    pub.send("mytopic", value=json.dumps(topic).encode('utf-8'))
    return jsonify(usuario)

if __name__ == '__main__':
    app.run(debug=True, port=3000)