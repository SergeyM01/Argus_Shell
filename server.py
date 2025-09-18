import socket
from colorama import Fore, Style

HOST = ''
PORT = 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind((HOST, PORT))
    soc.listen(5)
    print(Fore.GREEN + "\n[+] Сервер ожидает входящего подключения..." + Style.RESET_ALL)

    client_connection, client_addr = soc.accept()
    print(Fore.GREEN + f"[+] Установлено соединение с: {client_addr}" + Style.RESET_ALL)

    with client_connection:
        while True:
            command = input('\nВведите команду:\n')

            if command.lower() == 'exit':
                print(Fore.BLUE + '[*] Завершение соединения' + Style.RESET_ALL)
                break

            if not command:
                continue

            try:
                output = command.encode('utf-8')
                client_connection.sendall(output)
                data_from_client = client_connection.recv(4096).decode('utf-8')
                print(Fore.GREEN + data_from_client + Style.RESET_ALL)
            except Exception as err:
                print(Fore.RED + f"[!] Ошибка: {err}" + Style.RESET_ALL)
                exit()