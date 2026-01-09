import socket

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server đang chạy...")

client, address = server.accept()
print(f"Kết nối từ {address}")

message = client.recv(1024).decode()
print("Client gửi:", message)

client.close()
