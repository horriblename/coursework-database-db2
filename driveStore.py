import connect
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
        sql = "SELECT fid FROM FINAL TABLE (INSERT INTO fahrt \
(status, startort, zielort, fahrtdatumzeit, maxPlaetze, fahrtkosten, \
anbieter, transportmittel, beschreibung) VALUES \
(?, ?, ?, ?, ?, ?, ?, ?, ?))"
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
        ret = curs.fetchall()
        if len(ret) > 0:
            return ret[0][0]
        return

    def addReservation(self, user: int, fid: int, numSeats: int):
        curs = self.conn.cursor()
        sql = "INSERT INTO reservieren (kunde, fahrt, anzPlaetze) VALUES (?, ?, ?)"
        curs.execute(sql, (user, fid, numSeats))

    def deleteDrive(self, user:int, fid: int):
        curs = self.conn.cursor()
        # workaround for cascading deletion
        curs.execute('DELETE FROM reservieren WHERE fahrt=?', (fid,))
        curs.execute('DELETE FROM schreiben WHERE fahrt=?', (fid,))

        curs.execute('DELETE FROM fahrt WHERE fid=? AND anbieter=?', (fid, user))

    def addRating(self, userID: int, fid: int , comment: str, rating: int):
        '''
            Insert new rating into database
        '''
        curs = self.conn.cursor()
        sql = "SELECT beid FROM FINAL TABLE (INSERT INTO bewertung (textnachricht, rating) VALUES (?, ?))"
        curs.execute(sql, (comment, rating))
        res = curs.fetchall()
        print(res)
        assert len(res) >= 0, "An error has occured while inserting into table bewertung"
        res = res[0][0]

        sql = "INSERT INTO schreiben (benutzer, fahrt, bewertung) VALUES (?, ?, ?)"
        curs.execute(sql, (userID, fid, res))

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
