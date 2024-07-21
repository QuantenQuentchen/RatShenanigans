import sqlite3


class PrefManager:

    class kind:
        Stock = 0
        Vote = 1
        Log = 2
        Constitution = 3

    instance = None
    
    #Nooow this is important as it interacts with the persitant DB, it uses SQL, which is technically another Lamguage so ig learning it is a good idea

    def getInstance():
        if PrefManager.instance is None:
            PrefManager.instance = PrefManager()
        return PrefManager.instance

    def __init__(self):
        #defines the connection to the db (currently the file democracy.db in the data subfolder)
        self.connection = sqlite3.connect("data/pref.db")
        self.cur = self.connection.cursor()
        self.create_tables_if_not_exist()
    
    def create_tables_if_not_exist(self):
        #creates the tables if they don't exist
        self.cur.execute("CREATE TABLE IF NOT EXISTS channel_prefs (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id TEXT, kind INTEGER, channel TEXT, UNIQUE(kind, guild_id));")
        self.connection.commit()
    
    def drop_tables(self):
        #drops the tables
        self.cur.execute("DROP TABLE channel_prefs;")
        self.connection.commit
    
    def get_channel(self, kind, guild_id, default=None):
        if not self.does_channel_exist(kind, guild_id) and default is not None:
            self.set_channel(kind, guild_id, default)
        #gets the channel for a specific kind
        self.cur.execute("SELECT channel FROM channel_prefs WHERE kind = ? AND guild_id = ?", (kind, guild_id))
        return int(self.cur.fetchone()[0])

    def set_channel(self, kind, guild_id, channel):
        #sets the channel for a specific kind
        print(kind, guild_id, channel)
        self.cur.execute("INSERT OR REPLACE INTO channel_prefs (channel, kind, guild_id) VALUES (?, ?, ?)", (channel, kind, guild_id))
        self.connection.commit()
    
    def does_channel_exist(self, kind, guild_id):
        #checks if a channel exists
        self.cur.execute("SELECT channel, guild_id FROM channel_prefs WHERE kind = ? AND guild_id = ?", (kind, guild_id))
        return self.cur.fetchone() is not None