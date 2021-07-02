import socket
import os
import subprocess
#
#
# def file_exist(file_name):
#     try:
#         file = open(file_name, 'r')
#         status = "HTTP/1.1 200 OK\n"
#         status_code = 200
#         file.close()
#     except IOError:
#         status = "HTTP/1.1 404 NOT FOUND\n"
#         status_code = 404
#
#     return status, status_code
#
#
# def generate_header(file_name):
#     header = "----------------------------------------------"
#     header += "file name :"
#     header += file_name
#     header += '\n'
#     header += "status :"
#     status, status_code = file_exist(file_name)
#     header += status
#     header += '\n'
#     return header, status_code
#
#
# def read_file_content(file_name):
#     file1 = open(file_name, 'r')
#     lines = file1.readlines()
#
#     count = 0
#     file_content = ""
#     for line in lines:
#         count += 1
#         file_content += line.strip()
#         file_content += '\n'
#
#     return file_content


def command_detail(command):
    command_splited = command.split()
    if command_splited[0] == 'cd':
        print(command_splited[1])
        new_path = command_splited[1]
        if new_path == '..':
            pwd_path = new_path.split('/')
            lenght = len(pwd_path)
            new_path = ''
            for i in range(lenght):
                new_path += pwd_path[i]
            print("new new E")
            print(new_path)
        os.chdir(new_path)
        return subprocess.run('ls -a', capture_output=True, shell=True)
    command_result = subprocess.run([command], capture_output=True, shell=True)
    return command_result


def header_generator(return_code, command):
    header = "----------------------------------------------"
    header += "command :"
    header += command
    header += '\n'
    header += "status :"
    status = "HTTP/1.1 200 EXECUTED \n" if return_code == 0 else "HTTP/1.1 404 CAN NOT EXECUTE\n"
    header += status
    return header


def execute_data(file_content):
    result_command = command_detail(file_content)
    header = header_generator(result_command.returncode, file_content)
    result= result_command.stdout.decode()
    if result == '':
        result = "This command doesn't have textual result "
    if result_command.returncode != 0 :
        result = "your intended comment DOESN'T EXIST !   "
    return result, header

s = socket.socket()
print("Socket successfully created")
port = 12345
s.bind(('', port))
print("socket binded to %s" % port)
s.listen(5)
print("socket is listening")

while True:
    Allow = True
    first_access = False
    con, addr = s.accept()
    while Allow:

        data = con.recv(1024)
        data_content = data.decode('utf-8')
        if first_access:
            if data == b'alitabasi':
                showed_text = "user with "
                showed_text += str(addr)
                showed_text += " can access to server --->  "
                print(showed_text)

                content = "Allow"
                new_data = bytes(content, 'utf-8')
                first_access=False
                con.send(new_data)

                continue

            else:
                showed_text = "user with "
                showed_text += str(addr)
                showed_text += " can NOT access to server !!!!"
                print(showed_text)

                first_access = False
                Allow=False
                content = "Deny"
                new_data = bytes(content, 'utf-8')
                con.send(new_data)
                continue

        if not first_access:
            if data == b'connection request':
                print("user with ")
                print(addr)
                print(" want to connect ?? ")
                content = "insert password"
                new_data = bytes(content, 'utf-8')
                first_access = True
                con.send(new_data)
                continue

        if data_content == '':
            break
        print(data_content)
        result , header =execute_data(data_content)
        # header, status_code = generate_header(data_content)
        # file_name = data_content
        # if status_code == 404:
        #     file_name = "not_found.html"
        # content = read_file_content(file_name)
        print(header)

        new_data = bytes(result, 'utf-8')
        con.send(new_data)

    con.close()
