import asyncio
import os
import uvicorn
from api.main import app
from bot.main import run_bot


async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    server = uvicorn.Server(config)
    
    await asyncio.gather(
        server.serve(),
        run_bot()
    )


if __name__ == "__main__":
    asyncio.run(main())
