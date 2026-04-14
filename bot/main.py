import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import BOT_TOKEN
from db.connection import init_db, close_db
from db.migrations import create_tables, ensure_defaults
from bot.handlers.start import start_handler
from bot.handlers.menu import menu_handler, menu_callback
from bot.handlers.profile import profile_handler
from bot.handlers.link import link_handler
from bot.handlers.referrals import referrals_handler
from bot.handlers.ai import ai_handler
from bot.services.welcome import schedule_welcome_series
from bot.services.broadcast import schedule_broadcasts

logger = logging.getLogger(__name__)

application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler('start', start_handler))
application.add_handler(CommandHandler('menu', menu_handler))
application.add_handler(CommandHandler('profile', profile_handler))
application.add_handler(CommandHandler('link', link_handler))
application.add_handler(CommandHandler('refs', referrals_handler))
application.add_handler(CommandHandler('ai', ai_handler))
application.add_handler(CallbackQueryHandler(menu_callback))
application.add_error_handler(lambda update, context: logger.exception('Bot error', exc_info=context.error))

scheduler = AsyncIOScheduler()
scheduler.add_job(schedule_welcome_series, 'interval', minutes=15)
scheduler.add_job(schedule_broadcasts, 'interval', minutes=5)


async def startup():
    pool = await init_db()
    await create_tables(pool)
    await ensure_defaults(pool)


async def shutdown():
    await close_db()


async def run_bot():
    if not BOT_TOKEN:
        raise RuntimeError('BOT_TOKEN is required')
    scheduler.start()
    await startup()
    await application.initialize()
    await application.start()
    await application.updater.start_polling()