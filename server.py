import socket
from colorama import Fore, Style

HOST = ''
PORT = 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind((HOST, PORT))
    soc.listen(5)
    print(Fore.GREEN + "[+] Сервер ожидает входящего подключения..." + Style.RESET_ALL)

    client_connection, client_addr = soc.accept()
    print(Fore.GREEN + f"[+] Установлено соединение с: {client_addr}" + Style.RESET_ALL)

    with client_connection:
        while True:
            command = input('Введите команду:\n')
            if command == 'exit':
                break

            output = command.encode('utf-8')
            client_connection.sendall(output)
            data_from_client = client_connection.recv(4096)
            print(data_from_client.decode('utf-8'))