from datetime import datetime, timedelta
from queue import Queue
from telegram.ext import ExtBot, Dispatcher, Defaults, JobQueue
from threading import Thread

from bot.config import TOKEN, TIMEZONE
from bot.handlers import register_handlers
from bot.handlers.scheduler import scheduler


defaults = Defaults(parse_mode='MarkdownV2', disable_web_page_preview=True, tzinfo=TIMEZONE)

bot = ExtBot(token=TOKEN, defaults=defaults)

update_queue = Queue()
job_queue = JobQueue()

dispatcher = Dispatcher(bot=bot, update_queue=update_queue, job_queue=job_queue)

register_handlers(dispatcher)

thread = Thread(target=dispatcher.start, name='dispatcher')
thread.start()

now = datetime.now(TIMEZONE)
time_first = (now + timedelta(seconds=60)).replace(second=0, microsecond=0)

job_queue.set_dispatcher(dispatcher)
job_queue.run_repeating(callback=scheduler, interval=60, first=time_first, name='scheduler')
job_queue.start()
