import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import json

HOST = '127.0.0.1'
PORT = 5050

class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat App")
        self.nickname = ""
        self.waiting_nick = False

        self.text_area = scrolledtext.ScrolledText(self.root, state='disabled')
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input_area = tk.Entry(self.root)
        self.input_area.pack(fill=tk.X, padx=10)
        self.input_area.bind("<Return>", lambda e: self.send_message())

        self.send_btn = tk.Button(self.root, text="Gửi", command=self.send_message)
        self.send_btn.pack(pady=5)

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))
        except:
            messagebox.showerror("Lỗi", "Không kết nối được server")
            self.root.destroy()
            return

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        threading.Thread(target=self.receive, daemon=True).start()
        self.root.mainloop()

    def receive(self):
        buffer = ""
        try:
            while True:
                data = self.client.recv(4096).decode('utf-8')
                if not data:
                    break

                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)

                    if line == "NICK_REQUEST":
                        self.root.after(0, self.ask_nickname)
                    else:
                        msg = json.loads(line)
                        self.root.after(0, self.display, msg)
        except:
            self.root.after(0, self.on_close)

    def ask_nickname(self):
        if self.waiting_nick:
            return
        self.waiting_nick = True

        name = simpledialog.askstring(
            "Nickname", "Nhập nickname:", parent=self.root
        )

        if not name:
            self.on_close()
            return

        self.nickname = name
        self.client.send((name + "\n").encode('utf-8'))
        self.waiting_nick = False

    def send_message(self):
        text = self.input_area.get()
        if not text or not self.nickname:
            return

        if text.strip() == "/exit":
            self.on_close()
            return

        if text.startswith("/msg "):
            try:
                _, receiver, content = text.split(" ", 2)
                msg = {
                    "type": "private",
                    "sender": self.nickname,
                    "receiver": receiver,
                    "content": content
                }
            except:
                self.display({
                    "type": "system",
                    "content": "Sai cú pháp: /msg ten noi_dung"
                })
                return
        else:
            msg = {
                "type": "group",
                "sender": self.nickname,
                "content": text
            }

        self.client.send((json.dumps(msg) + "\n").encode('utf-8'))
        self.input_area.delete(0, tk.END)

    def display(self, msg):
        self.text_area.config(state='normal')

        if msg["type"] == "system":
            self.text_area.insert(tk.END, f"** {msg['content']} **\n", "sys")
        elif msg["type"] == "private":
            self.text_area.insert(tk.END, f"[PM] {msg['sender']}: {msg['content']}\n", "pm")
        else:
            self.text_area.insert(tk.END, f"{msg['sender']}: {msg['content']}\n")

        self.text_area.tag_config("sys", foreground="red")
        self.text_area.tag_config("pm", foreground="blue")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

    def on_close(self):
        try:
            self.client.close()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    ChatClient()
