import psycopg2
from psycopg2 import pool
from os import environ
from datetime import datetime

DATABASE_URL = environ['DATABASE_URL']

try:
    conn_pool =  pool.SimpleConnectionPool(10, 18, DATABASE_URL, sslmode='require')
    if (conn_pool):
        print("Database connection pool created successfully")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)

def add_user(ctx, wallet):
    with conn_pool.getconn() as conn:
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

