

import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {
    'apiKey': "AIzaSyDiIbGGFUgVBPy9UzYCQETw6qjJf2c85-k",
    'authDomain': "hackactive-a24d2.firebaseapp.com",
    'projectId': "hackactive-a24d2",
    'storageBucket': "hackactive-a24d2.appspot.com",
    'messagingSenderId': "390742365637",
    'appId': "1:390742365637:web:38fa8d9e3a5928d600e7ac",
    'measurementId': "G-ZYRZQ6GGDJ",
    'databaseURL': "https://hackactive-a24d2-default-rtdb.firebaseio.com/"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/3d")
def three_d():
    return render_template("3d.html")

@app.route("/head")
def head():
    return render_template("head.html")

@app.route("/leg")
def leg():
    return render_template("leg.html")

@app.route("/chest")
def chest():
    return render_template("chest.html")

@app.route("/stomach")
def stomach():
    return render_template("stomach.html")

#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome2.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run()
