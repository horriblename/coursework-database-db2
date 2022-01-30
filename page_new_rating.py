from flask import render_template, request
from werkzeug.utils import redirect
import driveStore
import connect
from user import USER_ID

def newRatingGet():
    fid = request.args.get('fid', None, int)
    if fid is None:
        return render_template('error.html', errmsg='Missing field fid', prevPage='/')
    return render_template('new_rating.html', fid=fid)


def newRatingPost():
    conn = connect.DBUtil().getExternalConnection()
    fid = request.args.get('fid', default=None, type=int)
    ratingtext = request.form.get('comment', default=None, type=str)
    rating = request.form.get('rating', default=0, type=int)
    if fid is None or ratingtext is None or rating < 1 or rating > 5:
        return render_template('error.html', errmsg='Your input is incomplete.')

    driveId = []
    curs = conn.cursor()
    sql = "SELECT fahrt FROM schreiben WHERE benutzer=1 AND fahrt=?"
    curs.execute(sql, (fid,))
    data = curs.fetchall()
    for row in data:
        driveId.append(row[0])
    if len(data) > 0:
        return render_template('error.html', errmsg='You have already rated this drive.')

    try:
        ds = driveStore.DriveStore()
        ds.addRating(USER_ID, fid, ratingtext, rating)
        ds.completion()
    except Exception as e:
        print(e)
        return render_template('error.html', errmsg='DB error!', prevPage=f'/view_drive?fid={fid}')
    finally:
        ds.close() # type: ignore

    return redirect(f'/view_drive?fid={fid}')
