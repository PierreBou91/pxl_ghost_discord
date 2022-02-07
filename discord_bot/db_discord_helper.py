from psycopg2 import connect
from os import environ
from datetime import datetime

DATABASE_URL = environ['DATABASE_URL']

def add_user(ctx):
    with connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO test (id, name, creation_date) VALUES(%s, %s, %s)
            """,
                (ctx.author.id,
                ctx.author.name,
                datetime.now())
            )
            conn.commit()
            cursor.close()
            print(ctx.author.id)
