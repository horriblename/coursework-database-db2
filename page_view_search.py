from flask import render_template, request
import connect

def carSearch():
    conn = connect.DBUtil().getExternalConnection()
    start = request.args.get('start', None, str)
    destination = request.args.get('destination', None, str)
    fromDate = request.args.get('fromdate', None, str)

    if start is None or destination is None or fromDate is None:
        return render_template('view_search.html', totalfahrt=0)

    fahrtType = []
    fahrtStart = []
    fahrtEnd = []
    fahrtCost = []
    fahrtId = []
    curs = conn.cursor()
    sql = "SELECT transportmittel, startort, zielort, fahrtkosten, fid FROM fahrt WHERE LCASE(startort) LIKE LCASE('%%%s%%') AND LCASE(zielort) LIKE LCASE('%%%s%%') AND fahrtdatumzeit >= '%s' AND status='offen' "
    curs.execute(sql % (start, destination, fromDate))
    data = curs.fetchall()
    for row in data:
        fahrtType.append(row[0])
        fahrtStart.append(row[1])
        fahrtEnd.append(row[2])
        fahrtCost.append(row[3])
        fahrtId.append(row[4])
    totalfahrt = len(fahrtStart)
    return render_template('view_search.html', fahrtType=fahrtType, fahrtStart=fahrtStart, fahrtEnd=fahrtEnd,
                           fahrtCost=fahrtCost, fahrtId=fahrtId, totalfahrt=totalfahrt)
