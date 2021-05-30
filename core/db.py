import psycopg2
from loguru import logger
import dj_database_url
import dotenv
import pandas as pd

from .utils import monday


class Database:
    def __init__(self):
        self.conn = None
        self.connect()
        self.create_table()

    def connect(self):
        dotenv.load_dotenv()
        db_config = dj_database_url.config(conn_max_age=600)
        self.conn = psycopg2.connect(
            database=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT'],
        )
        logger.info(f"Connected to database {db_config['NAME']} successfully")

    def execute(self, commands):
        try:
            cur = self.conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.exception(error)

    def delete_table(self):
        commands = [
            """
            DROP TABLE IF EXISTS submissions;
            """
        ]
        self.execute(commands)

    def create_table(self):
        commands = [
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id SERIAL PRIMARY KEY,
                user_name varchar(45) NOT NULL,
                create_date DATE NOT NULL DEFAULT CURRENT_DATE
            );
            """
        ]
        self.execute(commands)

    def reset_table(self):
        self.delete_table()
        self.create_table()

    def get_table(self):
        table = pd.read_sql('select * from submissions', self.conn)
        return table

    def get_weekly_summary(self):
        table = pd.read_sql(
            f"""
                select 
                    * 
                from 
                    submissions 
                where 
                    create_date >= '{monday()}'::DATE;
                """,
            self.conn
        )

        users = table.drop_duplicates(subset=["user_name"])['user_name']
        summary_stat = {
            'user': users,
            'submissions': [self.get_weekly_user_count(user) for user in users]
        }

        return pd.DataFrame(summary_stat, columns=['user', 'submissions'])

    def get_weekly_user_count(self, user):
        table = pd.read_sql(
            f"""
                select 
                    * 
                from 
                    submissions 
                where 
                    user_name='{user}' AND
                    create_date >= '{monday()}'::DATE;
            """,
            self.conn
        )
        return len(table)

    def add_submission(self, user):
        commands = [
            f"""
            INSERT INTO submissions (user_name)
            VALUES('{user}');
            """
        ]
        self.execute(commands)

    def add_missed_submission(self, user, date: str):
        commands = [
            f"""
            INSERT INTO submissions (user_name, create_date)
            VALUES('{user}', '{date}'::DATE);
            """
        ]
        self.execute(commands)


if __name__ == '__main__':
    db = Database()
    db.add_submission("anya")
