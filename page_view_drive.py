from flask import request, render_template
import driveStore

def viewDriveGet():
    '''
        The flask page to be served at /view_drive
    '''
    fid = request.args.get('fid', -1, int)
    print(fid)
    if fid == -1:
        return render_template('view_drive_not_found.html', errmsg='Please provide fid')
    drive = None
    try: 
        ds = driveStore.DriveStore()
        drive = ds.fetchDriveByFID(fid) # type: ignore
    except Exception as e:
        print(e)
        return render_template('view_drive_not_found.html', errmsg='DB error!')
    finally:
        ds.close() #type:ignore

    if drive is None:
        return render_template('view_drive_not_found.html', errmsg='The drive you are looking for does not exist')
    
    return render_template('view_drive.html', drive=drive)
