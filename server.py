import asyncio
import json

HOST = '127.0.0.1'
PORT = 5050

clients = {}

async def send(writer, obj):
    writer.write((json.dumps(obj) + "\n").encode('utf-8'))
    await writer.drain()

async def broadcast(obj):
    for w in clients.values():
        await send(w, obj)

async def handle_client(reader, writer):
    writer.write(b"NICK_REQUEST\n")
    await writer.drain()

    nickname = None
    try:
        nickname = (await reader.readline()).decode('utf-8').strip()

        if not nickname or nickname in clients:
            await send(writer, {
                "type": "system",
                "content": "Nickname không hợp lệ hoặc đã tồn tại!"
            })
            writer.close()
            return

        clients[nickname] = writer
        print(f"[+] {nickname} connected")

        await broadcast({
            "type": "system",
            "content": f"{nickname} đã tham gia phòng chat"
        })

        while True:
            data = await reader.readline()
            if not data:
                break

            msg = json.loads(data.decode('utf-8'))

            if msg["type"] == "group":
                await broadcast(msg)

            elif msg["type"] == "private":
                receiver = msg["receiver"]
                if receiver in clients:
                    await send(clients[receiver], msg)
                    await send(writer, msg)
                else:
                    await send(writer, {
                        "type": "system",
                        "content": f"{receiver} không online"
                    })

    except Exception as e:
        print("Lỗi:", e)

    finally:
        if nickname and nickname in clients:
            del clients[nickname]
            await broadcast({
                "type": "system",
                "content": f"{nickname} đã rời đi"
            })
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"Server đang chạy tại {HOST}:{PORT}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
