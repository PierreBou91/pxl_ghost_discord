import psycopg2
from psycopg2 import pool
from os import environ
from datetime import datetime

DATABASE_URL = environ['DATABASE_URL']

try:
    conn_pool =  pool.SimpleConnectionPool(5, 15, DATABASE_URL, sslmode='require')
    if (conn_pool):
        print("Database connection pool created successfully")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)

def add_user(ctx, wallet):
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
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
        return "Done"
    except psycopg2.errors.UniqueViolation as e:
        return "UniqueViolation"
    except Exception as e:
        print(e)

def safe_giveaway_launch(ctx, name, is_owner):
    giveaway_limit = check_only_giveaway(is_owner)
    if (giveaway_limit != "Done"):
        return giveaway_limit
    return launch_giveaway(ctx, name, is_owner)

def check_only_giveaway(is_owner):
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT count(*)
                    FROM giveaways
                    WHERE is_open IS TRUE
                    AND owner_giveaway IS {is_owner}
                    """
                )
                response = cursor.fetchall()
                if response[0][0] != 0:
                    if is_owner:
                        return ("OwnerUnique")
                    else:
                        return ("NonOwnerUnique")
        return "Done"
    except Exception as e:
        print(e)

def launch_giveaway(ctx, name, is_owner):
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO giveaways (
                        name,
                        creator,
                        creation_date,
                        owner_giveaway,
                        is_open
                    )
                    VALUES(%s, %s, %s, %s, %s)
                    """,
                    (
                        name,
                        ctx.author.id,
                        datetime.now(),
                        is_owner,
                        True
                    )
                )
                conn.commit()
        return "Done"
    except psycopg2.errors.UniqueViolation as e:
        return "UniqueViolation"
    except Exception as e:
        print(e)

def delete_giveaway(giveaway):
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    DELETE FROM giveaways
                    WHERE name = '{giveaway}'
                    """
                    )
                conn.commit()
        return "Done"
    except Exception as e:
        return e

def safe_add_to_giveaway(ctx):
    # check if author is owner
    # if is owner
        # check if there is an owner giveway
            # if yes:
                # check if already in the giveaway
    
    is_owner = False
    for role in ctx.author.roles:
        if role.id == 932792909504323684:
            is_owner = True
    if is_owner:
        add_owner_to_giveaways(ctx)
    

def add_owner_to_giveaways(ctx):
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE giveaways
                    SET participants = participants || '{{{str(ctx.author.id)}}}'
                    WHERE is_open IS TRUE
                    """
                    )
                conn.commit()
        return "Done"
    except Exception as e:
        print(e)
        return e