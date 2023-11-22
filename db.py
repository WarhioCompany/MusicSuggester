import sqlite3

db_name = 'db.db'


def get_cursor():
    conn = sqlite3.connect(db_name)
    return conn.cursor()


def create_db():
    c = get_cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS search ( 
    id integer PRIMARY KEY,
    query text NOT NULL,
    uri text NOT NULL UNIQUE,
    type text NOT NULL,
    name text NOT NULL,
    artist text,
    cover text NON NULL,
    duration text
    ); """)


def add_search_results(query, new_data):
    cursor = get_cursor()
    query = query.replace(' ', '_')

    add_data(cursor, query, new_data['track'] + new_data['album'] + new_data['artist'])

    cursor.connection.commit()


def add_data(cursor, query, data):
    for element in data:
        insert(cursor, query, element['uri'], element['type'], element['name'],
               element['artist'], element['cover'], element['duration'])


def update_data(cursor, query, data):
    for element in data:
        update(cursor, query, element['uri'])


def insert(cursor, query, uri, elem_type, name, artist, cover, duration):
    try:
        cursor.execute(f"INSERT INTO search (query, uri, type, name, artist, cover, duration) "
                       f"VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (query, uri, elem_type, name, f'"{artist}"', cover, duration))
    except sqlite3.IntegrityError:
        update(cursor, query, uri)


def update(cursor, query, uri):
    res = cursor.execute(f"SELECT query, uri FROM search WHERE uri = ?", (uri,)).fetchone()
    queries = set(res[0].split() + [query])
    cursor.execute("UPDATE search SET query = ? WHERE uri = ?", (' '.join(queries), res[1]))


def print_table():
    c = get_cursor()
    res = c.execute("SELECT * FROM search")
    [print(i) for i in res]


def search_by_query(query):
    c = get_cursor()
    res = {
        'track': [],
        'album': [],
        'artist': []
    }

    query_res = c.execute("SELECT * FROM search ORDER BY type").fetchall()
    search_res = [i for i in query_res if query.replace(' ', '_') in i[1].split()]

    columns = ['query', 'uri', 'type', 'name', 'artist', 'cover', 'duration']
    for element in search_res:
        data = {}
        for i in range(len(columns)):
            data[columns[i]] = element[i + 1]
        data['artist'] = data['artist'][1:-1]
        res[data['type']].append(data)

    return res
