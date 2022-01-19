from flask import request, render_template
import driveStore
import db_query_util

def viewDriveGet():
    '''
        The flask page to be served at /view_drive
    '''
    fid = request.args.get('fid', -1, int)
    print(fid)
    if fid == -1:
        return render_template('error.html', errmsg='Please provide fid')
    drive = None
    try: 
        ds = driveStore.DriveStore()
        drive, driverEmail, takenSeats = ds.fetchDriveInfo(fid) # type: ignore
    except Exception as e:
        print(e)
        return render_template('error.html', errmsg='DB error!')
    finally:
        ds.close() #type:ignore

    if drive is None:
        return render_template('error.html', errmsg='The drive you are looking for does not exist')

    ratings = listRatings(fid)
    ratingAvg: str | float = '-'
    if len(ratings) > 0:
        ratingAvg = round(sum(r[2] for r in ratings) / len(ratings), 2)


    if drive.status == 'offen': status = 'open'
    elif drive.status == 'geschlossen': status = 'closed'
    else: status = ''

    return render_template('view_drive.html', 
        drive=drive, 
        driverEmail=driverEmail,
        freeSeats=drive.getMaxCap() - takenSeats,
        status=status,
        ratings=ratings,
        ratingAvg=ratingAvg,
    )

def listRatings(fid: int) -> list[tuple]:
    '''
        Query the database for a list of ratings given a drive's FID
        param fid
        return list of tuples [(email:str, comment:str, rating:int), ...]
    '''
    # TODO add truncate symbol?
    # TODO check character limit?
    sql = f'''
SELECT b.email, cast(be.textnachricht AS varchar(100)), be.rating
FROM schreiben s
    LEFT JOIN bewertung be
        ON be.beid=s.bewertung
    LEFT JOIN benutzer b
        ON b.bid=s.benutzer
WHERE s.fahrt={fid}
    '''
    res = db_query_util.customQueryDB(sql)
    print(res)
    if res is None: return [] # TODO throw error?
    return list(res)
