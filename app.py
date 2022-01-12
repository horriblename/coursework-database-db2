from flask import Flask, render_template
import user
import connect
import userStore
# import threading
import csv
import re

import page_new_drive as newDrive


app = Flask(__name__, template_folder='template')

userList = []
userList.append(user.User("Bill", "Gates"))
userList.append(user.User("Steve", "Jobs"))
userList.append(user.User("Larry", "Page"))
userList.append(user.User("Sergey", "Brin"))
userList.append(user.User("Larry", "Ellison"))

def csv_reader(path):
    with open(path, "r") as csvfile:
        tmp = {}
        reader = csv.reader(csvfile, delimiter='=')
        for line in reader:
            tmp[line[0]] = line[1]
    return tmp

config = csv_reader("properties.settings")

@app.route('/hello', methods=['GET'])
def hello():
    return render_template('hello.html', users=userList)


@app.route('/new_drive', methods=['GET'])
def newDriveGet():
    return render_template('new_drive.html')

@app.route('/new_drive', methods=['POST'])
def newDrivePost():
    return newDrive.newDrivePost()

@app.route('/', methods=['GET'])
def index():
    return carShare()

@app.route('/view_main', methods=['GET'])
def carShare():

    db2exists = ''
    try:
        dbExists = connect.DBUtil().checkDatabaseExistsExternal()
        if dbExists:
            db2exists = 'vorhanden! Supi!'
        else:
            db2exists = 'nicht vorhanden :-('
    except Exception as e:
        print(e)

    return render_template('view_main.html', db2exists=db2exists)

@app.route('/addUser', methods=['GET'])
def addUser():
    try:
        userSt = userStore.UserStore()
        userToAdd = user.User("Max", "Mustermann")
        userSt.addUser(userToAdd)
        userSt.completion()

        # ...
        # mach noch mehr!
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        userSt.close() # type: ignore


if __name__ == "__main__": 
    port = int("9" + re.match(r"([a-z]+)([0-9]+)", config["username"], re.I).groups()[1]) # type: ignore
    app.run(host='127.0.0.1', port=port, debug=True)
