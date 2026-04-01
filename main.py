import os
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web  # NEW IMPORT

# ... [Keep all your existing database, rss_parser, and pyrogram command logic here exactly as they were] ...

# --- NEW: Dummy Web Server for Free Hosting Health Checks ---
async def web_handler(request):
    return web.Response(text="RSS Bot is alive and running!")

async def start_web_server():
    webapp = web.Application()
    webapp.router.add_get('/', web_handler)
    runner = web.AppRunner(webapp)
    await runner.setup()
    
    # Cloud providers inject the PORT environment variable. Default to 8080.
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Dummy web server listening on port {port} for health checks.")

# --- Updated Main Execution ---
async def main():
    # 1. Start the dummy web server FIRST so the platform registers it
    await start_web_server()

    # 2. Start RSS Scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_rss_feeds, "interval", minutes=5, args=[app])
    scheduler.start()
    
    # 3. Start Pyrogram Bot
    print("Bot is starting...")
    await app.start()
    print("Bot is running!")
    
    # Keep the script running
    import pyrogram
    await pyrogram.idle()

if __name__ == "__main__":
    app.run(main())