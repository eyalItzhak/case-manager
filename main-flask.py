from flask import Flask, request, render_template, redirect, url_for, session, flash
import fileManager
import dataBaseManager
from models import db, users, customer, case
import os

user_home_path = os.path.expanduser("~/")
basePath = os.path.join(user_home_path, "OneDrive", "Desktop", "sharon project", "demoMainFiles")
path = os.path.join(user_home_path, "OneDrive", "Desktop", "sharon project", "demoMainFiles")

# ************************************
app = Flask(__name__)  # start the flask file
app.secret_key = "hello"
# ************************************

dataBaseManager.init_DB(app)

@app.route('/', methods=["POST", "GET"])
def home():
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

        if dataBaseManager.addNewUser(user,password,email):
            flash("user already exist")
            return render_template("register.html")
        else:
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
    if not dataBaseManager.addCustomer(firstName,lastName,tz,email,password):
        flash("user already exist")
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["userName"]
        password = request.form["password"]
        found_user = dataBaseManager.verificationUser(user,password) #retrun the user if found
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

            dataBaseManager.updateUserInfo(email,workSpace,password,user)
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
    global path # why?
    global basePath
    if basePath == path:
        caseName = request.form["cname"]
        customerTz = request.form["custTz"]
        if(fileManager.creatDir(path, caseName)):
            dataBaseManager.creatCase(customerTz,caseName,'')
        return redirect(url_for("home"))
    else:
        caseName = request.form["cname"]
        fileManager.creatDir(path, caseName)
        return redirect(url_for("case"))




@app.route("/deleteFile",methods=['GET', 'POST'])
def delete():
    delete_name = request.form["userChose"]
    if path == basePath:
        dataBaseManager.removeCase(delete_name)

    fileManager.deleteFile(path,delete_name)
    return redirect(url_for("home"))



@app.route("/editFile", methods=['GET', 'POST'])
def editFile():
    userFileChose=request.form["userChose"]
    case = dataBaseManager.returnCaseInfo(userFileChose)
    return render_template("caseInfo.html", caseName=case.caseName, info=case.info)


@app.route("/saveEditChanges", methods=['GET', 'POST'])
def saveEditChanges():
    info=request.form["info"]
    newNameCase=request.form["newNameCase"]
    oldNameCase=request.form["oldNameCase"]
    dataBaseManager.changeCaseInfo(oldNameCase,newNameCase,info)
   # fileManager.changefolderName(oldNameCase,newNameCase,path) #need to fix
    return redirect(url_for("home"))






if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
