import mysql.connector
from mysql.connector import errorcode

print("Connecting... Hold tight, we're going in!")

try:
      conn = mysql.connector.connect(
            host='localhost',
            user='main_root',
            password='welcome'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something went wrong with the username or password, huh?')
      else:
            print(f"Oops, something else went wrong: {err}")

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `api4noobs`;")  # Who needs old databases anyway?

cursor.execute("CREATE DATABASE `api4noobs`;")  # New shiny database coming up!

cursor.execute("USE `api4noobs`;")  # Using the new shiny database... "Feelin' fancy!"

# Creating tables (we’re building the future here)
TABLES = {}
TABLES['games'] = ('''
      CREATE TABLE `games` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      `category` varchar(40) NOT NULL,
      `company` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['users'] = ('''
      CREATE TABLE `users` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nickname` varchar(8) NOT NULL,
      `password` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for table_name in TABLES:
      table_sql = TABLES[table_name]
      try:
            print(f'Creating table {table_name}: ', end=' ')
            cursor.execute(table_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Oops, this table already exists.')
            else:
                  print(f"Error: {err.msg}")
      else:
            print('Table created successfully!')

# Inserting users (we’re populating the world with cool people)
user_sql = 'INSERT INTO users (nickname, password) VALUES (%s, %s)'
users = [
      ("Ayres", "welcome".Strip()),
      ("ALC", "hamsters".Strip()),
      ("JsS", "password123".Strip())
]
cursor.executemany(user_sql, users)

cursor.execute('SELECT * FROM users')
print(' ------------- Users:  -------------')
for user in cursor.fetchall():
    print(user[1])  # Printing just the nickname, no secrets revealed! 

# Inserting games 
game_sql = 'INSERT INTO games (name, category, company) VALUES (%s, %s, %s)'
games = [
      ('Zelda', 'Adventure', 'Nintendo'),
      ('God of War', 'Hack n Slash', 'Sony'),
      ('Halo', 'FPS', 'Microsoft'),
      ('Metroid', 'Metroidvania', 'Nintendo'),
      ('Dark Souls', 'Souls', 'FromSoftware'),
      ('Red Dead Redemption', 'Action-Adventure', 'Rockstar'),
]
cursor.executemany(game_sql, games)

cursor.execute('SELECT * from games')
print(' ------------- Games:  -------------')
for game in cursor.fetchall():
    print(game[1])  # We all know games are life!

# Committing changes (Otherwise, it's like it never happened)
conn.commit()

cursor.close()
conn.close()

print("All done!") # we're done here, folks!