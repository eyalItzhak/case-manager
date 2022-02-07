from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    _id = db.Column("id", db.Integer,primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password=db.Column("password", db.String(100))
    workSpace=db.Column("workSpace",db.String(1000))

    def __init__(self, name, password, email, workspace):
        self.name = name
        self.password=password
        self.email = email
        self.workspace=workspace

class customer(db.Model):
      _id=db.Column("id", db.Integer,primary_key=True)
      fName = db.Column("fname", db.String(100))
      lName = db.Column("lname", db.String(100))
      email = db.Column("email", db.String(100))
      phone=db.Column("phone", db.String(100))
      tz=db.Column("tz", db.String(100),unique=True)

      def __init__(self, fName,lName,email, phone, tz):
          self.fName = fName
          self.lName = lName
          self.email = email
          self.phone = phone
          self.tz = tz


class case(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    Tz = db.Column("Tz", db.String(100), unique=True)
    caseName = db.Column("caseName", db.String(100), unique=True)

    def __init__(self,Tz,CaseName):
        self.Tz = Tz
        self.caseName = CaseName