from pymongo import MongoClient
import os
import time
import threading

c = MongoClient('34.82.142.213:27017')                  # mongo db connection of instance server ex: c = MongoClient('[instance_ip]:[mongodb port]')
db = c.cameras                                          # database connection

active_port = []

'''
ssh tunnel to the remote port

params:
        ip:             camera local ip
        cam_port:       camera local port
        tunnel_port:    remote port
        server_ip:      tunnel server ip
returns:
        nothing
'''
def sshTunnel(ip, cam_port, tunnel_port, server_ip):
    cmd = "autossh -o StrictHostKeyChecking=no -N -R 0.0.0.0:" + tunnel_port + ":" + ip + ":" + cam_port + " " + "sshtunnel@" + server_ip       # command to be executed for tunneling
    os.system(cmd)
    active_port.remove(tunnel_port)                     # remove tunnel port from active_port if autossh failed/closed or connection can't be established


if __name__ == "__main__":
    while True:
        data = db.camera.find()                         # retrieve data from db
        
        for d in data:
            if d["tport"] == "":                        # check if tunnel port is empty or not
                pass
            else:
                if not d["tport"] in active_port:
                    active_port.append(d["tport"])      # append tunnel port that will be tunneled
                    th = threading.Thread(target=sshTunnel, args=(d["lip"], d["lport"], d["tport"], d["sip"],), daemon=True)
                    th.start()
                    time.sleep(1)
        
        time.sleep(1)