from flask import request, render_template
from datetime import datetime
import driveStore
from user import USER_ID
from drive import Drive
import connect

def viewDriveGet():
    '''
        The flask page to be served at /view_drive
    '''
    fid = request.args.get('fid', None, int)
    print(fid)
    if fid is None:
        return render_template('error.html', errmsg='Please provide fid', prevPage='/')
    drive, driverEmail, takenSeats = fetchDriveInfo(fid)

    if drive is None:
        return render_template('error.html', errmsg='The drive you are looking for does not exist', prevPage='/')

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
        fid=fid,
        iscreator=drive.getDriverBID() == USER_ID
    )

def newReservationPost():
    '''
        Handles new reservation requests
    '''
    fid = request.form.get('fid', None, int)
    reservationCount = request.form.get('reservationcount', 0, int)
    if fid is None:
        return render_template('error.html', errmsg='Missing fid?', prevPage='/')

    conn = connect.DBUtil().getExternalConnection()
    curs = conn.cursor()
    sql = '''
SELECT f.status, f.maxPlaetze, f.anbieter, r.reserviert, b.alreadyReserved
FROM fahrt f 
LEFT JOIN (
    SELECT r.fahrt, SUM(r.anzPlaetze) AS reserviert
    FROM reservieren r
    WHERE r.fahrt=?
    GROUP BY r.fahrt
) r ON r.fahrt=f.fid
LEFT JOIN (
    SELECT r.fahrt, COUNT(*) AS alreadyReserved
    FROM reservieren r
    WHERE r.fahrt=? AND r.kunde=?
    GROUP BY r.fahrt
) b ON b.fahrt=f.fid
WHERE f.fid=?
'''
    print(sql)
    curs.execute(sql, (fid, fid, USER_ID, fid))
    res = curs.fetchall()
    print(res)

    if len(res) == 0:
        return render_template('error.html', errmsg='The drive you are looking for does not exist', prevPage=f'/view_drive?fid={fid}')

    status, maxSeats, driverBID, takenSeats, userReserved = res[0]

    if status != 'offen':
        return render_template('error.html', errmsg='The drive you are looking for is closed', prevPage=f'/view_drive?fid={fid}')

    freeSeats=maxSeats - takenSeats
    if reservationCount < 1 or reservationCount > 2 or reservationCount > freeSeats :
        return render_template('error.html', errmsg='Invalid Reservation count', prevPage=f'/view_drive?fid={fid}')

    if driverBID == USER_ID:
        return render_template('error.html', errmsg='You may not reserve your own drive!', prevPage=f'/view_drive?fid={fid}')

    if userReserved is not None:
        return render_template('error.html', errmsg='You have already made a reservation!', prevPage=f'/view_drive?fid={fid}')

    try:
        ds = driveStore.DriveStore()
        ds.addReservation(USER_ID, fid, reservationCount)
        ds.completion()
    except Exception as e:
        print(e)
        return render_template('error.html', errmsg='DB error!', prevPage=f'/view_drive?fid={fid}')
    finally:
        ds.close() # type: ignore

    if reservationCount == freeSeats:
        curs = connect.DBUtil().getExternalConnection().cursor()
        curs.execute('SELECT status FROM fahrt WHERE fid=?', (fid,))
        status = curs.fetchall()
        curs.close()
        if len(status) == 0:
            return render_template('info.html', msg=f'Successfully reserved {reservationCount} seats, but could not find drive info', redir=f'/view_drive?fid={fid}')
        status = status[0][0]

        if status == 'offen':
            return render_template('info.html', msg=f'Successfully reserved {reservationCount} seats, but current drive status "open" is incorrect', redir=f'/view_drive?fid={fid}')
        else:
            return render_template('info.html', msg=f'Successfully reserved {reservationCount} seats, drive status set to "closed"', redir=f'/view_drive?fid={fid}')

    return render_template('info.html', msg=f'Successfully reserved {reservationCount} seats.', redir=f'/view_drive?fid={fid}')

def deleteDrivePost():
    fid = request.form.get("fid", None, int)
    if fid is None:
        return render_template('error.html', errmsg='Missing fid When Deleting drive!', prevPage='/')

    curs = connect.DBUtil().getExternalConnection().cursor()
    curs.execute('SELECT anbieter from fahrt WHERE fid=?', (fid,))
    driver = curs.fetchall()
    curs.close()

    if len(driver) == 0:
        return render_template('error.html', errmsg='Drive not found in DB!', prevPage='/')
    
    driver = driver[0][0]

    if driver != USER_ID:
        return render_template('error.html', errmsg="You may not delete other user's drive!", prevPage=f'/view_drive?fid={fid}')

    try:
        ds = driveStore.DriveStore()
        ds.deleteDrive(USER_ID, fid)
        ds.completion()
    except Exception as e:
        print(e)
        return render_template('error.html', errmsg='DB error!', prevPage=f'/view_drive?fid={fid}')
    finally:
        ds.close() # type: ignore

    return render_template('info.html', msg=f'Drive successfully deleted.', redir='/')

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
    sql = '''
SELECT b.email, cast(be.textnachricht AS varchar(100)), be.rating
FROM schreiben s
    LEFT JOIN bewertung be
        ON be.beid=s.bewertung
    LEFT JOIN benutzer b
        ON b.bid=s.benutzer
WHERE s.fahrt=?
ORDER BY be.erstellungsdatum DESC
    '''
    curs = connect.DBUtil().getExternalConnection().cursor()
    curs.execute(sql, (fid,))
    res = curs.fetchall()
    curs.close()

    return res
