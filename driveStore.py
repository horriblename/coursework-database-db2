import connect
from drive import Drive

class DriveStore:

    def __init__(self):
        #dbUtil = connect.DBUtil().getExternalConnection("testdb")
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False) 
        self.complete = None

    def addDrive(self, driveToAdd:Drive):
        curs = self.conn.cursor()
        sql = "INSERT INTO fahrt \
            (status, startort, zielort, fahrtdatumzeit, maxPlaetze, fahrtkosten,\
            anbieter, transportmittel, beschreibung) VALUES\
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
