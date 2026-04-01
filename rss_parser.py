import feedparser
import asyncio
from pyrogram import Client
from database import get_all_feeds, update_last_link

async def check_rss_feeds(app: Client):
    feeds = await get_all_feeds()
    for feed in feeds:
        try:
            url = feed['url']
            chat_id = feed['chat_id']
            last_link = feed.get('last_link')

            # Run feedparser in a thread to avoid blocking the async event loop
            parsed = await asyncio.to_thread(feedparser.parse, url)
            
            if parsed.entries:
                latest_entry = parsed.entries[0]
                current_link = latest_entry.link
                
                if current_link != last_link:
                    title = latest_entry.get('title', 'No Title')
                    msg = f"**New RSS Update!**\n\n**{title}**\n[Read More]({current_link})"
                    
                    await app.send_message(chat_id, msg)
                    await update_last_link(url, chat_id, current_link)
        except Exception as e:
            print(f"Error parsing {feed['url']}: {e}")