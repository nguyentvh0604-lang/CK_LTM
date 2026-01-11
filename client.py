import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

HOST = '127.0.0.1'
PORT = 5050

class ChatClient:
    def __init__(self, host, port):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, port))
        except ConnectionRefusedError:
            print("Lỗi: Bạn chưa bật Server hoặc sai địa chỉ IP/Port!")
            return

        self.root = tk.Tk()
        self.root.title("Ứng dụng Chat")

        self.nickname = simpledialog.askstring("Nickname", "Chọn tên hiển thị:", parent=self.root)
        if not self.nickname: self.nickname = "Anonymous"

        self.text_area = scrolledtext.ScrolledText(self.root)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.input_area = tk.Entry(self.root)
        self.input_area.pack(padx=20, pady=5)
        self.input_area.bind("<Return>", lambda e: self.write())

        threading.Thread(target=self.receive, daemon=True).start()
        self.root.mainloop()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    self.text_area.config(state='normal')
                    self.text_area.insert(tk.END, message + "\n")
                    self.text_area.config(state='disabled')
            except:
                self.client.close()
                break

    def write(self):
        msg = f"{self.nickname}: {self.input_area.get()}"
        self.client.send(msg.encode('utf-8'))
        self.input_area.delete(0, tk.END)

if __name__ == "__main__":
    ChatClient(HOST, PORT)