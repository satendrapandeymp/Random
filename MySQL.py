import MySQLdb

# database connection parameters
Database_ip = "localhost"
Database_user = "root"
Password = ""
Database_name="temp"

# connecting to the database
conn = MySQLdb.connect(Database_ip, Database_user, Password, Database_name)
c = conn.cursor()
conn.set_character_set('utf8')

# create a table for customers
query = 'create table customers (name VARCHAR(32), address VARCHAR(128))'
c.execute(query)

# insert into table
query = "insert into customers (name, address) values ('Satyendra', 'Kanpur, India')"
c.execute(query)

# commiting these changes to the database
conn.commit()

# updating a row
query = "update customers set name = 'Narendra' where name REGEXP '^S' "
c.execute(query)

conn.commit()

# select all from table
query = "select * from customers"
responses = c.execute(query)
if responses:
    datas = c.fetchall()
for i in datas:
    print i

print "Done with basics"