from faulthandler import is_enabled
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
class GhostMember:
    def __init__(self, id, name, display_name, nick, discriminator, mention, created_at, joined_at, top_role, is_bot, wallet=None, is_here=True):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.nick = nick
        self.discriminator = discriminator
        self.mention = mention
        self.wallet = wallet
        self.created_at = created_at
        self.joined_at = joined_at
        self.top_role = top_role
        self.is_bot = is_bot
        self.is_here = is_here
    
    def __eq__(self, other):
        if (isinstance(other, GhostMember)):
            return self.id == other.id
        return False

    def __hash__(self):
        return int(self.id)

def member_adapter_from_discord(member):
    adapted_member = GhostMember(
        str(member.id),
        member.name,
        member.display_name,
        member.nick,
        int(member.discriminator),
        member.mention,
        member.created_at,
        member.joined_at,
        member.top_role.id,
        member.bot
        )
    
    return adapted_member

def member_adapter_from_db(member):
    adapted_member = GhostMember(
        member[0],
        member[1],
        member[2],
        member[3],
        member[4],
        member[5],
        member[7],
        member[8],
        member[9],
        member[10],
        member[6],
        member[11]
    )
    return adapted_member

def add_user(member):
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO members (
                        id,
                        name,
                        display_name,
                        nick,
                        discriminator,
                        mention,
                        wallet,
                        created_at,
                        joined_at,
                        top_role,
                        is_bot,
                        is_here
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                    member.id,
                    member.name,
                    member.display_name,
                    member.nick,
                    member.discriminator,
                    member.mention,
                    None,
                    member.created_at,
                    member.joined_at,
                    member.top_role,
                    member.is_bot,
                    True
                    )
                )
                conn.commit()
        return "Done"
    except psycopg2.errors.UniqueViolation as e:
        return "UniqueViolation"
    except Exception as e:
        print(f"Exception in add_user: {e}")

def add_multiple_users(memberlist):
    try:
        conn = conn_pool.getconn()
        cursor = conn.cursor()
        for member in memberlist:
            cursor.execute(
                """
                INSERT INTO members (
                    id,
                    name,
                    display_name,
                    nick,
                    discriminator,
                    mention,
                    wallet,
                    created_at,
                    joined_at,
                    top_role,
                    is_bot,
                    is_here
                )
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                member.id,
                member.name,
                member.display_name,
                member.nick,
                member.discriminator,
                member.mention,
                None,
                member.created_at,
                member.joined_at,
                member.top_role,
                member.is_bot,
                True
                )
            )
        conn.commit()
        cursor.close()
        conn_pool.putconn(conn)
        return "Done"
    except psycopg2.errors.UniqueViolation as e:
        return "UniqueViolation"
    except Exception as e:
        print(f"Exception in add_multiple_users: {e}")

################ IN DEV ##################

def get_members():
    members = {}
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM members
                    """
                )
                for row in cursor.fetchall():
                    members[str(row[0])] = member_adapter_from_db(row)
        return members
    except psycopg2.errors.UniqueViolation as e:
        return "UniqueViolation"
    except Exception as e:
        print(f"Exception in get_members: {e}")

def member_is_in_db(member):
    try:
        with conn_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT *
                    FROM members
                    WHERE id = '{member.id}'
                    """
                )
                return len(cursor.fetchall()) == 1
    except Exception as e:
        print(f"Exception in member_is_in_db(): {e}")

def update_is_here(memberlist, is_here):
    try:
        conn = conn_pool.getconn()
        cursor = conn.cursor()
        for mem in memberlist:
            cursor.execute(
                f"""
                UPDATE members
                SET is_here = '{is_here}'
                WHERE id = '{mem.id}'
                """
            )
        conn.commit()
        cursor.close()
        conn_pool.putconn(conn)
        return ("Done")
    except Exception as e:
        print(f"Exception in update_is_here(): {e}")    

def update_nick_and_displayname(memberlist):
    try:
        conn = conn_pool.getconn()
        cursor = conn.cursor()
        for mem in memberlist:
            cursor.execute(
                f"""
                UPDATE members
                SET nick = '{mem.nick}', display_name = '{mem.display_name}'
                WHERE id = '{mem.id}'
                """
            )
        conn.commit()
        cursor.close()
        conn_pool.putconn(conn)
        return ("Done")
    except Exception as e:
        print(f"Exception in update_nick_and_displayname(): {e}")   


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
        print(f"Exception in check_only_giveaway: {e}")

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
        print(f"Exception in launch_giveaway: {e}")

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
        print(f"Exception in delete_giveaway: {e}")
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
        print(f"Exception in add_owner_to_giveaways: {e}")
        return e
