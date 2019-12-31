from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient
import json

client = MongoClient('localhost:27017')
db = client.cameras

app = Flask(__name__)
CORS(app)

@app.route('/add_camera', methods=['POST'])
def add_camera():
    if request.method == 'POST':
        data = request.get_json(force=True)
        rtsp = data['rtsp']
        lip = data['lip']
        lport = data['lport']
        tport = data['tport']
        sip = data['sip']
        sport = data['sport']

        if sip == "" or tport == "":
            p = rtsp.replace("[ip]", lip, 1)
            q = p.replace("[port]", lport, 1)
            rtsp = q
        else:
            p = rtsp.replace("[ip]", sip, 1)
            q = p.replace("[port]", tport, 1)
            rtsp = q
        
        db.camera.insert_one(
            {
                "rtsp": rtsp,
                "lip": lip,
                "lport": lport,
                "tport": tport,
                "sip": sip,
                "sport": sport
            }
        )

        return "success"

@app.route('/show_camera', methods=['GET'])
def show_camera():
    l = []
    data = db.camera.find()
    for d in data:            
        l.append(d["rtsp"])
    return json.dumps(l)

@app.route('/delete_camera', methods=['POST'])
def delete_camera():
    if request.method == 'POST':
        data = request.get_json(force=True)
        rtsp_link = data['rtsp']
        
        db.camera.delete_many({"rtsp":rtsp_link})

        return "success"

if __name__ == '__main__':
    app.run(host="10.138.0.32", debug=True)
