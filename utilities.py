# Get all the games
def getGames(gameid, option="", getall=False):
        if getall:
                query = f"SELECT {option} from Game"
        else:
                query = f"SELECT {option} FROM Game WHERE IdGame=\'{gameid}\'"
        return dbquery(query)

def getUsers(userid, option="", getall=False):
        if getall:
                query = f"SELECT {option} from User"
        else:
                query = f"SELECT {option} FROM User WHERE IdUser = \'{userid}\'"

        return dbquery(query)

def getUserid(email):
        return dbquery(f"SELECT IdUser FROM User WHERE email = \'{email}\'")[0]

def authenticate(session):
        if not session.get('userid'):
                return False
        return True

def error(message):
        return f"<script>alert(\'{message}\');window.location.assign(\'http://localhost:5000/\')</script>"
