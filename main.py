import asyncio
import os
import threading
import uvicorn
from bot.main import run_bot
from api.main import app


def run_api():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


async def main():
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    await run_bot()


if __name__ == "__main__":
    asyncio.run(main())
