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
# @cross_origin(origin='*', headers=['Content-Type']) # * Only uncomment if you know what you are doing. If you need this..then you're fucked. GL
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
    return render_template("login.html")


#
@app.route("/games", methods=['GET'])
def viewGames():
    return render_template("games.html")


@app.route("/all-games", methods=['GET'])
def viewAllGames():
    return render_template("games.html")


# *################################*#

# * API Pages -- User should usually not go on these sites#
@app.route("/api/login", methods=['POST'])
def dologin():
    email = request.form.get('email')
    userid = getUserid(email)

    if not userid:
        message = "User does not exist!"
        return error(message, "login")

    setWebSession(session, userid)

    return redirect("/dashboard")


@app.route("/api/logout", methods=['GET'])
def dologout():
    unsetWebSession(session)
    return redirect("/login")


@app.route("/api/all-games", methods=['GET'])  # Accepting the methods ['GET'], ['POST', 'GET']
def games():

    return getAllGamesInfo()
    #result = getAllGames(connection, cursor)
    #return jsonify(result)


# return render_template("front.html") # * Renders the HTML page

# TODO Check if this route is needed
@app.route("/api/<user>/infos", methods=['GET'])
def user_infos(user):
    if not authenticate(session):
        message = "401 Unauthenticated"
        return error(message)
    return ""

@app.route("/api/topup", methods=['GET', 'POST'])
def topupBalance():
    if not authenticate(session):
        message = "401 Unaunthenticated"
        return error(message)

    amount = request.form.get('Amount')
    userid = session['userid']

    addUserBalance(userid, amount)
    return redirect("/profile")

@app.route("/api/emailchange", methods=['GET', 'POST'])
def changeEmail():
    if not authenticate(session):
        message = "401 Unaunthenticated"
        return error(message)

    userid = session['userid']
    newemail = request.form.get('email-change')
    changeUseremail(userid, newemail)
    return redirect("/profile")




# *################################*#


# * Si le port 5000 ne marche pas, lancer sur port 8000
# if __name__ == "__main__":
#    app.run(port=8000, debug=True)


# * Running the app
app.run(debug=True)
