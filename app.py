from datetime import datetime
from flask import Flask, request, render_template
from werkzeug.utils import redirect
from drive import Drive
import driveStore
import user
import connect
import userStore
# import threading
import csv
import re
from typing import Any, cast


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
    requiredParams   = ('depart', 'destination', 'maxCap', 'cost', 'vehicleType', 'driveDateTime')
    param:dict[str, Any] = {'driverBID': 1, 'status': 'offen'} # TODO driverBID

    param['depart']         = request.form.get('depart', type=str)
    param['destination']    = request.form.get('destination', type=str)
    param['maxCap']         = request.form.get('maxcap', type=int)
    param['cost']           = request.form.get('cost', type=float)
    param['vehicleType']    = request.form.get('vehicletype', type=str)
    datestr = request.form.get('drivedatetime', type=str) 
    if datestr is None or datestr == '':  # I think it returns '' and not None
        param['driveDateTime']  = None
    else:    
        param['driveDateTime']  = datetime.strptime(str(datestr), '%Y-%m-%dT%H:%M')
    param['description']    = str(request.form.get('description', type=str))

    for r in requiredParams:
        if param[r] == None:
            print("Got an incomplete form: empty field ", r)
            return render_template('new_drive.html')
        
    ds: driveStore.DriveStore
    try:
        ds = driveStore.DriveStore()
        print("new Drive was passed the parameters ", param)
        driveToAdd = Drive(**param)
        ds.addDrive(driveToAdd)
        ds.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        ds.close() # type: ignore

    # TODO query FID and redirect to view_drive
    return redirect('/')

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
    m: re.Match[str] = cast(re.Match[str], re.match(r"([a-z]+)([0-9]+)", config["username"], re.I))
    port = int("9" + m.groups()[1])
    app.run(host='127.0.0.1', port=port, debug=True)
