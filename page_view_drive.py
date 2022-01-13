from flask import request, render_template
import driveStore

def viewDriveGet():
    '''
        The flask page to be served at /view_drive
    '''
    fid = request.args.get('fid', int)
    print(fid)
    if fid is None:
        return "Please provide fid"
    drive = None
    try: 
        ds = driveStore.DriveStore()
        drive = ds.fetchDriveByFID(fid) # type: ignore
    except Exception as e:
        print(e)
        return "Could not fetch drive info."
    finally:
        ds.close() #type:ignore

    if drive is None:
        ... #TODO
    
    return render_template('view_drive.html', drive=drive)
