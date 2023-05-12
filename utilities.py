from mysql import connector

# * Database connection details
connection = connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root", #empty for Will /TODO Change if doesn't work
    database="Project"  # for Will it's  was "bd_proj" For Georg it's "Project"             /This is for testing"testingFlask", change if shit fucks up
)


# * sql query wrapper
def dbquery(q, action="select"):
        result = []
        with connection.cursor() as cursor:
                cursor.execute(q)
                if action != "select":
                        connection.commit() # either update or insert
                else:
                        rows = cursor.fetchall()
                        if rows:
                                for r in rows:
                                        result.append(r)
                                return result # <-- result is an array, to access first row use result[0], to access first column value of first row use result[0][0]


# Game related helper functions:
def getGames():
	query = f"SELECT game_title FROM Game"
	result = dbquery(query)
	games = []

	for i in len(result):
		games.append(result[i][0])
	return games

def getGameid(game_title):
	query = f"SELECT IdGame FROM Game WHERE game_title = \'{game_title}\'"
	return dbquery(query)[0][0]

def getGametitle(gameid):
	query = f"SELECT game_title FROM Game WHERE IdGame = {gameid}"
	return dbquery(query)[0][0]

# User related helper functions:
def getUsers():
	query = f"SELECT name from User"
	result = dbquery(query)
	usernames = []

	for i in len(result):
		usernames.append(usernames[i][0])
	return usernames
	

def getUserid(email):
	query = f"SELECT IdUser FROM User WHERE email = \'{email}\'"
	return dbquery(query)[0][0]

def getUsername(userid):
	query = f"SELECT name FROM User WHERE IdUser = {userid}"
	return dbquery(query)[0][0]

# Session related helper functions:
def setSession(session, userid):
	session['userid'] = userid

def unsetSession(session):
	session['userid'] = None

def authenticate(session):
	if not session.get('userid'):
		return False
	return True



def error(message):
	return f"<script>alert(\'{message}\');window.location.assign(\'http://localhost:5000/\')</script>"
