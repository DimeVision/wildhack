import aiomysql

import bot_init
import config


async def create_connection_pool(loop):
    return await aiomysql.create_pool(
        host=config.DB_HOST,
        port=3306,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        db=config.DB_NAME,
        loop=loop,
        autocommit=True
    )

db_connection_pool = \
    bot_init.loop.run_until_complete(create_connection_pool(bot_init.loop))
