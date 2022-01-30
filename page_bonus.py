from flask import render_template
import connect

def bonusGet():

    curs = connect.DBUtil().getExternalConnection().cursor()
    sql = """
SELECT r.anbieter, b.email, r.rating
FROM (
    SELECT f.anbieter, AVG(CAST(be.rating AS DECIMAL(5,2))) AS rating
    FROM schreiben s
        LEFT JOIN fahrt f ON s.fahrt = f.fid
        LEFT JOIN bewertung be ON s.bewertung = be.beid
    GROUP BY f.anbieter
) r LEFT JOIN benutzer b ON b.bid = r.anbieter
WHERE r.rating = (SELECT MAX(r.rating) FROM (
    SELECT f.anbieter, AVG(CAST(be.rating AS DECIMAL(5,2))) AS rating
    FROM schreiben s
        LEFT JOIN fahrt f ON s.fahrt = f.fid
        LEFT JOIN bewertung be ON s.bewertung = be.beid
    GROUP BY f.anbieter
) r )
FETCH FIRST ROWS ONLY
    """
    curs.execute(sql)
    res = curs.fetchall()
    assert len(res) > 0, "DB error!"
    res = res[0]
    bid = res[0]

    sql = """
SELECT f.fid, f.transportmittel, f.startort, f.zielort
FROM (
    SELECT s.fahrt, AVG(be.rating) AS rating

    FROM schreiben s
        LEFT JOIN fahrt f ON f.fid = s.fahrt
        LEFT JOIN bewertung be ON be.beid = s.bewertung
    WHERE f.anbieter = ?
    GROUP BY s.fahrt
) s LEFT JOIN fahrt f ON f.fid = s.fahrt
ORDER BY s.rating DESC
    """
    curs.execute(sql, (bid,))
    availableDrives = curs.fetchall()
    print('available drives: ', availableDrives)

    return render_template('bonus.html', email=res[1], ratingAvg=round(res[2], 2), availableDrives=availableDrives)
