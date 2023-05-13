from mysql import connector
from socket import gethostname

# * Database connection details
database="Project"
if gethostname() == "Entropy":
	database="bd_proj"
connection = connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root", #empty for Will /TODO Change if doesn't work
    database=database  # for Will it's  was "bd_proj" For Georg it's "Project"             /This is for testing"testingFlask", change if shit fucks up
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
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def getGametitle(gameid):
	query = f"SELECT game_title FROM Game WHERE IdGame = {gameid}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def getGamerating(gameid):
	query = f"SELECT user_rating FROM Game WHERE IdGame = {gameid}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def getGamecopyright(gamied):
	query = f"SELECT copyright FROM Game WHERE IdGame = {gameid}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

# Room related helper functions:
def getRooms():
	query = f"SELECT room_name from Room"
	result = dbquery(query)
	rooms = []

	for i in len(result):
		rooms.append(result[i][0])
	return rooms

def getRoomid(room_name):
	query = f"SELECT IdRoom FROM Room WHERE room_name = \'{room_name}\'"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def getRoomname(roomid):
	query = f"SELECT room_name FROM Room WHERE IdRoom = {roomid}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def getRoomcapacity(roomid):
	query = f"SELECT room_capacity FROM Room WHERE IdRoom = {roomid}"
	result = dbqueryh(query)
	if not result:
		return None
	return result[0][0]

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
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def getUsername(userid):
	query = f"SELECT name FROM User WHERE IdUser = {userid}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def getUseremail(userid):
	query = f"SELECT email FROM User WHERE IdUser = {userid}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def getUserbalance(userid):
	query = f"SELECT balance FROM User WHERE IdUser = {userid}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]


# Web Session related helper functions:
def setSession(session, userid):
	session['userid'] = userid

def unsetSession(session):
	session['userid'] = None

def authenticate(session):
	if not session.get('userid'):
		return False
	return True


# Other helper functions:
def error(message,redirect=""):
	return f"<script>alert(\'{message}\');window.location.assign(\'http://localhost:5000/{redirect}\')</script>"
