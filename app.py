#!venv/bin/python
from flask import Flask, request, render_template, session, redirect, url_for, Response
from mysql.connector import connect
from csv import writer
from forms import EditAccountForm
import re

mydb = connect(
  host="usersrv01.cs.virginia.edu",
  user="aas8pgq",
  passwd="Spr1ng2021!!",
  database="aas8pgq"
)

cursor = mydb.cursor()

app = Flask(__name__)
app.secret_key = 'LBS'

############################## TABLE 1 ##############################
@app.route('/account/')
def account():
  if 'loggedin' in session:
    query = ("SELECT * FROM account")
    cursor.execute(query)
    data = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    with open("./data/account.csv", "w") as f:
      temp = writer(f)
      temp.writerow(headers)
      temp.writerows(data)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    return render_template('index.html', account=account, data=data, headers=headers, cols=range(len(headers)), file="/accountcsv")
  return redirect(url_for('login'))

@app.route('/accountcsv/')
def accountcsv():
  if 'loggedin' in session:
    with open("data/account.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/account.csv"}
    )
  return redirect(url_for('login'))


############################## TABLE 2 ##############################
@app.route('/course/')
def course():
  if 'loggedin' in session:
    query = ("SELECT * FROM course")
    cursor.execute(query)
    data = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    with open("./data/course.csv", "w") as f:
      temp = writer(f)
      temp.writerow(headers)
      temp.writerows(data)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    return render_template('index.html', account=account, data=data, headers=headers, cols=range(len(headers)), file="/coursecsv")
  return redirect(url_for('login'))

@app.route('/coursecsv/')
def coursecsv():
  if 'loggedin' in session:
    with open("data/course.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/course.csv"}
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
            return redirect(url_for('account'))
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
  return redirect(url_for('account'))

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

if __name__ == '__main__':
    app.run(debug=True)

