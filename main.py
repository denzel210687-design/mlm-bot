import asyncio
import os
import uvicorn
from bot.main import run_bot
from api.main import app

async def main():
    bot_task = asyncio.create_task(run_bot())
    api_config = uvicorn.Config(app, host='0.0.0.0', port=int(os.getenv('PORT', '8000')))
    api_server = uvicorn.Server(api_config)
    api_task = asyncio.create_task(api_server.serve())
    await asyncio.gather(bot_task, api_task)

if __name__ == '__main__':
    asyncio.run(main())
