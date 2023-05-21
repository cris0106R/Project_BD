from mysql import connector
from socket import gethostname
from datetime import date

# * Database connection details
database="NewProjectSchema"
if gethostname() == "Entropy":
    database = "bd_proj"
connection = connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",  # empty for Will /TODO Change if doesn't work
    database = database
    # for Will it's  was "bd_proj" For Georg it's "Project"             /This is for testing"testingFlask", change if shit fucks up
)

MAX_HOUR = 8

# * sql query wrapper
def dbquery(q, action="select"):
    result = []
    with connection.cursor() as cursor:
        cursor.execute(q)
        if action != "select":
            connection.commit()  # either update or insert
        else:
            rows = cursor.fetchall()
            if rows:
                for r in rows:
                    result.append(r)
                return result  # <-- result is an array, to access first row use result[0], to access first column value of first row use result[0][0]


# Reservation related helper functions:


def getReservationid(userid):
    query = f"SELECT IdReservation FROM Reservation WHERE IdUser = {userid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getReservationdate(reservationid):
    query = f"SELECT date FROM Reservation,Session WHERE reservation.IdSession = Session.IdSession AND IdReservation= {reservationid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]

#time=alloc_time
def getReservationtime(reservationid):
    query = f"SELECT time_alloc FROM Reservation WHERE IdReservation = {reservationid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]

def addReservation(sessionid, userid, alloctime):
    reservationid = getmaxid("Reservation")
    if reservationid == None:
        reservationid = 0
    else:
        reservationid += 1

    query = f"INSERT INTO Reservation (Reservation.IdReservation, Reservation.IdSession, Reservation.IdUser, Reservation.time_alloc) VALUES ({reservationid}, {sessionid}, {userid}, {alloctime})"
    dbquery(query, "INSERT")


def deleteReservation(reservationid):
    query = f"DELETE from Reservation WHERE IdReservation = {reservationid}"
    dbquery(query, "DELETE")

# Game related helper functions:


# * Get all game titles
def getGames():
    query = f"SELECT game_title FROM Game"
    result = dbquery(query)
    games = []

    for i in range(len(result)):
        games.append(result[i][0])
    return games


def getAllGamesInfo():
    query = f"SELECT * FROM Game"
    result = dbquery(query)
    games = []
    for i in range(len(result)):
        games.append(result[i])
    return games


def getGameid(game_title):
    game_title = game_title.replace("'", "''")
    query = f"SELECT IdGame FROM Game WHERE game_title = \'{game_title}\' "
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]

def getGametitle(gameid):
    gameid = gameid.replace("'", "''")
    query = f"SELECT game_title FROM Game WHERE IdGame = {gameid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getGamerating(gameid):
    query = f"SELECT user_rating FROM Game WHERE IdGame = {gameid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getGamecopyright(gameid):
    query = f"SELECT copyright FROM Game WHERE IdGame = {gameid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


# Room related helper functions:
def getRooms():
    query = f"SELECT room_name from Room"
    result = dbquery(query)
    rooms = []

    for i in range(len(result)):
        rooms.append(result[i][0])
    return rooms


def getRoomid(room_name):
    query = f"SELECT IdRoom FROM Room WHERE room_name = \'{room_name}\'"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getRoomname(roomid):
    query = f"SELECT room_name FROM Room WHERE IdRoom = {roomid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getRoomcapacity(roomid):
    maxcapacity = getRoomMaxcapacity(roomid)
    sessionid = getSessionid("Room", roomid)

    query = f"SELECT COUNT(DISTINCT(IdUser)) From Reservation WHERE IdSession = {sessionid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]

def getRoomMaxcapacity(roomid):
    query = f"SELECT room_capacity FROM Room WHERE IdRoom = {roomid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def isRoomfull(roomid):
    if getRoomMaxcapacity(roomid) == getRoomcapacity(roomid):
        return True
    return False


# User related helper functions:

def getUsers():
    query = f"SELECT name from User"
    result = dbquery(query)
    usernames = []

    for i in range(len(result)):
        usernames.append(result[i][0])
    return usernames


def getUserid(email):
    query = f"SELECT IdUser FROM User WHERE email = \'{email}\'"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getUsername(userid):
    query = f"SELECT name FROM User WHERE IdUser = {userid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getUseremail(userid):
    query = f"SELECT email FROM User WHERE IdUser = {userid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getUserBalance(userid):
    query = f"SELECT balance FROM User WHERE IdUser = {userid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getUserReservations(userid):
    query = f"select IdReservation, game_title, room_name, time_alloc from Reservation JOIN Session ON Reservation.IdSession = Session.IdSession JOIN Room ON Session.IdRoom = Room.IdRoom JOIN Game ON Session.IdGame = Game.IdGame WHERE IdUser = {userid};"
    print(query)
    result = dbquery(query)
    if result == None:
        return None
    return result

def getUsertime(userid):
    query = f"SELECT SUM(time_alloc) FROM Reservation WHERE IdUser = {userid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]

def getUsergames(userid):
    usergames = []
    query = f"SELECT IdSession FROM Reservation WHERE IdUser = {userid}"
    result = dbquery(query)
    if result == None:
        return None
    for i in range(len(result)):
        gameid = getSessiongameid(result[i][0])
        game = getGametitle(gameid)
        usergames.append(game)
    return usergames
    

def createAccount(name, email):
    maxid = getmaxid("User")
    userid = maxid + 1
    query = f"INSERT INTO User (User.IdUser, User.name, User.email, User.balance) VALUES ({userid}, \'{name}\', '\{email}\', 0);"
    dbquery(query, "INSERT")

def changeUseremail(userid, newemail):
    query = f"UPDATE User SET email = \'{newemail}\' WHERE IdUser = {userid}"
    dbquery(query, "UPDATE")


def changeUsername(userid, newname):
    query = f"UPDATE User SET name = \'{newname}\' WHERE IdUser = {userid}"
    dbquery(query, "UPDATE")


def addUserBalance(userid, amount):
    amount = getUserBalance(userid) + int(amount)
    query = f"UPDATE User SET balance = {amount} WHERE IdUser = {userid}"
    dbquery(query, "UPDATE")

def removeUserCost(userid,cost):
    total = getUserBalance(userid) - int(cost)
    query = f"UPDATE User SET balance = {total} WHERE IdUser = {userid}"
    dbquery(query, "UPDATE")


def verifyUsertime(userid, newtime):
    query = f"SELECT SUM(time_alloc) FROM Reservation WHERE IdUser = {userid}"
    result = dbquery(query)
    if result[0][0] == None:
        return None
    elif result[0][0] + int(newtime) >= MAX_HOUR:
        return False
    return True

# Game Session related helper functions:
def getSessionid(_type, _id):
    query = f"SELECT IdSession FROM Session WHERE Id{_type} = {_id}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]

def getSessiongameid(sessionid):
    query = f"SELECT IdGame FROM Session WHERE IdSession = {sessionid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]

def getSessionroomid(sessionid):
    query = f"select IdRoom FROM Session WHERE IdSession = {sessionid}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]

def newSession(gameid):
    gamesessionid = getmaxid("Session")
    if gamesessionid == None:  # if it's the first session to be created
        gamesessionid = 0
    else:
        gamesessionid += 1

    rand_roomids = __import__('random').sample(range(getmaxid("Room")), getmaxid("Room"))
    for i in rand_roomids:
        for j in getRooms():
            if i != getRoomid(j):
                query = f"INSERT INTO Session (Session.IdSession, Session.IdRoom, Session.IdGame, Session.date) VALUES ({gamesessionid}, {i}, {gameid}, CURDATE())"
                dbquery(query, "INSERT")
                return gamesessionid
    return None

# Web Session related helper functions:
def setWebSession(session, userid):
    session['userid'] = userid


def unsetWebSession(session):
    session['userid'] = None


def authenticate(session):
    if session.get('userid') == None:
        return False
    return True


# Other helper functions:
def getmaxid(table):
    query = f"SELECT MAX(Id{table}) FROM {table}"
    result = dbquery(query)
    if result == None:
        return None
    return result[0][0]


def getcount(table):
    return getmaxid(table)

def sanitize(input):
    if "'" in input:
        return input.replace("'", "\\'")
    return input

def getMaxhour():
    return MAX_HOUR

def error(message, redirect=""):
    return f"<script>alert(\'{message}\');window.location.assign(\'http://127.0.0.1:5000/{redirect}\')</script>"
