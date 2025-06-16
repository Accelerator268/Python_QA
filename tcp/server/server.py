import socket
import os


def tcp_server() -> None:
    #Определение названия хоста и порта, на котором сервер будет принимать сигналы
    host: str = 'localhost'
    port: int = 20000

    #Устанавливаем, в какой папке будут происходить последующие процессы
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #Создание сервера
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(1)
        print(f"TCP Server listening on {host}:{port}")

        #Запуск сервера
        while True:
            conn, address = server.accept()
            address = ':'.join([str(i) for i in address])
            print(f"Request from {address}")

            #Сервер проверяет полученную информацию
            try:
                #Сервер получает имя файла
                filename = conn.recv(1024).decode()
                if not filename:
                    continue

                #Сервер выводит название запрошенного файла, если полученная информация является названием файла
                print(f"Client requested file: {filename}\nSending...")

                #Если запрошенный файл существует, то сервер его отправляет. Если нет, то сообщает об этом
                if os.path.exists(filename):
                    filesize: int = os.path.getsize(filename)
                    conn.send(str(filesize).encode())

                    with open(filename, 'rb') as file:
                        while True:
                            data: bytes = file.read(4096)
                            if not data:
                                break
                            conn.send(data)
                    print(f"Finished sending to {address}")
                else:
                    conn.send(b"-1")
                    print(f"File not found\nFailed sending to {address}")

            #Если возникла ошибка, то выводит ее
            except Exception as exception:
                print(f"Error: {exception}")

            #Сервер закрывает соединение с клиентом, но сам продолжает работу
            finally:
                conn.close()

#Основное тело программы
if __name__ == "__main__":
    tcp_server()
