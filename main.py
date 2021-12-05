from aiogram import executor
from bot_init import dispatcher
from controllers import client_handler


async def on_startup(_):
    print('Бот запустился')


client_handler.register_client_handler(dispatcher)

if __name__ == "__main__":
    from controllers.client_handler import dispatcher

    executor.start_polling(dispatcher, on_startup=on_startup, skip_updates=True)
