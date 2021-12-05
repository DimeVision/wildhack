from aiomysql import Pool, DictCursor

from database.db_mysql import db_connection_pool


class DBCommands:
    connection_pool: Pool = db_connection_pool

    FIND_FAQ = "SELECT f.description FROM std_1930_wildhack.faq as f WHERE f.id='%s'"
    INSERT_VOLUNTEER = "INSERT INTO std_1930_wildhack.volunteers (name, email, birthdate, phone, education, desired_area, check_in_date, check_out_date, languages, experience, skills, book, recommendation, motivation, video) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    async def find_faq(self, faq_id):
        async with self.connection_pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(self.FIND_FAQ, faq_id)
                return await cur.fetchone()

    async def add_volunteer(self, shit):
        async with self.connection_pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(self.INSERT_VOLUNTEER, shit)
                return await cur.fetchone


commands = DBCommands()
