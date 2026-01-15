import socket
import threading
import json
import sys

HOST = '127.0.0.1'
PORT = 5050
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            
            if message == "NICK_REQUEST":
                pass
            elif message == "NICK_REJECTED":
                print("[Hệ thống] Tên này đã tồn tại. Vui lòng chọn tên khác!")
            elif message == "NICK_ACCEPTED":
                print("[Hệ thống] Kết nối thành công!")
            else:
                data = json.loads(message)
                msg_type = data.get("type")
                content = data.get("content")
                
                if msg_type == "system":
                    print(f"\n*** {content} ***")
                elif msg_type == "private":
                    sender = data.get("sender", "Ẩn danh")
                    print(f"\n[PM từ {sender}]: {content}")
                else:
                    sender = data.get("sender", "Người dùng")
                    print(f"\n[{sender}]: {content}")
                
                print("> ", end="", flush=True) 
        except:
            print("Đã mất kết nối với Server.")
            client.close()
            break

def write(nickname):
    while True:
        try:
            content = input("> ")
            
            if content.startswith("/w "):
                parts = content.split(" ", 2)
                if len(parts) >= 3:
                    receiver = parts[1]
                    msg_body = parts[2]
                    message_obj = {
                        "type": "private",
                        "sender": nickname,
                        "receiver": receiver,
                        "content": msg_body
                    }
                else:
                    print("Lệnh sai! Cú pháp: /w [tên] [nội dung]")
                    continue
            else:
                message_obj = {
                    "type": "group",
                    "sender": nickname,
                    "content": content
                }
            
            client.send(json.dumps(message_obj).encode(FORMAT))
        except:
            break

def start_client():
    nickname = ""
    while True:
        signal = client.recv(1024).decode(FORMAT)
        if signal == "NICK_REQUEST":
            nickname = input("Nhập biệt danh của bạn: ")
            client.send(nickname.encode(FORMAT))
        elif signal == "NICK_REJECTED":
            print("Lỗi: Tên này đã có người dùng!")
        elif signal == "NICK_ACCEPTED":
            print(f"Chào mừng {nickname}! Bạn có thể bắt đầu chat.")
            break

    receive_thread = threading.Thread(target=receive)
    receive_thread.daemon = True 
    receive_thread.start()

    write(nickname)

if __name__ == "__main__":
    start_client()