from mysql.connector import connect

mydb = connect(
  host="usersrv01.cs.virginia.edu",
  user="aas8pgq",
  passwd="Spr1ng2021!!",
  database="aas8pgq"
)

cursor = mydb.cursor()
query = ("SELECT * FROM account")
cursor.execute(query)
for r in cursor:
  print(r)
