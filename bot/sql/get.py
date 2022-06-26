from bot.sql import query_execute
from bot.sql.create import create_users


def get_users():
    create_users()
    query = """
            SELECT *
            FROM users
            ORDER BY userid;
            """
    out = query_execute(query)
    return out if out else []


def get_user(user_id):
    create_users()
    query = """
            SELECT *
            FROM users
            WHERE userid = {0};
            """
    out = query_execute(query.format(user_id))
    return out[0] if out else []


def get_table(user_id):
    query = """
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'people_{0}';
            """
    out = query_execute(query.format(user_id))
    return out[0][0] if out else None


def get_people(user_id):
    create_users()
    query = """
            CREATE TABLE IF NOT EXISTS people_{0} (
                userid      INTEGER   PRIMARY KEY UNIQUE NOT NULL,
                switchstate BOOLEAN   DEFAULT FALSE,
                years       INTEGER[] DEFAULT NULL,
                ignored     BOOLEAN   DEFAULT FALSE
            );
            INSERT INTO people_{0} (userid) (
                SELECT userid
                FROM users
                WHERE userid != {0}
                AND username is not NULL
                AND gender is not NULL
                AND birthday is not NULL
            )
            ON CONFLICT (userid) DO NOTHING;
            DELETE FROM people_{0}
            WHERE EXISTS (
                SELECT *
                FROM users
                WHERE users.userid = people_{0}.userid
                AND (
                    users.username is NULL
                    OR users.gender is NULL
                    OR users.birthday is NULL
                )
            );
            DELETE FROM people_{0}
            WHERE NOT EXISTS (
                SELECT *
                FROM users
                WHERE users.userid = people_{0}.userid
            );
            SELECT *
            FROM people_{0}
            ORDER BY userid;
            """
    out = query_execute(query.format(user_id))
    return out if out else []


def get_birthday(timezone, user_id):
    create_users()
    query = """
            SELECT userid, username, gender
            FROM users
            WHERE to_char(current_timestamp at time zone {0}, 'DD.MM') =
                  to_char(birthday, 'DD.MM')
            AND userid != {1}
            ORDER BY userid;
            """
    out = query_execute(query.format(f"'{timezone}'", user_id))
    return out if out else []


def get_every(user_id):
    query = """
            SELECT userid
            FROM people_{0}
            ORDER BY userid;
            """
    out = query_execute(query.format(user_id))
    return [row[0] for row in out] if out else []


def get_switched(user_id, state):
    query = """
            SELECT userid
            FROM people_{0}
            WHERE switchstate = {1}
            ORDER BY userid;
            """
    out = query_execute(query.format(user_id, state))
    return [row[0] for row in out] if out else []


def get_prompted(user_id):
    query = """
            SELECT userid
            FROM people_{0}
            WHERE date_part('year', current_date)::INTEGER = ANY(years)
            ORDER BY userid;
            """
    out = query_execute(query.format(user_id))
    return [row[0] for row in out] if out else []


def get_ignored(user_id):
    query = """
            SELECT userid
            FROM people_{0}
            WHERE ignored = True
            ORDER BY userid;
            """
    out = query_execute(query.format(user_id))
    return [row[0] for row in out] if out else []


def get_holidays():
    query = """
            CREATE TABLE IF NOT EXISTS holidays (
                data   JSONB   DEFAULT '{}'::jsonb,
                latest INTEGER DEFAULT NULL
            );
            SELECT *
            FROM holidays;
            """
    out = query_execute(query)
    return out[0] if out else []
