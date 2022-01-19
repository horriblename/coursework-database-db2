import connect
from datetime import datetime
from drive import Drive

class DriveStore:
    '''
        Provides utilities to interact with the FAHRT table
    '''

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False) 
        self.complete = None

    def addDrive(self, driveToAdd:Drive):
        curs = self.conn.cursor()
        sql = "INSERT INTO fahrt \
(status, startort, zielort, fahrtdatumzeit, maxPlaetze, fahrtkosten, \
anbieter, transportmittel, beschreibung) VALUES \
(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        curs.execute(sql, (
            driveToAdd.getStatus(),
            driveToAdd.getDepart(),
            driveToAdd.getDestination(),
            driveToAdd.getDriveDateTimeStr(),
            driveToAdd.getMaxCap(),
            driveToAdd.getCost(),
            driveToAdd.getDriverBID(),
            driveToAdd.getVehicleTypeId(),
            driveToAdd.getDescription()
        ))
        # curs.execute(r'SELECT FID FROM fahrt WHERE ')
        #print(curs.fetchall())

        # TODO move to some other place, SELECT queries don't need all this prep work like INSERTs do
    def fetchDriveInfo(self, fid: int) -> tuple[Drive, str, int] | None:
        curs = self.conn.cursor()
        sql = f'''
SELECT f.status, f.startort, f.zielort, f.fahrtdatumzeit, f.maxPlaetze, f.fahrtkosten, f.anbieter, f.transportmittel, f.beschreibung, b.email, r.reserviert
FROM fahrt f 
    LEFT JOIN benutzer b 
        ON b.bid=f.anbieter
    LEFT JOIN (
        SELECT r.fahrt, SUM(r.anzPlaetze) AS reserviert
        FROM reservieren r
        WHERE r.fahrt={fid}
        GROUP BY r.fahrt
    ) r ON r.fahrt=f.fid
WHERE f.fid={fid} 
'''
        print(sql)
        curs.execute(sql)
        res = curs.fetchall()
        if len(res) == 0:
            return None
        res = res[0]
        print("got row ",res)

        param = dict()
        param['status'] 	    = res[0]
        param['startort'] 	    = res[1]
        param['zielort'] 	    = res[2]
        param['fahrtdatumzeit'] = datetime.strptime(res[3], '%Y-%m-%d %H:%M:%S')
        param['maxPlaetze'] 	= res[4]
        param['fahrtkosten'] 	= res[5]
        param['anbieter'] 	    = res[6]
        param['transportmittel']= res[7]
        param['beschreibung'] 	= res[8]

        return Drive(**param), res[9], int(res[10])

    def completion(self):
        self.complete = True

    def close(self):
        if self.conn is not None:
            try:
                if self.complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                print(e)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    print(e)
