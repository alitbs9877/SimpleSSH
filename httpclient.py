import socket
import getpass
from socket import timeout


request = b"home.html"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 12345))
try:
    # first attempt
    request = "connection request"
    print(request)
    request = bytes(request, 'utf-8')
    s.send(request)
    data = (str(s.recv(4096), 'utf-8'))
    print(data)
    # enter password
    request = getpass.getpass()
    request = bytes(request, 'utf-8')
    s.send(request)
    data = (str(s.recv(4096), 'utf-8'))
    if data == 'Allow':
        while True:

            print("Allowed to connect to server")
            request = bytes(input(), 'utf-8')

            if request == b'exit':
                break;

            s.send(request)
            data = (str(s.recv(4096), 'utf-8'))
            print(data)

    else:
        print("Deny")
    # catch_html_file(data)
    s.close()
except ConnectionResetError:
    print("==> ConnectionResetError")
    pass
except timeout:
    print("==> Timeout")
    pass
