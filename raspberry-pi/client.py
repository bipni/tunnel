import socket
from pymongo import MongoClient

c = MongoClient('34.82.142.213:27017')						# mongo db connection of instance server ex: c = MongoClient('[instance_ip]:[mongodb port]')
db = c.cameras												# database connection

data = db.camera.find()										# retrieve data from db

for d in data:
	if not d["sip"] == "":									# check if tunnel server ip is empty or not
		HOST = d["sip"]
		PORT = int(d["sport"])
		break
	else:
		HOST = ""
		PORT = ""

if not HOST == "":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))									# connect to tunnel server

	while True:												# simultaneously send/receive dummy data to/from the tunnel server
		s.sendall(b'ok')
		data = s.recv(1024)
		print('Received', repr(data))