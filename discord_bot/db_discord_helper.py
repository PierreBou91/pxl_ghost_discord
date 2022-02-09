from psycopg2 import connect
from os import environ
from datetime import datetime

DATABASE_URL = environ['DATABASE_URL']

def add_user(ctx, wallet):
    with connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO members (
                    id,
                    name,
                    display_name,
                    wallet_address,
                    creation_date,
                    top_role
                    )
                    VALUES(%s, %s, %s, %s, %s, %s)
                """,
                    (
                    ctx.author.id,
                    ctx.author.name,
                    ctx.author.display_name,
                    wallet,
                    datetime.now(),
                    ctx.author.top_role.id,
                    )
                )
            conn.commit()
            cursor.close()
