import sqlite3
from contextlib import closing


def create_table(conn):
    with closing(conn.cursor()) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        """)
        conn.commit()


def insert_user(conn, name, email, age):
    with closing(conn.cursor()) as cur:
        cur.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (name, email, age)
        )
        conn.commit()
        return cur.lastrowid


def get_all_users(conn):
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM users")
        return cur.fetchall()


def get_user_by_id(conn, user_id):
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cur.fetchone()


def update_user(conn, user_id, name, email, age):
    with closing(conn.cursor()) as cur:
        cur.execute(
            "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?",
            (name, email, age, user_id)
        )
        conn.commit()


def delete_user(conn, user_id):
    with closing(conn.cursor()) as cur:
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()


def main():
    conn = sqlite3.connect("database.db")

    try:
        create_table(conn)

        user_id = insert_user(conn, "Leandro", "leandro@example.com", 26)
        print(f"Created user with ID: {user_id}")

        insert_user(conn, "Maria", "maria@example.com", 24)
        insert_user(conn, "Joao", "joao@example.com", 30)

        print("\nAll users:")
        for user in get_all_users(conn):
            print(user)

        user = get_user_by_id(conn, user_id)
        print(f"\nUser {user_id}: {user}")

        update_user(conn, user_id, "Leandro Santos", "leandro@example.com", 27)
        print(f"\nUpdated user {user_id}: {get_user_by_id(conn, user_id)}")

        delete_user(conn, user_id)
        print(f"\nDeleted user {user_id}")
        print("Remaining users:", get_all_users(conn))

    finally:
        conn.close()


if __name__ == "__main__":
    main()
