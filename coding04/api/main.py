import time
import json
import ast
from fastapi import FastAPI
from starlette.websockets import WebSocket
import hit_and_blow

app = FastAPI()
digit = hit_and_blow.DIGIT

# 接続中のクライアントを識別するためのヘッダを格納
clients = {}
# ユーザー名を格納
users = {}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    # クライアントを識別するためのヘッダを取得
    key = ws.headers.get('sec-websocket-key')
    clients[key] = ws
    try:
        while True:
            # クライアントからメッセージを受信
            msg = await ws.receive_json()
            print(msg)

            if 'user' in msg:
                print(key)
                # 送られてきたデータがuserフォームのものであった場合、ユーザー情報を保存
                users[key] = msg.get('user')
                data = {
                    'user': f"You are '{msg.get('user')}'"
                }
                await clients[key].send_json(data)
            elif 'answer' in msg:
                print(key)
                # 送られてきたデータがgameフォームのものであった場合
                hit, blow = hit_and_blow.check_the_answer(msg.get('answer'))
                if hit == digit:
                    data = {
                        'answer': f"Clear! Winner {users.get(key)}"
                    }
                else:
                    data = {
                        'answer': f"{users.get(key)}  Hit: {hit} Blow: {blow}"
                    }
                # 接続中のクライアントそれぞれにメッセージを送信（ブロードキャスト）
                for client in clients.values():
                    await client.send_json(data)
            else:
                raise()
    except:
        await ws.close()
        # 接続が切れた場合、当該クライアントを削除する
        del clients[key]
