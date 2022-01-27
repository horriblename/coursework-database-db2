from flask import request, render_template
from datetime import datetime
from drive import Drive
import db_query_util
import connect

def viewDriveGet():
    '''
        The flask page to be served at /view_drive
    '''
    fid = request.args.get('fid', -1, int)
    print(fid)
    if fid == -1:
        return render_template('error.html', errmsg='Please provide fid')
    drive, driverEmail, takenSeats = fetchDriveInfo(fid) # type: ignore

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
        fid=fid
    )

def fetchDriveInfo(fid: int) -> tuple[Drive | None, str, int]:
    '''
        Query database for drive info
        return (Drive, driver_email, reserved_seats) or (None, '', 0) on error
    '''
    conn = connect.DBUtil().getExternalConnection()
    curs = conn.cursor()
    sql = '''
SELECT f.status, f.startort, f.zielort, f.fahrtdatumzeit, f.maxPlaetze, f.fahrtkosten, f.anbieter, f.transportmittel, cast(f.beschreibung AS varchar(50)), b.email, r.reserviert
FROM fahrt f 
LEFT JOIN benutzer b 
    ON b.bid=f.anbieter
LEFT JOIN (
    SELECT r.fahrt, SUM(r.anzPlaetze) AS reserviert
    FROM reservieren r
    WHERE r.fahrt=?
    GROUP BY r.fahrt
) r ON r.fahrt=f.fid
WHERE f.fid=?
'''
    print(sql)
    curs.execute(sql, (fid, fid))
    res = curs.fetchall()
    if len(res) == 0:
        return None, '', 0
    res = res[0]
    print("got row ",res)

    drive = Drive(
        status 	        = res[0],
        startort 	    = res[1],
        zielort 	    = res[2],
        fahrtdatumzeit  = datetime.strptime(res[3], '%Y-%m-%d %H:%M:%S'),
        maxPlaetze 	    = res[4],
        fahrtkosten 	= res[5],
        anbieter 	    = res[6],
        transportmittel = res[7],
        beschreibung 	= res[8]
    )
    freeSeats = res[10] if res[10] != None else 0

    conn.close()
    return drive, res[9], freeSeats

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
