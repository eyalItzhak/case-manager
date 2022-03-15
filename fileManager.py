import os
from werkzeug.utils import secure_filename

nameFileToIcon = {"docx": "bi bi-file-earmark-word", "rtf": "bi bi-file-earmark-word", "zip": "bi bi-file-earmark-zip",
                  "dir": "bi bi-folder", "empty": "bi bi-x-square-fill",
                  "rar": "bi bi-file-earmark-zip"}  # pic to dispaly


# Get the list of all files and directories


def changefolderName(oldName,newName,path):
    if os.chdir(path) and os.rename("oldName", "newName"):
        return True
    return False

def cheakIfdataBaseExsit(fileName, path):
    if (os.path.exists(fileName)):
        return True
    return False


def infoFromDirPath(path="C://Users//eyal//OneDrive//Desktop//sharon project//demoMainFiles//id-500 hit and run"):  # currect path is for testing  //retrun list of what inside the path
    try:
        dir_list = os.listdir(path)
        return dir_list
    except:
        return None


def fileNameAndTypePic(listOfFiles):  # get list of file ["name.rtf", "name.zip"] and return [["name-","bi bi-file-earmark-word"],[name," bi bi-file-earmark-zip"]]
    picList = []
    if listOfFiles == []:
        val = ["empty", "empty"]
        val[1] = nameFileToIcon.get(val[1])
        picList.append(val)
        return picList

    for elment in listOfFiles:
        val = elment.rsplit(".", 1)
        if (len(val) == 1):
            val.append("dir")
        val[0] = val[0] #+ "." + val[1]
        val[1] = nameFileToIcon.get(val[1])
        picList.append(val)
    return picList


def convertSingleTypePicToFileName(name):  # get "name bi bi-file somting... " return "name zip/rar/type"
    tempName = name.split(" , ", 1)
    tempName[1] = "." + [k for k, v in nameFileToIcon.items() if v == tempName[1]][0]
    return ''.join(tempName)


def runFile(path="C://Users//eyal//OneDrive//Desktop//sharon project//demoMainFiles//id-500 hit and run",
            offsetPath=''):  # currect path is for testing  //run file
    os.startfile(path + "//" + offsetPath)
    return


def creatDir(path, name):
    try:
        os.chdir(path)
        os.mkdir(name)
        return True
    except:
        return False


def pythonPath(userPath):
    if(userPath):
        return userPath.replace('/', '\\')
    else:
        return


def userPath(pythonPath):
    return pythonPath.replace('\\', '/')


def uploadFile(path, file):
    try:
        filename = secure_filename(file.filename)
        file.save(os.path.join(path, filename))
        return True
    except:
        return False


def chekIfDir(name):
    val = name.rsplit(".", 1)
    if val[1] == "dir":
        return True
    else:
        return False


def listOfCustomer(customer):
    return customer.query.all()
