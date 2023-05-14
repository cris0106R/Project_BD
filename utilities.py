from mysql import connector
from socket import gethostname
from datetime import date

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

# Reservation related helper functions:
# TODO Crisitan must complete this part 
# NOTE: getting a user's reservation is already implemented in the user helper function section
def getReservations():
	return ""

def getReservationid(userid):
	return ""

def getReservationtime(reservationid):
	return ""

def addReservation(userid, alloctime):
	return ""

def deleteReservation(reservationid):
	return ""



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

def isRoomfull(roomid):
	sessionid = getSessionid("Room", roomid)
	query = f"SELECT COUNT(DISTINCT(IdUser)) FROM Reservation WHERE IdSession = {sessionid}"
	result = dbquery(query)
	if not result:
		return None
	if result == getRoomcapcity(roomid):
		return True
	return False

# User related helper functions:
def getUsers():
	query = f"SELECT name from User"
	result = dbquery(query)
	usernames = []

	for i in len(result):
		usernames.append(result[i][0])
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

def getUserreservation(userid):
	query = f"SELECT IdReservation FROM Reservation WHERE IdUser = {userid}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def changeUseremail(userid, newemail):
	query = f"UPDATE User SET email = \'{newemail}\' WHERE IdUser = {userid}"
	dbquery(query, "UPDATE")	

def changeUsername(userid, newname):
	query = f"UPDATE User SET name = \'{newname}\' WHERE IdUser = {userid}"
	dbquery(query, "UPDATE")

def addUserbalance(userid, amount):
	amount = getUserbalanace(userid) + amount
	query = f"UPDATE User SET balance = {amount} WHERE IdUser = {userid}"
	dbquery(query, "UPDATE")


# Game Session related helper functions:
def getSessionid(_type, _id):
	query = f"SELECT IdSession FROM Session WHERE Id{_type} = {_id}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def newSession(gameid):
	gamesessionid =  getmaxid("Session") 
	if not gamesessionid: # if it's the first session to be created
		gamesessionid = 0
	else:
		gamesessionid += 1

	roomid = __import__('random').randrange(getmaxid("Room"))

	for r in getRooms():
		if roomid != getRoomid(r):
			date =  date.today().strftime("%d/%m/%Y")
			query = f"INSERT INTO Session (Session.IdSession, Session.IdRoom, Session.IdGame, Session.date) VALUES ({gamesessionid}, {roomid}, {gameid}, {date})"
			dbquery(query, "INSERT")
			return 0
	
	return 1


# Web Session related helper functions:
def setWebSession(session, userid):
	session['userid'] = userid

def unsetWebSession(session):
	session['userid'] = None

def authenticate(session):
	if not session.get('userid'):
		return False
	return True


# Other helper functions:
def getmaxid(table):
	query = f"SELECT MAX(Id{table}) FROM {table}"
	result = dbquery(query)
	if not result:
		return None
	return result[0][0]

def getcount(table):
	return getmaxid(table)

def error(message,redirect=""):
	return f"<script>alert(\'{message}\');window.location.assign(\'http://localhost:5000/{redirect}\')</script>"
