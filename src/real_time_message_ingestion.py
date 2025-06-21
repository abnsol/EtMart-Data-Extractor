from telethon import TelegramClient, events
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone') 

session_store = os.path.join('data','sessions','real_time_session') 
client = TelegramClient(session_store, api_id, api_hash)

# Define a directory for media files
REALTIME_MEDIA_DIR = os.path.join('data','output_data','photos')
os.makedirs(REALTIME_MEDIA_DIR, exist_ok=True)

REALTIME_CSV_FILE = os.path.join('data','output_data','telegram_data.csv')
csv_file = open(REALTIME_CSV_FILE, 'a', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

# Write header only if the file is new/empty
if os.stat(REALTIME_CSV_FILE).st_size == 0:
    csv_writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

@client.on(events.NewMessage(chats=['@ethio_brand_collection','@Shegeronlinestore','@Leyueqa','@sinayelj','@modernshoppingcenter','@qnashcom','@MerttEka','@marakibrand'])) 
async def handler(event):
    message = event.message
    channel_entity = await event.get_chat()
    channel_title = channel_entity.title if hasattr(channel_entity, 'title') else "Unknown Channel"
    channel_username = channel_entity.username if hasattr(channel_entity, 'username') else str(channel_entity.id)

    media_path = None
    if message.media:
        if hasattr(message.media, 'photo'):
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(REALTIME_MEDIA_DIR, filename)
            await client.download_media(message.media, media_path)
            print(f"Downloaded photo: {media_path}")

    print(f"New message from {channel_title} (@{channel_username}): {message.text or '[No Text]'} [ID: {message.id}]")
    csv_writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])
    csv_file.flush() 

async def real_time_main():
    print("Client starting for real-time ingestion...")
    await client.start()
    print("Client is running. Listening for new messages...")
    await client.run_until_disconnected() 

if __name__ == '__main__':
    try:
        with client:
            client.loop.run_until_complete(real_time_main())
    except KeyboardInterrupt:
        print("Stopping real-time ingestion...")
    finally:
        if csv_file:
            csv_file.close()
            print("CSV file closed.")