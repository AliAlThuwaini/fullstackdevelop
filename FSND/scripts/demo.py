import psycopg2

connection = psycopg2.connect('dbname=example user=postgres')

# cursor is an interface that allows you to queau work and txns
cursor = connection.cursor()

# We want to create a new table in our db (we'll drop it if it exists, reason: if we rerun the script not to create the same table twice). because we want to pass multi-line command, the way to do that is through a trible quoates

cursor.execute('DROP TABLE IF EXISTS table2')

cursor.execute('''
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT False
    );
''')

#cursor.execute('INSERT INTO table2 (id, completed) VALUES (1, true);')

#another way to insert is by passing arguments to string:
cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s,%s);' ,(1, True))

connection.commit()

#closing: psycopy2 will not close the connection for you and we need to do manually
connection.close()
cursor.close()