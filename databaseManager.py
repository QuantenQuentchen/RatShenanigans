import sqlite3


class dbManager():

    instance = None
    
    def getInstance():
        if dbManager.instance is None:
            dbManager.instance = dbManager()
        return dbManager.instance

    def __init__(self):
        self.connection = sqlite3.connect("data/democracy.db")
        self.cur = self.connection.cursor()
        self.create_tables_if_not_exist()

    def create_tables_if_not_exist(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS constitution (
                number INTEGER PRIMARY KEY,
                title TEXT NOT NULL
            );
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS paragraphs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                para_id INTEGER,
                FOREIGN KEY (para_id) REFERENCES constitution(number)
            );
        """)


        #Old revision Artikel
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS constitution_old (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                art_id INTEGER,
                title TEXT NOT NULL,
                FOREIGN KEY (art_id) REFERENCES constitution(number)
            );
        """)

        #Old revision Paragraph
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS paragraphs_old (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                para_id INTEGER,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (para_id) REFERENCES paragraphs(number)
            );
        """)

        #Proposed changes
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS article_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                art_id INTEGER,
                title TEXT NOT NULL,
                FOREIGN KEY (art_id) REFERENCES constitution(number)
            );
        """)

        #Proposed changes
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS paragraph_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                para_id INTEGER,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (para_id) REFERENCES paragraphs(number)
            );
        """)

        # Create the users table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                discord_id INTEGER PRIMARY KEY,
                balance REAL
            );
        """)

        # Create the companies table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value REAL NOT NULL
            );
        """)

        # Create the user_stocks table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS user_stocks (
                discord_id INTEGER,
                company_id INTEGER,
                stocks_held INTEGER,
                PRIMARY KEY (discord_id, company_id),
                FOREIGN KEY (discord_id) REFERENCES users(discord_id),
                FOREIGN KEY (company_id) REFERENCES companies(company_id)
            );
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            );
        """)

        self.connection.commit()

    def add_article(self, number, title, paragraphs):
        self.cur.execute("INSERT INTO constitution (number, title) VALUES (?, ?)", (number, title))
        for paragraph in paragraphs:
            self.cur.execute("INSERT INTO paragraphs (para_id, title, content) VALUES (?, ?, ?)", (number, paragraph["title"], paragraph["content"]))
        self.connection.commit()

    def get_all_articleIDs(self):
        self.cur.execute("SELECT number FROM constitution")
        result = self.cur.fetchall()

        return result
    
    def drop_articles(self):
        self.cur.execute("DELETE FROM constitution")
        self.cur.execute("DELETE FROM paragraphs")
        self.connection.commit()

    def fix_all_articleIDs(self):
        for article in self.get_all_articleIDs():
            self.cur.execute("SELECT title FROM constitution WHERE number = ?", (article[0],))
            oldTitle = self.cur.fetchone()[0]
            oldTitle = oldTitle.replace("Artikel", "")
            oldTitle = oldTitle.replace(str(article[0]), "")
            oldTitle = oldTitle.strip()
            self.cur.execute("UPDATE constitution SET title = ? WHERE number = ?", (article[0], article[0]))

    def get_article(self, article_number: int):

        self.cur.execute("SELECT title FROM constitution WHERE number = ?", (article_number,))
        title = self.cur.fetchall()

        self.cur.execute("SELECT title, content FROM paragraphs WHERE para_id = ? ORDER BY id ASC",(article_number,))
        paragraphs = self.cur.fetchall()

        para = []
        for paragraph in paragraphs:
            paragraphRes = {}
            paragraphRes["title"] = paragraph[0]
            paragraphRes["content"] = paragraph[1]
            para.append(paragraphRes)

        return {"num": article_number, "title": title, "paragraphs": para}

    def add_memory(self, question, answer):
        self.cur.execute("INSERT INTO memory (question, answer) VALUES (?, ?)", (question, answer))
        self.connection.commit()
    def get_question(self, question):
        self.cur.execute("SELECT answer FROM memory WHERE question = ?", (question,))
        result = self.cur.fetchone()

        return result[0] if result else None
    
    def get_answer(self, answer):
        self.cur.execute("SELECT question FROM memory WHERE answer = ?", (answer,))
        result = self.cur.fetchone()

        return result[0] if result else None
    
    def get_random_memory(self):
        self.cur.execute("SELECT id FROM memory ORDER BY RANDOM() LIMIT 1")
        result = self.cur.fetchone()

        return result if result else None

    def remove_memory(self, question):
        self.cur.execute("DELETE FROM memory WHERE question = ?", (question,))
        self.connection.commit()

    def drop_tables(self):
        self.cur.execute("DROP TABLE IF EXISTS users")
        self.cur.execute("DROP TABLE IF EXISTS companies")
        self.cur.execute("DROP TABLE IF EXISTS user_stocks")
        self.cur.execute("DROP TABLE IF EXISTS constitution_changes")
        self.cur.execute("DROP TABLE IF EXISTS memory")
        self.connection.commit()

    def get_all_companies(self):
        self.cur.execute("SELECT company_id FROM companies")
        result = self.cur.fetchall()

        return result

    def set_company_value(self, company_id, value):
        self.cur.execute("UPDATE companies SET value = ? WHERE company_id = ?", (value, company_id))
        self.connection.commit()

    def get_company_value(self, company_id):
        self.cur.execute("SELECT value FROM companies WHERE company_id = ?", (company_id,))
        result = self.cur.fetchone()

        return result[0] if result else None

    def get_company_name(self, company_id):
        self.cur.execute("SELECT name FROM companies WHERE company_id = ?", (company_id,))
        result = self.cur.fetchone()

        return result[0] if result else None
    
    def does_user_exist(self, discord_id):
        self.cur.execute("SELECT 1 FROM users WHERE discord_id = ?", (discord_id,))
        result = self.cur.fetchone()

        return True if result else False

    def get_user_balance(self, discord_id):

        self.add_user(discord_id, 100)

        self.cur.execute("SELECT balance FROM users WHERE discord_id = ?", (discord_id,))
        result = self.cur.fetchone()


        return result[0]

    def set_user_balance(self, discord_id, new_balance):

        self.add_user(discord_id, 100)

        self.cur.execute("UPDATE users SET balance = ? WHERE discord_id = ?", (new_balance, discord_id))
        self.connection.commit()

    def get_company_value(self, company_id):
        
            self.cur.execute("SELECT value FROM companies WHERE company_id = ?", (company_id,))
            result = self.cur.fetchone()
        
        
            return result[0] if result else None

    def get_user_stocks(self, discord_id, company_id):

        self.cur.execute("SELECT stocks_held FROM user_stocks WHERE discord_id = ? AND company_id = ?", (discord_id, company_id))
        result = self.cur.fetchone()

        return result[0] if result else None

    def get_all_user_stocks(self, discord_id):
        
            self.cur.execute("SELECT company_id, stocks_held FROM user_stocks WHERE discord_id = ?", (discord_id,))
            result = self.cur.fetchall()
        
        
            return result

    def add_user(self, discord_id, balance):
        if not self.does_user_exist(discord_id):
            self.cur.execute("INSERT INTO users (discord_id, balance) VALUES (?, ?)", (discord_id, balance))
            self.connection.commit()

    def add_company(self, name, value):
        self.cur.execute("SELECT 1 FROM companies WHERE name = ?", (name,))
        result = self.cur.fetchone()
        if result:
            return
        self.cur.execute("INSERT INTO companies (name, value) VALUES (?, ?)", (name, value))
        self.connection.commit()

    def add_stocks_to_user(self, discord_id, company_id, additional_stocks):
        # Check if the user already has stocks of the company
        self.cur.execute("SELECT stocks_held FROM user_stocks WHERE discord_id = ? AND company_id = ?", (discord_id, company_id))
        result = self.cur.fetchone()

        if result:
            # User already has stocks, update the amount
            current_stocks = result[0]
            new_total = current_stocks + additional_stocks
            self.cur.execute("UPDATE user_stocks SET stocks_held = ? WHERE discord_id = ? AND company_id = ?", (new_total, discord_id, company_id))
        else:
            # User does not have stocks of this company, insert a new record
            self.cur.execute("INSERT INTO user_stocks (discord_id, company_id, stocks_held) VALUES (?, ?, ?)", (discord_id, company_id, additional_stocks))
        
        self.connection.commit()

    def increment_company_value(self, company_id, percentage):
            current_value = self.get_company_value(company_id)
            increment = current_value*percentage
            self.cur.execute("UPDATE companies SET value = value + ? WHERE company_id = ?", (increment, company_id))
            self.connection.commit()
    
    def remove_company(self, company_id):
        self.cur.execute("DELETE FROM companies WHERE company_id = ?", (company_id,))
        self.connection.commit()
