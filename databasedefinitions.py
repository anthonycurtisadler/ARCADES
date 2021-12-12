def create_database (db_cursor):

    """Definitions for creating the database"""
    

    db_cursor.executescript("""
        CREATE TABLE IF NOT EXISTS notebooks (
            notebook TEXT NOT NULL UNIQUE );
            """)
    db_cursor.executescript("""

        CREATE TABLE IF NOT EXISTS notes (
            
            notebook TEXT NOT NULL,
            note_index TEXT NOT NULL,
            note_body TEXT DEFAULT '',
            size INTEGER DEFAULT 60,
            user TEXT DEFAULT 'user',
            UNIQUE (notebook, note_index)
            FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
            );""")
                
    db_cursor.executescript("""
        CREATE TABLE IF NOT EXISTS timestamps (
            notebook TEXT NOT NULL,
            note_index TEXT NOT NULL,
            timestamp DATE NOT NULL,
            UNIQUE (notebook, note_index, timestamp)
            FOREIGN KEY (notebook, note_index) REFERENCES notes (notebook, note_index) ON DELETE CASCADE 
            );""")
                            
    db_cursor.executescript("""        
        CREATE TABLE IF NOT EXISTS all_note_keys (
            notebook TEXT NOT NULL,
            note_index TEXT NOT NULL,
            keyword TEXT NOT NULL,
            UNIQUE (notebook, note_index, keyword)
            FOREIGN KEY (notebook, note_index) REFERENCES notes (notebook, note_index) ON DELETE CASCADE
            );""")
    db_cursor.executescript("""                        
        CREATE TABLE IF NOT EXISTS all_words (
            notebook TEXT NOT NULL,
            word TEXT NOT NULL,
            UNIQUE (notebook, word)
            );""")
    db_cursor.executescript("""
        CREATE TABLE IF NOT EXISTS all_keys (
            keyword TEXT NOT NULL,
            notebook TEXT NOT NULL,
            UNIQUE (keyword, notebook)
            );""")

    db_cursor.executescript("""
        CREATE TABLE IF NOT EXISTS keys_to_indexes (
            notebook TEXT NOT NULL,
            keyword TEXT NOT NULL,
            note_index TEXT NOT NULL,
            UNIQUE (keyword, notebook, note_index)
            FOREIGN KEY (notebook, keyword) REFERENCES all_keys (notebook, keyword) ON DELETE CASCADE
            );""")
    db_cursor.executescript("""
        CREATE TABLE IF NOT EXISTS tags_to_keys (
            notebook TEXT NOT NULL,
            tag TEXT NOT NULL,
            keyword TEXT NOT NULL,
            UNIQUE (notebook, tag, keyword)
            FOREIGN KEY (notebook, keyword) REFERENCES all_keys (notebook, keyword) ON DELETE CASCADE
            );
        """)
    db_cursor.executescript("""
        CREATE TABLE IF NOT EXISTS word_to_indexes (
            notebook TEXT NOT NULL,
            word TEXT NOT NULL,
            note_index TEXT NOT NULL,
            UNIQUE (notebook, word, note_index)
            FOREIGN KEY (notebook, word) REFERENCES all_words (notebook, word) ON DELETE CASCADE
            );
        """)

    db_cursor.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
            notebook TEXT NOT NULL UNIQUE,
            projectfile TEXT,
            FOREIGN KEY (notebook) REFERENCES notebooks (notebook)
            );
            
            """)
    db_cursor.executescript("""
        CREATE TABLE IF NOT EXISTS defaults (
            notebook TEXT NOT NULL,
            attribute TEXT NOT NULL,
            content TEXT NOT NULL,
            UNIQUE (notebook, attribute)
            FOREIGN KEY (notebook) REFERENCES notebooks (notebook)
            );
            """)

    db_cursor.executescript("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_all_words ON all_words (notebook, word);""")

    db_cursor.executescript("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_all_keys ON all_keys (notebook, keyword);""")

    db_cursor.executescript("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_notes ON notes (notebook, note_index);""")

            


