from flask import render_template
import connect
from user import USER_ID

def carSharer():

    conn = connect.DBUtil().getExternalConnection()

    fahrtType = []
    fahrtStart = []
    fahrtEnd = []
    freePlace = []
    fahrtCost = []
    fahrtStatus = []
    fid=[]
    curs = conn.cursor()
    sql = """
SELECT f.transportmittel, f.startort, f.zielort, (f.maxplaetze - COALESCE(r.reserviert, 0)) AS freePlace, f.fahrtkosten, f.status, f.fid 
FROM fahrt f LEFT JOIN (
    SELECT r.fahrt, SUM(r.anzPlaetze) AS reserviert
    FROM reservieren r
    GROUP BY r.fahrt
) r ON r.fahrt=f.fid
WHERE f.status='offen'
    """
    curs.execute(sql)
    data = curs.fetchall()
    for row in data:
        fahrtType.append(row[0])
        fahrtStart.append(row[1])
        fahrtEnd.append(row[2])
        freePlace.append(row[3])
        fahrtCost.append(row[4])
        fahrtStatus.append(row[5])
        fid.append(row[6])
    totalfahrt = len(fahrtStart)

    fahrtType1 = []
    fahrtStart1 = []
    fahrtEnd1 = []
    fahrtStatus1 = []
    fid1 = []
    curs1 = conn.cursor()
    curs1.execute("SELECT transportmittel, startort, zielort, status, fid FROM fahrt f, reservieren r WHERE r.kunde = ? AND f.fid = r.fahrt", (USER_ID,))
    data1 = curs1.fetchall()
    for row1 in data1:
        fahrtType1.append(row1[0])
        fahrtStart1.append(row1[1])
        fahrtEnd1.append(row1[2])
        fahrtStatus1.append(row1[3])
        fid1.append(row1[4])
    totalfahrt1 = len(fahrtStart1)
    print(f'fid {fid}\n fid1 {fid1}')
    return render_template('carSharer.html', fahrtType=fahrtType, fahrtStart=fahrtStart, fahrtEnd=fahrtEnd,
    freePlace=freePlace, fahrtCost=fahrtCost, fahrtStatus=fahrtStatus, totalfahrt=totalfahrt,
    fahrtType1=fahrtType1, fahrtStart1=fahrtStart1, fahrtEnd1=fahrtEnd1,
    fahrtStatus1=fahrtStatus1, totalfahrt1=totalfahrt1, fid=fid, fid1=fid1)
