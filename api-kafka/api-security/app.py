from flask import Flask, jsonify
from kafka import KafkaConsumer
import json
import threading
import re

app = Flask(__name__)

bloqueados = {
    "users-blocked": []
}

class BackgroundTasks(threading.Thread):
        con = KafkaConsumer(bootstrap_servers='kafka:9092', auto_offset_reset = 'earliest',  value_deserializer= lambda x: x.decode('utf-8'), consumer_timeout_ms = 3000)
        con.subscribe('mytopic')
        user = []
        while(True):
            for message in con:
                print(message.value)
                s = re.sub('{|"|\'|,|:|}', '', message.value)
                s = s.split()
                var = True
                for i in range(len(user)):
                    if s[1] in user[i]:
                        user[i].append(s[3])
                        if len(user[i])==6:
                            dif = float(user[i][5])-float(user[i][1])
                            if dif > 60:
                                user[i].pop(1)
                            else:
                                bloqueados['users-blocked'].append(user[i][0])
                        elif len(user[i])>6:
                            user[i].pop(1)
                        var = False
                if var:
                    user.append([])
                    user[len(user)-1].append(s[1])
            with open('data.json', 'w') as file:
                json.dump(bloqueados, file, indent=4)

@app.route('/blocked')
def blocked():
    datos = {
        "users-blocked": []
    }
    try:
        with open('data.json', 'r') as file:
            datos = json.load(file)
    except FileNotFoundError:
        return jsonify(datos)
    return jsonify(datos)


if __name__ == '__main__':
    t = BackgroundTasks()
    t.start()
    app.run(debug=True, port=5000)
