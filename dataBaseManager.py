# to do -move function from main-flask

from models import db, users, customer, case
from sqlalchemy import delete

def init_DB(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    return True

def removeCase(caseName):
    info = case.query.filter_by(caseName=caseName).delete()
    db.session.commit()
    return True

def returnCaseInfo(caseName):
    info = case.query.filter_by(caseName=caseName).first()
    if info:
        return info
    else:
        return None


def changeCaseInfo(oldCaseName,newCaseName,info):
    found_case = case.query.filter_by(caseName=oldCaseName).first()
    found_case.caseName = newCaseName
    found_case.info = info
    db.session.commit()
    return True


def addNewUser(user,password,email):
    found_user = users.query.filter_by(name=user).first()
    if found_user:
        return True
    else:
        usr = users(user, password, email, "")
        db.session.add(usr)
        db.session.commit()
        return False

def verificationUser(name,password): #return user if found
    return users.query.filter_by(name=name, password=password).first()

def updateUserInfo(email,workSpace,password,user):
    try:
        found_user = users.query.filter_by(name=user).first()
        found_user.email = email
        found_user.workSpace = workSpace
        found_user.user = user
        found_user.password = password
        db.session.commit()
        return True
    except:
        return False

def addCustomer(firstName,lastName,tz,email,password):
    found_user = customer.query.filter_by(tz=tz).first()
    if found_user:
        return False
    else:
        cust = customer(firstName, lastName, email, password, tz)
        db.session.add(cust)
        db.session.commit()
        return True

def creatCase(customerTz,caseName,info):
    try:
        userCase = case(customerTz, caseName, info)
        db.session.add(userCase)
        db.session.commit()
        return True
    except:
        return False



