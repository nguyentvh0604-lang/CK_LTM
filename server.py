import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5050
FORMAT = 'utf-8'

clients_dict = {}

def broadcast(message_obj):
    json_data = json.dumps(message_obj).encode(FORMAT)
    for nickname in clients_dict:
        clients_dict[nickname].send(json_data)

def handle_client(client, nickname):
    while True:
        try:
            data = client.recv(1024).decode(FORMAT)
            if not data: break
            
            msg_obj = json.loads(data)
            msg_type = msg_obj.get("type")

            if msg_type == "group":
                broadcast(msg_obj)
            
            elif msg_type == "private":
                receiver = msg_obj.get("receiver")
                if receiver in clients_dict:
                    clients_dict[receiver].send(json.dumps(msg_obj).encode(FORMAT))
                    client.send(json.dumps(msg_obj).encode(FORMAT))
                else:
                    error_msg = {"type": "system", "content": f"User {receiver} offline."}
                    client.send(json.dumps(error_msg).encode(FORMAT))
        except:
            break

    del clients_dict[nickname]
    client.close()
    broadcast({"type": "system", "content": f"{nickname} left."})

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server: {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        client.send("NICK_REQUEST".encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        
        clients_dict[nickname] = client
        broadcast({"type": "system", "content": f"{nickname} joined."})
        
        thread = threading.Thread(target=handle_client, args=(client, nickname))
        thread.start()

if __name__ == "__main__":
    start_server()