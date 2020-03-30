from pathlib import Path
import sqlite3


def makeDatabase(path):
    path = Path(path)
    Path.mkdir(path.parent, exist_ok=True, parents=True)
    if path.exists():
        raise ValueError(f"That database ({path}) already exists and would be overwritten. Exiting")
    conn = sqlite3.connect(str(path))
    cursor = conn.cursor()
    return conn, cursor


def initializeDatabase(conn, cursor):
    cursor.execute("""
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title text, 
            subtitle text, 
            content text,
            url text,
            likes integer
        );
    """)
    cursor.execute("""
        CREATE TABLE participants (
            username text primary key,
            name text,
            skills text,
            interests text,
            image text
        );
    """)
    cursor.execute("""
        CREATE TABLE images (
            project integer,
            imageUrl text,
            FOREIGN KEY (project) REFERENCES 
                projects (id)
        );
    """)
    cursor.execute("""
        CREATE TABLE updates (
            project integer,
            author text,
            content text,
            date date,
            FOREIGN KEY (project) REFERENCES 
                projects (id),
            FOREIGN KEY (author) REFERENCES
                participants (username)
        );
    """)
    cursor.execute("""
        CREATE TABLE participation (
            project integer,
            participant text,
            FOREIGN KEY (project) REFERENCES
                projects (id),
            FOREIGN KEY (participant) REFERENCES
                participants (username)
        );
    """)
    cursor.execute("""
        CREATE TABLE following (
            user text,
            follows text,
            FOREIGN KEY (user) REFERENCES
                participants (username),
            FOREIGN KEY (follows) REFERENCES
                participants (username)
        );
    """)
    cursor.execute("""
        CREATE TABLE technologies (
            name text primary key
        );
    """)
    cursor.execute("""
        CREATE TABLE project_uses (
            project integer,
            tech integer,
            FOREIGN KEY (project) REFERENCES
                projects (id),
            FOREIGN KEY (tech) REFERENCES
                technologies (id)
        );
    """)
    conn.commit()


def insertProject(cursor, title, subtitle, content, url, likes):
    cursor.execute("INSERT INTO projects VALUES (?,?,?,?,?,?)", (None, title, subtitle, content, url, likes))
    return cursor.lastrowid


def insertParticipant(cursor, username, name, skills, interests, image):
    try:
        cursor.execute("INSERT INTO participants VALUES (?,?,?,?,?)", (username, name, skills, interests, image))
    except sqlite3.IntegrityError as e:
        print(f"Could not add {username} already existing.")
    finally:
        return username


def insertImage(cursor, project_id, url):
    cursor.execute("INSERT INTO images VALUES (?,?)", (project_id, url))


def insertUpdate(cursor, project_id, author, content, date):
    cursor.execute("INSERT INTO updates VALUES (?,?,?,?)", (project_id, author, content, date))


def insertParticipation(cursor, project_id, participant):
    cursor.execute("INSERT INTO participation VALUES (?,?)", (project_id, participant))


def insertFollowing(cursor, user, follows):
    cursor.execute("INSERT INTO following VALUES (?,?)", (user, follows))


def insertTechnology(cursor, name):
    try:
        cursor.execute("INSERT INTO technologies VALUES (?)", (name))
    except sqlite3.IntegrityError:
        print(f"Could not add Tech {name} already existing.")
    finally:
        return name


def insertProjectUses(cursor, project_id, tech_name):
    cursor.execute("INSERT INTO project_uses VALUES (?,?)", (project_id, tech_name))


def test_db_instanciation():
    conn, cursor = makeDatabase("test_db.db")
    initializeDatabase(conn, cursor)


if __name__ == "__main__":
    test_db_instanciation()
