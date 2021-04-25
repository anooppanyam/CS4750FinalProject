#!venv/bin/python
from flask import Flask, request, render_template, session, redirect, url_for
from mysql.connector import connect
from csv import writer

mydb = connect(
  host="usersrv01.cs.virginia.edu",
  user="aas8pgq",
  passwd="Spr1ng2021!!",
  database="aas8pgq"
)

cursor = mydb.cursor()

app = Flask(__name__)
app.secret_key = 'LBS'

@app.route('/account')
def account():
  query = ("SELECT * FROM account")
  cursor.execute(query)
  data = cursor.fetchall()
  headers = [desc[0] for desc in cursor.description]
  with open("data/account.csv", "w") as f:
    temp = writer(f)
    temp.writerow(headers)
    temp.writerows(data)
  return render_template('index.html', data=data, headers=headers, cols=range(len(headers)))

@app.route('/course')
def course():
  query = ("SELECT * FROM course")
  cursor.execute(query)
  data = cursor.fetchall()
  headers = [desc[0] for desc in cursor.description]
  with open("data/course.csv", "w") as f:
    temp = writer(f)
    temp.writerow(headers)
    temp.writerows(data)
  return render_template('index.html', data=data, headers=headers, cols=range(len(headers)))

if __name__ == '__main__':
    app.run(debug=True)

