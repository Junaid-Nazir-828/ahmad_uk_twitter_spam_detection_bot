from flask import Flask, jsonify
import threading
import asyncio
from telethon import TelegramClient, events
import constants
import tele_wraper
import full_flow

app = Flask(__name__)

# class TelegramListener:
#     def __init__(self, api_id, api_hash, phone_number, channel_username):
#         self.api_id = api_id
#         self.api_hash = api_hash
#         self.phone_number = phone_number
#         self.channel_username = channel_username
#         self.client = TelegramClient('twitter', self.api_id, self.api_hash)
#         self.client.session.report_errors = False

#     async def authenticate_and_connect(self):
#         await self.client.connect()        

#     async def start_listener(self):
#         await self.authenticate_and_connect()
#         @self.client.on(events.NewMessage(chats=self.channel_username))
#         async def new_message_listener(event):
#             print(f"m : {event.message.text}")
#             if event.message.text.startswith("RE : "):
#                 pass
#             else:
#                 await tele_wraper.check_tele_messages(event.message.text)
        
#         async with self.client:
#             await self.client.run_until_disconnected()

#     async def stop_listener(self):
#         await self.client.disconnect()

# listener = TelegramListener(constants.APP_ID, constants.APP_HASH, constants.PHONE_NUMBER, constants.USER_INPUT_CHANNEL)

# def start_telegram_listener():
#     asyncio.run(listener.start_listener())

# telegram_thread = threading.Thread(target=start_telegram_listener)

@app.route("/", methods=['GET','POST'])
def read_root():
    print('Testing home route')
    return 'Hello this is Junaid'

# @app.route('/start-tele-listener', methods=['GET','POST'])
# def start_listener():
#     telegram_thread.start()
#     return jsonify({'message': 'Tele Listener started successfully'})

# @app.route('/stop-tele-listener', methods=['GET','POST'])
# def stop_listener():
#     asyncio.run(listener.stop_listener())
#     return jsonify({'message': 'Tele Listener stopped successfully'})

@app.route('/start-x-listener',methods=['GET','POST'])
def start_x_listener():
    thread_2 = threading.Thread(target=full_flow.handle_full_twitter_flow)
    thread_2.start()
    return jsonify({'message': 'Twitter Listener started successfully'})


if __name__ == '__main__':
    app.run(debug=False)
