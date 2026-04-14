import asyncio
import os
import uvicorn
from api.main import app
from bot.main import application, run_bot, shutdown


async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    server = uvicorn.Server(config)
    await run_bot()
    await server.serve()
    await application.updater.stop()
    await application.stop()
    await application.shutdown()
    await shutdown()


if __name__ == "__main__":
    asyncio.run(main())