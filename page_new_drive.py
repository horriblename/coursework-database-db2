from flask import request, render_template
from datetime import datetime
from werkzeug.utils import redirect
from drive import Drive
import driveStore
from typing import Any

def newDrivePost():
    '''
        Handle POST request on '/new_drive'
    '''
    requiredParams = ('startort', 'zielort', 'maxPlaetze', 'fahrtkosten', 'transportmittel', 'fahrtdatumzeit')
    param:dict[str, Any] = {'anbieter': 1, 'status': 'offen'} # TODO anbieter

    param['startort']       = request.form.get('depart', type=str)
    param['zielort']        = request.form.get('destination', type=str)
    param['maxPlaetze']     = request.form.get('maxcap', type=int)
    param['fahrtkosten']    = request.form.get('cost', type=float)
    param['transportmittel']= request.form.get('vehicletype', type=str)
    datestr = request.form.get('drivedatetime', '', type=str) 
    if datestr == '':
        param['fahrtdatumzeit']  = None
    else:    
        param['fahrtdatumzeit']  = datetime.strptime(str(datestr), '%Y-%m-%dT%H:%M')
    param['beschreibung'] = request.form.get('description', '', type=str)

    # TODO input assertions: see pg.14 of the manual 
    for r in requiredParams:
        if param[r] is None:
            print("Got an incomplete form: empty field ", r)
            return render_template('new_drive.html')
        
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

