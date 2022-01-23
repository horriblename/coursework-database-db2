from flask import request, render_template
from datetime import datetime
from werkzeug.utils import redirect
from drive import Drive
import driveStore

def newDrivePost():
    '''
        Handle POST request on '/new_drive'
    '''
    startort        = request.form.get('depart', type=str, default=None)
    zielort         = request.form.get('destination', type=str, default=None)
    maxPlaetze      = request.form.get('maxcap', type=int, default=None)
    fahrtkosten     = request.form.get('cost', type=float, default=None)
    transportmittel = request.form.get('vehicletype', type=str, default='')
    datestr         = request.form.get('drivedatetime', type=str, default=None) 
    beschreibung    = request.form.get('description', type=str, default='')

    if startort is None or zielort is None or \
            maxPlaetze is None or fahrtkosten is None or \
            transportmittel not in  ('Auto', 'Bus', 'Kleintransporter') \
            or datestr is None:
        return render_template('new_drive.html')

    fahrtdatumzeit  = datetime.strptime(str(datestr), '%Y-%m-%dT%H:%M')
        
    try:
        ds = driveStore.DriveStore()
        driveToAdd = Drive(
            startort=startort,
            zielort=zielort,
            maxPlaetze=maxPlaetze,
            fahrtkosten=fahrtkosten,
            transportmittel=transportmittel,
            fahrtdatumzeit=fahrtdatumzeit,
            beschreibung=beschreibung,
            anbieter=1, # TODO
            status='offen'
        )
        ds.addDrive(driveToAdd)
        ds.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        ds.close() # type: ignore

    # TODO query FID and redirect to view_drive
    return redirect('/')

