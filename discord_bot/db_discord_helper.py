from faulthandler import is_enabled
import psycopg2
from psycopg2 import pool
from os import environ
from datetime import datetime

DATABASE_URL = environ['DATABASE_URL']

try:
    CONN_POOL = pool.SimpleConnectionPool(
        5, 15, DATABASE_URL, sslmode='require')
    if (CONN_POOL):
        print("Database connection pool created successfully")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)

# Class and adapters
class GhostMember:
    def __init__(self, id, name, display_name, nick, discriminator, mention, created_at, joined_at, top_role, is_bot, is_here=True):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.nick = nick
        self.discriminator = discriminator
        self.mention = mention
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
        member[6],
        member[8],
        member[9],
        member[10],
    )
    return adapted_member

# Member stuff

def add_user(member):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            """
            INSERT INTO members (
                id,
                name,
                display_name,
                nick,
                discriminator,
                mention,
                created_at,
                joined_at,
                top_role,
                is_bot,
                is_here
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                member.id,
                member.name,
                member.display_name,
                member.nick,
                member.discriminator,
                member.mention,
                member.created_at,
                member.joined_at,
                member.top_role,
                member.is_bot,
                True
            )
        )
        conn.commit()
        close_connection(conn, cursor)
    except Exception as e:
        print(f"Exception in add_user: {e}")


def add_multiple_users(memberlist):
    try:
        conn, cursor = open_connection()
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
                    created_at,
                    joined_at,
                    top_role,
                    is_bot,
                    is_here
                )
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    member.id,
                    member.name,
                    member.display_name,
                    member.nick,
                    member.discriminator,
                    member.mention,
                    member.created_at,
                    member.joined_at,
                    member.top_role,
                    member.is_bot,
                    True
                )
            )
        conn.commit()
        close_connection(conn, cursor)
    except Exception as e:
        print(f"Exception in add_multiple_users: {e}")


def get_all_members():
    members = {}
    try:
        conn, cursor = open_connection()
        cursor.execute(
            """
            SELECT *
            FROM members
            """
        )
        response = cursor.fetchall()
        close_connection(conn, cursor)
        for row in response:
            members[str(row[0])] = member_adapter_from_db(row)
        return members
    except Exception as e:
        print(f"Exception in get_all_members: {e}")


def update_is_here(memberlist, is_here):
    try:
        conn = CONN_POOL.getconn()
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
        close_connection(conn, cursor)
    except Exception as e:
        print(f"Exception in update_is_here(): {e}")


def update_db(memberlist):
    try:
        conn = CONN_POOL.getconn()
        cursor = conn.cursor()
        for mem in memberlist:
            cursor.execute(
                f"""
                UPDATE members
                SET nick = '{mem.nick}', display_name = '{mem.display_name}', top_role = '{mem.top_role}'
                WHERE id = '{mem.id}'
                """
            )
        conn.commit()
        close_connection(conn, cursor)
    except Exception as e:
        print(f"Exception in update_db(): {e}")


def member_is_in_db(member):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            f"""
            SELECT *
            FROM members
            WHERE id = '{member.id}'
            """
        )
        response = cursor.fetchall()
        close_connection(conn, cursor)
        return len(response) == 1
    except Exception as e:
        print(f"Exception in member_is_in_db(): {e}")


def get_member_by_id(id):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            f"""
            SELECT *
            FROM members
            WHERE id = '{id}'
            """
        )
        response = cursor.fetchall()
        close_connection(conn, cursor)
        return member_adapter_from_db(response[0])
    except Exception as e:
        print(f"Exception in get_member_by_id: {e}")

# Giveaway stuff

def check_only_giveaway(is_owner):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            f"""
            SELECT count(*)
            FROM giveaways
            WHERE is_open IS TRUE
            AND is_owner_only IS {is_owner}
            """
        )
        response = cursor.fetchall()
        close_connection(conn, cursor)
        return response[0][0] == 0
    except Exception as e:
        print(f"Exception in check_only_giveaway: {e}")


def launch_giveaway(ctx, is_owner):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            """
            INSERT INTO giveaways (
                creator,
                created_at,
                is_owner_only,
                is_open
            )
            VALUES(%s, %s, %s, %s)
            """,
            (
                ctx.author.id,
                datetime.now(),
                is_owner,
                True
            )
        )
        conn.commit()
        close_connection(conn, cursor)
    except Exception as e:
        print(f"Exception in launch_giveaway: {e}")


def delete_giveaway(giveaway_id):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            f"""
            DELETE FROM giveaways
            WHERE id = '{giveaway_id}'
            """
        )
        conn.commit()
        close_connection(conn, cursor)
    except Exception as e:
        print(f"Exception in delete_giveaway: {e}")


def check_if_ongoing_giveaway():
    try:
        conn, cursor = open_connection()
        cursor.execute(
            f"""
            SELECT count(*)
            FROM giveaways
            WHERE is_open IS TRUE
            """
        )
        response = cursor.fetchall()
        close_connection(conn, cursor)
        return response[0][0] > 0
    except Exception as e:
        print(f"Exception in check_only_giveaway: {e}")


def check_if_member_in_giveaway(member):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            f"""
            SELECT *
            FROM giveaways
            WHERE is_open IS TRUE
            """
        )
        response = cursor.fetchall()
        close_connection(conn, cursor)
        if response[0][2] is None:
            return False
        return member.id in response[0][2]
    except Exception as e:
        print(f"Exception in check_if_member_in_giveaway: {e}")


def add_member_to_giveaway(member):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            f"""
            UPDATE giveaways
            SET participants = participants || '{{{member.id}}}'
            WHERE is_open IS TRUE
            """
        )
        conn.commit()
        close_connection(conn, cursor)
    except Exception as e:
        print(f"Exception in add_member_to_giveaways: {e}")
        return e

# Wallet stuff

def wallet_already_in_db(wallet):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            f"""
            SELECT *
            FROM wallets
            WHERE address = '{wallet}'
            """
        )
        response = cursor.fetchall()
        close_connection(conn, cursor)
        if len(response) == 0:
            return False, None
        else:
            return True, get_member_by_id(response[0][2])
    except Exception as e:
        print(f"Exception in wallet_already_in_db: {e}")


def add_wallet(member, wallet):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            """
            INSERT INTO wallets (
                address,
                owner
            )
            VALUES(%s, %s)
            """,
            (
                wallet,
                member.id,
            )
        )
        conn.commit()
        close_connection(conn, cursor)
    except Exception as e:
        print(f"Exception in add_wallet: {e}")


def wallet_matches_onwer(member, wallet):
    try:
        conn, cursor = open_connection()
        cursor.execute(
            f"""
            SELECT *
            FROM wallets
            WHERE address = '{wallet}'
            """
        )
        response = cursor.fetchall()
        close_connection(conn, cursor)
        if response[0][2] == member.id:
            return True, member
        else:
            return False, get_member_by_id(response[0][2])
    except Exception as e:
        print(f"Exception in add_wallet: {e}")

############### HANDLERS #################

def open_connection():
    conn = CONN_POOL.getconn()
    cursor = conn.cursor()
    return conn, cursor


def close_connection(connection, cursor):
    cursor.close()
    CONN_POOL.putconn(connection)

################ IN DEV ##################
