import socket
import threading

HOST = "0.0.0.0"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}   # {socket: username}

print("Chat Server đang chạy...")

def broadcast(message, sender=None):
    for client in list(clients):
        try:
            if client != sender:
                client.send(message.encode("utf-8"))
        except:
            remove_client(client)

def remove_client(client):
    if client in clients:
        username = clients[client]
        del clients[client]
        broadcast(f"⚠ {username} đã rời phòng chat")
        client.close()
        print(f"{username} disconnected")

def handle_client(client):
    try:
        client.send("USERNAME".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")
        clients[client] = username

        print(f"{username} đã kết nối")
        broadcast(f"👋 {username} đã tham gia phòng chat")

        while True:
            msg = client.recv(1024).decode("utf-8")

            if msg.lower() == "/quit":
                remove_client(client)
                break

            full_msg = f"{username}: {msg}"
            print(full_msg)
            broadcast(full_msg, client)

    except:
        remove_client(client)

def receive():
    while True:
        client, addr = server.accept()
        print(f"Kết nối từ {addr}")
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
