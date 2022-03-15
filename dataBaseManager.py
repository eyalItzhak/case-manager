# to do -move function from main-flask

def returnCaseInfo(case, caseName):
    info = case.query.filter_by(caseName=caseName).first()
    if info:
        return info
    else:
        return None


def changeCaseInfo(db,case,oldCaseName,newCaseName,info):
    found_user = case.query.filter_by(caseName=oldCaseName).first()
    found_user.caseName = newCaseName
    found_user.info = info
    db.session.commit()

    return True

