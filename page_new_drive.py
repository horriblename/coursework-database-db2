from flask import request, render_template
from datetime import datetime
from werkzeug.utils import redirect
from drive import Drive
import driveStore
from typing import Any

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

