CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS items (
        [id] INTEGER PRIMARY KEY,
        [name] TEXT NOT NULL,
        [size] REAL NOT NULL,
        [creation_date] datetime NOT NULL
    )
    """
