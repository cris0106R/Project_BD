from flask import Flask, jsonify, render_template, redirect, session, request
from utilities import *
from gameCenter import *

# * Default flask project (don't change)
app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/", methods=['GET'])
def homeTest():
    return render_template("index.html")
    #


# result = getGames(connection, cursor)
# return jsonify(result)


@app.route("/index", methods=['GET'])
# @cross_origin(origin='*', headers=['Content-Type']) # * Only uncomment if you know what you are doing. GL
def home():
    return render_template("index.html")


@app.route("/dashboard", methods=['GET'])
def dashboard():
    if not authenticate(session):
        message = "401 Unauthenticated"
        return error(message)
    
    return render_template("dashboard.html", username=getUsername(session['userid']))


@app.route("/profile", methods=['POST', 'GET'])
def profile():
    if not authenticate(session):
        message = "401 Unauthenticated"
        return error(message)
    return render_template("profile.html", username=getUsername(session['userid']), email = getUseremail(session['userid']), balance = getUserBalance(session['userid']))


@app.route("/login", methods=['POST', 'GET'])
def login():
    if authenticate(session):
        return redirect("/dashboard")
    return render_template("login.html")


#
@app.route("/games", methods=['GET'])
def viewGames():
    return render_template("games.html")

@app.route("/all-games", methods=['GET'])
def viewAllGames():
    return render_template("games.html")

@app.route("/reservation", methods=['GET', 'POST'])
def makeReservation():
    if not authenticate(session):
        message = "401 Unauthenticated"
        return error(message)
    return render_template("reservation.html", username=getUsername(session['userid']))


# *################################*#

# * API Pages -- User should usually not go on these sites#
@app.route("/api/login", methods=['POST'])
def dologin():
    email = sanitize(request.form.get('email'))
    userid = getUserid(email)

    if userid == None:
        message = "User does not exist!"
        return error(message, "login")

    setWebSession(session, userid)

    return redirect("/dashboard")

@app.route("/api/createAccount", methods=['POST'])
def doCreateAccount():
    name = sanitize(request.form.get('name'))
    email = sanitize(request.form.get('email'))

    createAccount(name, email)

    userid = getUserid(email)

    setWebSession(session, userid)
    return redirect("/login")

@app.route("/api/logout", methods=['GET'])
def dologout():
    unsetWebSession(session)
    return redirect("/login")


@app.route("/api/all-games", methods=['GET'])  # Accepting the methods ['GET'], ['POST', 'GET']
def games():
    return getAllGamesInfo()

@app.route("/api/<game>/price", methods=['GET'])
def getGamePrice(game):
    gameid = getGameid(game)
    result = [getGamecopyright(gameid)]
    return result

# return render_template("front.html") # * Renders the HTML page

@app.route("/api/topup", methods=['GET', 'POST'])
def topupBalance():
    if not authenticate(session):
        message = "401 Unauthenticated"
        return error(message)

    amount = sanitize(request.form.get('Amount'))
    userid = session['userid']

    addUserBalance(userid, amount)
    return redirect("/profile")


@app.route("/api/emailchange", methods=['GET', 'POST'])
def changeEmail():
    if not authenticate(session):
        message = "401 Unauthenticated"
        return error(message)

    userid = session['userid']
    newemail = sanitize(request.form.get('email-change'))
    changeUseremail(userid, newemail)
    return redirect("/profile")

@app.route("/api/view_reservations", methods=['GET', 'POST'])
def viewReservations():
    if not authenticate(session):
        message = "401 Unauthenticated"
        return error(message)

    userid = session['userid']
    return getUserReservations(userid)

@app.route("/api/new_reservation", methods=['GET', 'POST'])
def newReservation():
    if not authenticate(session):
        message = "401 Unauthenticated"
        return error(message)

    userid = session['userid']
    usertime = sanitize(request.form.get('time'))
    game = sanitize(request.form.get('game'))
    gameid = getGameid(game)    
   
    if game == "" or gameid == None:
        message = "Please select a valid game."
        return error(message, "reservation")
    elif usertime == "":
        message = "Please choose play duration."
        return error(message, "reservation")
    
    price = round(int(getGamecopyright(gameid)) * int(usertime) * 0.1)
     
    if verifyUsertime(userid, usertime) == False:
        message = f"You cannot exceed the {getMaxhour()} hours play time" 
        return error(message)

    if (price > getUserBalance(userid)):
        message = f"Your balance is too low"
        return error(message)
    print(getSessionid("Game", gameid))
    if getSessionid("Game", gameid) == None: 
        sessionid = newSession(gameid)
        if sessionid == None:
            message = "Error creating new session"
            return error(message)
        addReservation(sessionid, userid, usertime)
        removeUserCost(userid, price)
        return redirect("/dashboard")
    	
    elif isRoomfull(getSessionroomid(getSessionid("Game", gameid))) == True:
        message = "Room is full, please select another game!"
        return error(message)
 
    sessionid = getSessionid("Game", gameid)
    addReservation(sessionid, userid, usertime)
    removeUserCost(userid,price)
    return redirect("/dashboard")

@app.route("/api/delete_reservation", methods=['GET'])
def delete_Reservation():
    if not authenticate(session):
        message = "401 Unauthenticated"
        return error(message)
    
    userid = session['userid']
    reservationid = sanitize(request.args.get('id'))
    userReservations = getUserReservations(userid)
    game = sanitize(userReservations[0][1])
    gamePrice = getGamecopyright(getGameid(game))
    time = userReservations[0][3]
    cost = round(int(gamePrice) * int(time) * 0.1)


    deleteReservation(reservationid)
    addUserBalance(userid,cost)
    return redirect("/dashboard")

# *################################*#


# * Si le port 5000 ne marche pas, lancer sur port 8000
# if __name__ == "__main__":
#    app.run(port=8000, debug=True)


# * Running the app
app.run(debug=True)
