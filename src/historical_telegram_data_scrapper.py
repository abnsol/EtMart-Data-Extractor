from telethon import TelegramClient
from dotenv import load_dotenv
import csv, os

# Load environments 
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Single channel Scrapper 
async def scrape_channel(client,channel_username,writer,media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title

    #iterate over the messages
    async for message in client.iter_messages(entity,limit=1000):
        media_path = None
        # download media
        if message.media and hasattr(message.media,'photo'):
            new_img_filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir,new_img_filename)

            await client.download_media(message.media,media_path)

        #write a row for this data
        writer.writerow([channel_title,channel_username,message.id,message.message,message.date,media_path])

# create client
session_store = os.path.join('data','historical_data_session') 
client = TelegramClient(session_store,api_id,api_hash)

async def main():
    await client.start()

    # create media store
    media_dir = os.path.join('data', 'photo')
    os.makedirs(media_dir, exist_ok=True)

    # open a csv to write data on
    data_folder = 'data'
    os.makedirs(data_folder, exist_ok=True)
    csv_file_path = os.path.join(data_folder, 'telegram_data.csv')
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title', 'Username', 'Id', 'Message', 'Date', 'Media path'])
        
        # list of curated 5 channels
        channels = ['@ethio_brand_collection','@Shegeronlinestore','@Leyueqa','@sinayelj','@modernshoppingcenter','@qnashcom','@MerttEka','@marakibrand']

        for channel in channels:
            await scrape_channel(client, channel , writer, media_dir)
            print(f'scrapped data from {channel}')

with client:
    client.loop.run_until_complete(main())



