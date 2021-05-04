#!venv/bin/python
from flask import Flask, request, render_template, session, redirect, url_for, Response
from mysql.connector import connect
from csv import writer
from app.forms import EditAccountForm
import re
import hashlib 

mydb = connect(
  host="usersrv01.cs.virginia.edu",
  user="ss9ae",
  passwd="Spring2020!!!",
  database="ss9ae"
)

cursor = mydb.cursor()




users = {
  "ss9ae_a": 'Spr1ng2021!!',
  "ss9ae_b": 'Spr1ng2021!!',
  "ss9ae_c": 'Spr1ng2021!!'
}



app = Flask(__name__)
app.secret_key = 'LBS'


############################## PREPARE DOWNLOADABLE CSVs ##############################
tables = ['people', 'pitching', 'batting', 'fielding', 'allstarfull', 'halloffame', 'battingpost', 'pitchingpost', 'awardsplayers', 'fieldingpost', 'appearances', 'teams', 'leagues', 'divisions']
# for table in tables:
#   cnx = connect(host="usersrv01.cs.virginia.edu", user="ss9ae_c", passwd=users['ss9ae_c'], database="ss9ae")
#   cursor = cnx.cursor()
#   query = ("SELECT * FROM " + table)
#   cursor.execute(query)
# 
#   data = cursor.fetchall()
#   cnx.close()
#   headers = [desc[0] for desc in cursor.description]
#   with open("./app/data/" + table + ".csv", "w") as f:
#           temp = writer(f)
#           temp.writerow(headers)
#           temp.writerows(data)


def displayTable(table):
  if 'loggedin' in session:
    cnx = connect(host="usersrv01.cs.virginia.edu", user="ss9ae_c", passwd=users['ss9ae_c'], database="ss9ae")
    if request.method == 'POST':
      query = "SELECT * FROM %s LIMIT 30" % table
      cursor.execute(query)
      cnx.close()
      data = cursor.fetchall()
      headers = [desc[0] for desc in cursor.description]
      if request.form.get('right'):
        ncol = min(len(headers), int(request.form.get('right'))+7)
      elif request.form.get('left'):
        ncol = max(7, int(request.form.get('left'))-7)
      else:
        ncol = 7
    else:
      query = "SELECT * FROM %s LIMIT 30" % (table)
      cursor.execute(query)
      data = cursor.fetchall()
      headers = [desc[0] for desc in cursor.description]
      ncol = 7
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    cnx.close()
    return render_template('index.html', nc=ncol, account=account, data=data, headers=headers[ncol-7:ncol], cols=range(len(headers))[ncol-7:ncol], file="/" + table + "csv")
    
  return redirect(url_for('login'))


############################## PEOPLE ##############################
@app.route('/people/', methods=['GET', 'POST'])
def people():
  return displayTable('people')

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


############################## PITCHING ##############################
@app.route('/pitching/', methods=['GET', 'POST'])
def pitching():
  return displayTable('pitching')

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


############################## BATTING ##############################
@app.route('/batting/', methods=['GET', 'POST'])
def batting():
  return displayTable('batting')

@app.route('/battingcsv/')
def battingcsv():
  if 'loggedin' in session:
    with open("./app/data/batting.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/batting.csv"}
    )
  return redirect(url_for('login'))


############################## FIELDING ##############################
@app.route('/fielding/', methods=['GET', 'POST'])
def fielding():
  return displayTable('fielding')

@app.route('/fieldingcsv/')
def fieldingcsv():
  if 'loggedin' in session:
    with open("./app/data/fielding.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/fielding.csv"}
    )
  return redirect(url_for('login'))


############################## ALLSTARFULL ##############################
@app.route('/allstarfull/', methods=['GET', 'POST'])
def allstarfull():
  return displayTable('allstarfull')

@app.route('/allstarfullcsv/')
def allstarfullcsv():
  if 'loggedin' in session:
    with open("./app/data/allstarfull.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/allstarfull.csv"}
    )
  return redirect(url_for('login'))


############################## halloffame ##############################
@app.route('/halloffame/', methods=['GET', 'POST'])
def halloffame():
  return displayTable('halloffame')

@app.route('/halloffamecsv/')
def halloffamecsv():
  if 'loggedin' in session:
    with open("./app/data/halloffame.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/halloffame.csv"}
    )
  return redirect(url_for('login'))


############################## BATTINGPOST ##############################
@app.route('/battingpost/', methods=['GET', 'POST'])
def battingpost():
  return displayTable('battingpost')

@app.route('/battingpostcsv/')
def battingpostcsv():
  if 'loggedin' in session:
    with open("./app/data/battingpost.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/battingpost.csv"}
    )
  return redirect(url_for('login'))


############################## PITCHINGPOST ##############################
@app.route('/pitchingpost/', methods=['GET', 'POST'])
def pitchingpost():
  return displayTable('pitchingpost')

@app.route('/pitchingpostcsv/')
def pitchingpostcsv():
  if 'loggedin' in session:
    with open("./app/data/pitchingpost.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/pitchingpost.csv"}
    )
  return redirect(url_for('login'))


############################## AWARDSPLAYERS ##############################
@app.route('/awardsplayers/', methods=['GET', 'POST'])
def awardsplayers():
  return displayTable('awardsplayers')

@app.route('/awardsplayerscsv/')
def awardsplayerscsv():
  if 'loggedin' in session:
    with open("./app/data/awardsplayers.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/awardsplayers.csv"}
    )
  return redirect(url_for('login'))


############################## fieldingPOST ##############################
@app.route('/fieldingpost/', methods=['GET', 'POST'])
def fieldingpost():
  return displayTable('fieldingpost')

@app.route('/fieldingpostcsv/')
def fieldingpostcsv():
  if 'loggedin' in session:
    with open("./app/data/fieldingpost.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/fieldingpost.csv"}
    )
  return redirect(url_for('login'))


############################## APPEARANCES ##############################
@app.route('/appearances/', methods=['GET', 'POST'])
def appearances():
  return displayTable('appearances')

@app.route('/appearancescsv/')
def appearancescsv():
  if 'loggedin' in session:
    with open("./app/data/appearances.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/appearances.csv"}
    )
  return redirect(url_for('login'))


############################## TEAMS ##############################
@app.route('/teams/', methods=['GET', 'POST'])
def teams():
  return displayTable('teams')

@app.route('/teamscsv/')
def teamscsv():
  if 'loggedin' in session:
    with open("./app/data/teams.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/teams.csv"}
    )
  return redirect(url_for('login'))


############################## LEAGUES ##############################
@app.route('/leagues/', methods=['GET', 'POST'])
def leagues():
  return displayTable('leagues')

@app.route('/leaguescsv/')
def leaguescsv():
  if 'loggedin' in session:
    with open("./app/data/leagues.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/leagues.csv"}
    )
  return redirect(url_for('login'))


############################## DIVISIONS ##############################
@app.route('/divisions/', methods=['GET', 'POST'])
def divisions():
  return displayTable('divisions')

@app.route('/divisionscsv/')
def divisionscsv():
  if 'loggedin' in session:
    with open("./app/data/divisions.csv") as fp:
          csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=data/divisions.csv"}
    )
  return redirect(url_for('login'))


############################## AUTH ##############################
# https://codeshack.io/login-system-python-flask-mysql/
@app.route('/login/', methods=['GET', 'POST'])
def login():
    print(session)
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access

        username = request.form['username']
        password = encode_pass(request.form['password'])
        cnx = connect(host="usersrv01.cs.virginia.edu", user="ss9ae_b", passwd=users['ss9ae_b'], database="ss9ae")
        cursor = cnx.cursor()
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        cnx.close()
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
    print(session)
    print()
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
  if 'loggedin' in session:
    return redirect(url_for('profile'))
  else:
    return redirect(url_for('login'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        # Create variables for easy access
        username = request.form['username']
        password = encode_pass(request.form['password'])
        email = request.form['email']
        cnx = connect(host='usersrv01.cs.virginia.edu', user='ss9ae_b', password=users['ss9ae_b'], database="ss9ae",  auth_plugin='mysql_native_password')
        cursor = cnx.cursor()
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
            cnx.commit()
            cnx.close()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
    

@app.route('/profile/')
def profile():
  
  if not ('loggedin' in session):
    return redirect(url_for('login'))

  cnx = connect(host="usersrv01.cs.virginia.edu", user="ss9ae_c", passwd=users['ss9ae_c'], database="ss9ae")
  # We need all the account info for the user so we can display it on the profile page
  cursor = cnx.cursor()
  cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
  account = cursor.fetchone()
  cnx.close()
  # Show the profile page with account info
  
  return render_template('profile.html', account=account)


@app.route('/editprofile/', methods=['GET', 'POST'])
def editprofile():
  if not 'loggedin' in session:
    redirect(url_for('login'))

  form = EditAccountForm()
  
  if request.method == 'POST':
      if form.validate_on_submit():
          # username = form.username.data
          # email = form.email.data
          # password = encode_pass(form.password.data)
          
          try:
            cnx = connect(host="usersrv01.cs.virginia.edu", user="ss9ae_c", passwd=users['ss9ae_c'], database="ss9ae")
            cursor = cnx.cursor()

            if encode_pass(form.password.data) == encode_pass(""):
              cursor.execute("update accounts set username=%(username)s , email=%(email)s where id=%(id)s" , {'username': form.username.data,
              'email': form.email.data,
              'id': session['id']
              })
            else:
              cursor.execute("update accounts set username=%(username)s , password=%(password)s, email=%(email)s where id=%(id)s" , {'username': form.username.data,
                'password': encode_pass(form.password.data),
                'email': form.email.data,
                'id': session['id']
                })

            cnx.commit()
            cnx.close()
          except:
            return render_template('editprofile.html', msg="Username already exists!", form=form)

      return render_template('editprofile.html', msg="Change Successful!", form=form)
  else: 
      cnx = connect(host="usersrv01.cs.virginia.edu", user="ss9ae_c", passwd=users['ss9ae_c'], database="ss9ae")
      cursor = cnx.cursor()
      cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
      account = cursor.fetchone()
      cnx.close()
      if account:
          form.username.data = account[1]
          form.password.data = ""
          form.email.data = account[3]

  return render_template('editprofile.html', msg='', form=form)

@app.route('/player/<playerid>/', methods=['GET', 'POST'])
def player(playerid):
  if not 'loggedin' in session:
    return redirect(url_for('login'))

  cnx = connect(host="usersrv01.cs.virginia.edu", user="ss9ae_c", passwd=users['ss9ae_c'], database="ss9ae")
  cnx.cursor()
  cursor.execute('SELECT * FROM people WHERE playerID = %s', (playerid,))
  test = cursor.fetchall()
  cnx.close()
  
  if not test:
    return redirect(url_for('search-player'))  # ---> redirect to search players if player id passed into url has no route 

  cnx = connect(host="usersrv01.cs.virginia.edu", user="ss9ae_c", passwd=users['ss9ae_c'], database="ss9ae")
  cursor.execute('SELECT * FROM people WHERE playerID = %s', (playerid,))
  people_headers = [desc[0] for desc in cursor.description]
  people_info = cursor.fetchall()

  cursor.execute('SELECT * FROM pitching WHERE playerID = %s', (playerid,))
  pitch_headers = [desc[0] for desc in cursor.description]
  pitch_info = cursor.fetchall()
  
  cursor.execute('SELECT * FROM batting WHERE playerID = %s', (playerid,))
  batting_headers = [desc[0] for desc in cursor.description]
  batting_info = cursor.fetchall()
  
  cursor.execute('SELECT * FROM fielding WHERE playerID = %s', (playerid,))
  fielding_headers = [desc[0] for desc in cursor.description]
  fielding_info = cursor.fetchall()
  
  cursor.execute('SELECT * FROM allstarfull WHERE playerID = %s', (playerid,))
  allstarfull_headers = [desc[0] for desc in cursor.description]
  allstarfull_info = cursor.fetchall()
  
  cursor.execute('SELECT * FROM halloffame WHERE playerID = %s', (playerid,))
  halloffame_headers = [desc[0] for desc in cursor.description]
  halloffame_info = cursor.fetchall()
  
  cursor.execute('SELECT * FROM battingpost WHERE playerID = %s', (playerid,))
  battingpost_headers = [desc[0] for desc in cursor.description]
  battingpost_info = cursor.fetchall()
  
  cursor.execute('SELECT * FROM pitchingpost WHERE playerID = %s', (playerid,))
  pitchingpost_headers = [desc[0] for desc in cursor.description]
  pitchingpost_info = cursor.fetchall()
  
  cursor.execute('SELECT * FROM awardsplayers WHERE playerID = %s', (playerid,))
  awardsplayers_headers = [desc[0] for desc in cursor.description]
  awardsplayers_info = cursor.fetchall()
  
  cursor.execute('SELECT * FROM fieldingpost WHERE playerID = %s', (playerid,))
  fieldingpost_headers = [desc[0] for desc in cursor.description]
  fieldingpost_info = cursor.fetchall()
  
  cursor.execute('SELECT * FROM appearances WHERE playerID = %s', (playerid,))
  appearances_headers = [desc[0] for desc in cursor.description]
  appearances_info = cursor.fetchall()
  cnx.close()
    
  return render_template('player.html',
      player=playerid,
      people=people_info, people_headers=people_headers,
      pitch=pitch_info, pitch_headers=pitch_headers,
      batting=batting_info, batting_headers=batting_headers,
      fielding=fielding_info, fielding_headers=fielding_headers,
      allstarfull=allstarfull_info, allstarfull_headers=allstarfull_headers,
      halloffame=halloffame_info, halloffame_headers=halloffame_headers,
      battingpost=battingpost_info, battingpost_headers=battingpost_headers,
      pitchingpost=pitchingpost_info, pitchingpost_headers=pitchingpost_headers,
      awardsplayers=awardsplayers_info, awardsplayers_headers=awardsplayers_headers,
      fieldingpost=fieldingpost_info, fieldingpost_headers=fieldingpost_headers,
      appearances=appearances_info, appearances_headers=appearances_headers,
      pitchlen=range(len(pitch_headers)),
      battinglen=range(len(batting_headers)),
      fieldinglen=range(len(fielding_headers)),
      allstarlen=range(len(allstarfull_headers)),
      halloffamelen=range(len(halloffame_headers)),
      battingpostlen=range(len(battingpost_headers)),
      pitchingpostlen=range(len(pitchingpost_headers)),
      awardslen=range(len(awardsplayers_headers)),
      fieldingpostlen=range(len(fieldingpost_headers)),
      appearanceslen=range(len(appearances_headers)),
      peoplelen=range(len(people_headers)),
      )


@app.route('/search-player/')
def search_player():
  if not 'loggedin' in session:
    return redirect(url_for('login'))

  query = request.args.get('query')
  orderby = request.args.get('orderby')
  table = request.args.get('table')

  cmd = """SELECT * from career_pitching_saber WHERE Full_Name LIKE %s"""
  if(table == 'Pitching'):
    cmd == """SELECT * from career_pitching_saber WHERE Full_Name LIKE %s"""
  elif(table == 'Batting'):
    cmd = """SELECT * from career_batting_saber WHERE Full_Name LIKE %s"""

  if query is None:
    query = ''

  name = ('%%' + query + '%%').lower()

  if orderby is None or orderby == 'None' or orderby == '':
    orderby = 'playerID'
  
  if orderby is not None and orderby != 'None':
      cmd = cmd + ' ORDER BY ' + orderby + ' DESC LIMIT 10' 
  else:
      cmd = cmd + ' LIMIT 10' 

  
  cnx = connect(host="usersrv01.cs.virginia.edu", user="ss9ae_c", passwd=users['ss9ae_c'], database="ss9ae")
  cursor = cnx.cursor()
  cursor.execute(cmd, (name, ))
  search_headers = [desc[0] for desc in cursor.description]

  result = []
  for item in cursor:
      result.append(item)
  
  cnx.close()

  if len(result) == 0:
      context = dict(message='Player not found!') 
  else:
      context = dict(data=result, cols = range(len(result[0])), query=query, orderby=orderby, data_header = search_headers) ##Code addition


  return render_template('search-player.html', **context)




#### static function to hash passwords ####
def encode_pass(pwd):
  return hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), bytes([32]), 100000)


