from mysql import connector

connection = connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root", #empty for Will /TODO Change if doesn't work
    database="Project"  # for Will it's  was "bd_proj" For Georg it's "Project"             /This is for testing"testingFlask", change if shit fucks up
)

cursor = connection.cursor()



# Get all the games
def getAllGames(conn, curs):
    mysql_query = """
                SELECT * 
                FROM GAME
    """

    curs.execute(mysql_query)  # execution de la requete
    games = curs.fetchall()  # renvoie des resulats

    result = {} #TODO Change json data (vr yes or no)

    result["data"] = []  # creation de la clé et de la liste qui va contenur chaque film. Il faut creer cette liste, car il y a plusieurs films

    for game in games:
        dico = {}  # dictionnaire
        dico["id"] = game[0]
        dico["game_title"] = game[1]
        dico["user_rating"] = game[2]
        dico["copyright"] = game[3]

        result["data"].append(dico)

    return result


def getUser(conn, curs, user):
    mysql_query = """
    SELECT IdUser FROM User WHERE name=%s
    """
    curs.execute(mysql_query, ((user,)))
    user = curs.fetchall
    result = {}

