import socket
import os
import time
import threading
import sys
from pymongo import MongoClient
import subprocess

c = MongoClient('34.82.142.213:27017')                          # mongo db connection of instance server ex: c = MongoClient('[instance_ip]:[mongodb port]')
db = c.cameras                                                  # database connection

tport = []
HOST = ''

data = db.camera.find()                                         # retrieve data from db

for d in data:
    if not d["sport"] == "":                                    # check if server port is empty or not
        PORT = int(d["sport"])
    else:
        PORT = ""

if not PORT == "":
    is_client_alive = True
    r_time = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))                                        # bind to the defined port to communicate with client
    s.listen(0)
else:
    pass

'''
kill port if port forwarding failed

params:
        l:             list of port to be killed

returns:
        nothing
'''
def killPort(l):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = sock.connect_ex(('localhost', int(l)))                # check if port is alive before kill

    if res == 0:
        print("kill port " + l)
        cmd = "sudo kill -9 $(sudo lsof -t -i:" + l + ")"       # command to be executed for killing port
        os.popen(cmd)

'''
check time to kill all port

params:
        nothing
returns:
        nothing
'''
def timer():
    global is_client_alive
    global r_time
    global s

    while not is_client_alive:
        if time.time()-r_time > 10.0:                       # wait for client, if not responds within 10 seconds then boom
            s.close()
            data = db.camera.find()
            for d in data:
                tport.append(d["tport"])                    # append all the port to be killed
            for l in tport:
                t = threading.Thread(target=killPort, args=(l, ))
                t.start()
                time.sleep(1)
            break


def server():
    global is_client_alive
    global r_time
    global s
    u_port = []
    prev_port = []
    conn, addr = s.accept()
    while True:
        u_data = db.camera.find()
        for u in u_data:
            u_port.append(u["tport"])                   # append all updated data

        if prev_port:
            for i in prev_port:
                if not i in u_port:                     # if any mismatch occur between previous port data and updated port data then all the deleted port will be killed
                     t = threading.Thread(target=killPort, args=(i, ))
                     t.start()

        prev_port = u_port[:]
        u_port.clear()

        is_client_alive = False

        r_time = time.time()
        t = threading.Thread(target=timer)
        t.start()
        
        time.sleep(2)

        data = conn.recv(1024)
        if not data:
            break

        is_client_alive = True
        conn.sendall(data)

if __name__ == "__main__":
    if not PORT == "":
        server()
