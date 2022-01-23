from flask import render_template
import connect

def carSearch():
    conn = connect.DBUtil().getExternalConnection()

    #input from user value1, value2, value3 to be initialized

    fahrtType = []
    fahrtStart = []
    fahrtEnd = []
    fahrtCost = []
    curs = conn.cursor()
    curs.execute("SELECT transportmittel, startort, zielort, fahrtkosten FROM fahrt WHERE startort LIKE ('value1%') AND zielort LIKE ('value2%') AND fahrtdatumzeit >= value3 AND status LIKE ('offen') ")
    data = curs.fetchall()
    for row in data:
        fahrtType.append(row[0])
        fahrtStart.append(row[1])
        fahrtEnd.append(row[2])
        fahrtCost.append(row[3])
    totalfahrt = len(fahrtStart)
    return render_template('view_search.html', fahrtType=fahrtType, fahrtStart=fahrtStart, fahrtEnd=fahrtEnd, fahrtCost=fahrtCost, totalfahrt=totalfahrt)
