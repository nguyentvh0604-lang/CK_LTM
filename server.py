import socket
import threading

HOST = '127.0.0.1'
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
nicknames = []

def broadcast(message):
    """Gửi tin nhắn đến tất cả client đang kết nối"""
    for client in clients:
        client.send(message)

def handle_client(client):
    """Xử lý luồng dữ liệu riêng cho từng client"""
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} đã rời khỏi phòng chat!'.encode(FORMAT))
            nicknames.remove(nickname)
            break

def receive():
    """Chấp nhận kết nối mới liên tục"""
    server.listen()
    print(f"[SERVER] Đang chạy trên {HOST}...")
    while True:
        client, address = server.accept()
        print(f"Kết nối mới từ {str(address)}")

        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname của client là {nickname}")
        broadcast(f"{nickname} đã tham gia vào đoạn chat!".encode(FORMAT))
        client.send('Đã kết nối đến server!'.encode(FORMAT))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()