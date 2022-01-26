from flask import Flask, render_template
import user
import userStore
# import threading
import csv
import re

import page_view_main as viewMain
import page_new_drive as newDrive
import page_view_drive as viewDrive
import page_view_search as viewSearch


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

@app.route('/view_drive', methods=['GET'])
def viewDriveGet():
    return viewDrive.viewDriveGet()

@app.route('/new_rating', methods=['GET'])
def newRatingGet():
    return render_template('new_rating.html')

@app.route('/', methods=['GET'])
def index():
    return carSharer()

@app.route('/view_main', methods=['GET'])
def carSharer():
    return viewMain.carSharer()

@app.route('/view_search', methods=['GET'])
def carSearch():
    return viewSearch.carSearch()

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
    app.run(host='0.0.0.0', port=port, debug=True)
