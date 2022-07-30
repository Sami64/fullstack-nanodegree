import psycopg2

connection = psycopg2.connect('dbname=smashbros54')

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS todos;")

cursor.execute(''' 
CREATE TABLE todos (
    id serial PRIMARY KEY,
    description VARCHAR NOT NULL
);
''')

cursor.execute('INSERT INTO todos (id,description) VALUES (%s, %s);', (1,"First todo"))
# dictionary method
SQL = 'INSERT INTO todos (id, description) VALUES (%(id)s, %(description)s)'
data = {'id': 2, 'description': 'Dictionary description'}
cursor.execute(SQL, data)

# read sql data
cursor.execute('SELECT * from todos')
result = cursor.fetchall()
print(result)

connection.commit()
cursor.close()
connection.close()
