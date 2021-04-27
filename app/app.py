#!venv/bin/python
from flask import Flask, request, render_template, session, redirect, url_for, Response
from mysql.connector import connect
from csv import writer
from app.forms import EditAccountForm
import re

mydb = connect(
  host="usersrv01.cs.virginia.edu",
  user="ap2af",
  passwd="Spr1ng2021!!",
  database="ap2af_baseball_db"
)

cursor = mydb.cursor(buffered=True)

app = Flask(__name__)
app.secret_key = 'LBS'


############################## PREPARE DOWNLOADABLE CSVs ##############################
tables = ['people', 'pitching']
for table in tables:
  query = ("SELECT * FROM " + table)
  cursor.execute(query)
  data = cursor.fetchall()
  headers = [desc[0] for desc in cursor.description]
  with open("./app/data/" + table + ".csv", "w") as f:
          temp = writer(f)
          temp.writerow(headers)
          temp.writerows(data)


############################## TABLE 1 ##############################
@app.route('/people/', methods=['GET', 'POST'])
def people():
  if 'loggedin' in session:
    if request.method == 'POST':
      query = 'SELECT * FROM people LIMIT ' + (request.form.get('numrow'))
      cursor.execute(query)
      data = cursor.fetchall()
      headers = [desc[0] for desc in cursor.description]
      cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
      account = cursor.fetchone()
      return render_template('index.html', nr=request.form.get('numrow'), account=account, data=data, headers=headers, cols=range(len(headers)), file="/peoplecsv")
    else:
      query = ("SELECT * FROM people LIMIT 10")
      cursor.execute(query)
      data = cursor.fetchall()
      headers = [desc[0] for desc in cursor.description]
      cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
      account = cursor.fetchone()
      return render_template('index.html', nr='10', account=account, data=data, headers=headers, cols=range(len(headers)), file="/peoplecsv")
  return redirect(url_for('login'))

@app.route('/peoplecsv/')
def peoplecsv():
  if 'loggedin' in session:
    with open("./app/data/people.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/people.csv"}
    )
  return redirect(url_for('login'))


############################## TABLE 2 ##############################
@app.route('/pitching/')
def pitching():
  if 'loggedin' in session:
    if request.method == 'POST':
      query = 'SELECT * FROM pitching LIMIT ' + (request.form.get('numrow'))
      cursor.execute(query)
      data = cursor.fetchall()
      headers = [desc[0] for desc in cursor.description]
      cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
      account = cursor.fetchone()
      return render_template('index.html', nr=request.form.get('numrow'), account=account, data=data, headers=headers, cols=range(len(headers)), file="/pitchingcsv")
    else:
      query = ("SELECT * FROM pitching LIMIT 10")
      cursor.execute(query)
      data = cursor.fetchall()
      headers = [desc[0] for desc in cursor.description]
      cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
      account = cursor.fetchone()
      return render_template('index.html', nr='10', account=account, data=data, headers=headers, cols=range(len(headers)), file="/pitchingcsv")
  return redirect(url_for('login'))

@app.route('/pitchingcsv/')
def pitchingcsv():
  if 'loggedin' in session:
    with open("./app/data/pitching.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/pitching.csv"}
    )
  return redirect(url_for('login'))


############################## AUTH ##############################
# https://codeshack.io/login-system-python-flask-mysql/
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('people'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('auth.html', msg=msg)

@app.route('/logout/')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/')
def default():
  return redirect(url_for('people'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mydb.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/profile/')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/editprofile/', methods=['GET', 'POST'])
def editprofile():
  if 'loggedin' in session:
    form = EditAccountForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            cursor.execute("update accounts set username='%s' , password='%s', email='%s' where id='%s'" % (username,password,email,session['id']))
            mydb.commit()
        return redirect('/profile/')
    else:
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        if account:
            form.username.data = account[1]
            form.password.data = account[2]
            form.email.data = account[3]
        return render_template('editprofile.html', title='Edit Account', form=form)
  return redirect(url_for('login'))

