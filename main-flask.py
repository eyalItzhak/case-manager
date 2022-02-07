from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import fileManager
from werkzeug.utils import secure_filename
from models import db, users, customer, case
import os

user_home_path = os.path.expanduser("~/")
basePath = os.path.join(user_home_path, "OneDrive", "Desktop", "sharon project", "demoMainFiles")
path = os.path.join(user_home_path, "OneDrive", "Desktop", "sharon project", "demoMainFiles")

# ************************************
app = Flask(__name__)  # start the flask file
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ************************************
# ************************************

# Init the db from an external file
db.app = app
db.init_app(app)


@app.route('/', methods=["POST", "GET"])
def home():
    #  path=basePath
    if "user" in session:
        global path
        global basePath
        basePath = fileManager.pythonPath(session["workSpace"])
        path = basePath
        if request.method == "GET":
            dirToDisplay = fileManager.infoFromDirPath(path)
            if (dirToDisplay == None):
                flash("please select valid path")
                return redirect(url_for("user"))
            piclist = fileManager.fileNameAndTypePic(dirToDisplay)
            listofCustomer = fileManager.listOfCustomer(customer)

            return render_template('index.html', dirInfo=piclist, listofCustomer=listofCustomer)
        else:  # post
            userChose = request.form["userChose"]

            nameOnly = userChose.split(".")
            path = path + "//" + nameOnly[0]
            return redirect(url_for("case"))
    else:
        flash("please log in")
        return redirect(url_for("login"))


@app.route('/case', methods=["POST", "GET"])
def case():
    global path
    if request.method == "GET":
        dirToDisplay = fileManager.infoFromDirPath(path)
        piclist = fileManager.fileNameAndTypePic(dirToDisplay)
        return render_template('case.html', dirInfo=piclist)
    else:
        userChose = request.form["userChose"]
        if (fileManager.chekIfDir(userChose) == True):
            nameOnly = userChose.split(".")
            path = path + "//" + nameOnly[0]
        else:
            fileManager.runFile(path, userChose)
    dirToDisplay = fileManager.infoFromDirPath(path)
    piclist = fileManager.fileNameAndTypePic(dirToDisplay)
    return render_template('case.html', dirInfo=piclist)


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "GET":
        if "user" in session:
            flash("alrady login")
            return redirect(url_for("user"))
        return render_template("register.html")
    else:
        user = request.form["userName"]
        password = request.form["password"]
        email = request.form["email"]
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            flash("user already exist")
            return render_template("register.html")
        else:
            usr = users(user, password, email, "")
            db.session.add(usr)
            db.session.commit()
            session.permanent = True
            session["user"] = user
            session["email"] = email
            session["password"] = password
            session["workSpace"] = ""
            flash("success to register,login successful!")
            return redirect(url_for("user"))


@app.route("/addCustomer", methods=['POST'])
def AddCustomer():
    firstName = request.form["Cfname"]
    lastName = request.form["Clname"]
    tz = request.form["cId"]
    email = request.form["cEmail"]
    password = request.form["cPhone"]
    found_user = customer.query.filter_by(tz=tz).first()
    if found_user:
        flash("user already exist")
        return redirect(url_for("home"))
    else:
        cust = customer(firstName, lastName, email, password, tz)
        db.session.add(cust)
        db.session.commit()
        return redirect(url_for("home"))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["userName"]
        password = request.form["password"]
        found_user = users.query.filter_by(name=user, password=password).first()
        if found_user:
            session["user"] = user
            session["password"] = password
            session["email"] = found_user.email
            session["workSpace"] = found_user.workSpace
            flash("login successful!")
            return redirect(url_for("home"))
        else:
            flash("password or username is incorrect!")
            return render_template("login.html")
    else:
        if "user" in session:
            # flash("already login")
            return redirect(url_for("home"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":

            email = request.form["email"]
            session["email"] = email

            workSpace = request.form["workSpace"]
            session["workSpace"] = workSpace

            password = request.form["password"]
            session["password"] = password

            user = request.form["user"]
            session["user"] = user

            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            found_user.workSpace = workSpace
            found_user.user = user
            found_user.password = password

            db.session.commit()
            flash("data saved!")
        else:
            email = session["email"]
            workSpace = session["workSpace"]
            password = session["password"]
            user = session["user"]

        return render_template("user.html", email=email, workSpace=workSpace, user=user, password=password)
    else:
        flash("you are not log in!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if ("user" in session):
        user = session["user"]
        flash(f"you have been logged out, {user}", "info")
        session.pop("user", None)
        session.pop("email", None)
        session.pop("password", None)
        return redirect(url_for("login"))
    else:
        flash("you have already log out")
        return redirect(url_for("login"))


@app.route("/backword", methods=['GET', 'POST'])
def backword():
    global path
    global basePath
    path = path.rsplit('//', 1)[0]
    if path <= basePath:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("case"))


@app.route("/uploadFile", methods=['GET', 'POST'])
def uploadFile():
    global path
    file = request.files["file"]
    fileManager.uploadFile(path, file)
    return redirect(url_for("case"))


@app.route('/createFile', methods=['GET', 'POST'])  # add cases
def createFile():
    from models import case #cheak why
    global path
    global basePath
    if basePath == path:
        # CustomerFirstName = request.form["fname"]
        # CustomerLastName = request.form["lname"]

        caseName = request.form["cname"]
        customerTz = request.form["custTz"]


        if(fileManager.creatDir(path, caseName)):
            case=case(customerTz,caseName)
            db.session.add(case)
            db.session.commit()

        return redirect(url_for("home"))
    else:
        caseName = request.form["cname"]
        fileManager.creatDir(path, caseName)
        return redirect(url_for("case"))


@app.route('/test')
def test():
    return render_template('new.html')


@app.route("/deleteFile")
def delete():
    return  # to do


@app.route("/showInfo")
def fileInfo():
    return  # to do


@app.route("/editFile")
def editFile():
    return  # to do


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
