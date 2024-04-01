from telethon import TelegramClient
import constants
import asyncio
# Create a lock to synchronize access to the Telethon client
client_lock = asyncio.Lock()

async def send_message(message):
    async with client_lock:
        async with TelegramClient(constants.PHONE_NUMBER, constants.APP_ID, constants.APP_HASH) as client:  
            destination_user_username = constants.USER_INPUT_CHANNEL
            entity = await client.get_entity(destination_user_username)
            await client.send_message(entity=entity, message=message)

async def send(message1):
    await send_message(message1)    

if __name__ == "__main__":    
    import asyncio
    asyncio.run(send('Junaid'))
