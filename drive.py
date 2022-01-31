from datetime import datetime

class Drive:
    def __init__(
            self,
            startort: str,
            zielort: str,
            transportmittel: int,
            maxPlaetze:int,
            fahrtkosten: float,
            fahrtdatumzeit: datetime,
            beschreibung: str,
            anbieter: int,
            status: str,
    ):
        self.startort: str              = startort
        self.zielort: str               = zielort
        self.transportmittel:int        = transportmittel
        self.maxPlaetze: int            = maxPlaetze
        self.fahrtkosten: float         = fahrtkosten
        self.fahrtdatumzeit: datetime   = fahrtdatumzeit
        self.beschreibung: str          = beschreibung
        self.anbieter: int              = anbieter
        self.status:    str             = status  # can be 'offen' or 'geschlossen'
        assert 1 <= maxPlaetze <= 10, f'Drive got "{maxPlaetze}" for parameter maxCap (Expected value between 1 and 10)'
        assert status == 'offen' or status == 'geschlossen', f'Drive got "{status}" for parameter status (Expected "offen" or "geschlossen")'

    def getDepart(self):
        return self.startort

    def getDestination(self):
        return self.zielort

    def getVehicleType(self):
        return self.transportmittel

    def getVehicleTypeId(self) -> int:
        return self.transportmittel

    def getMaxCap(self):
        return self.maxPlaetze

    def getCost(self) -> float:
        return round(self.fahrtkosten, 2)

    def getDriveDateTime(self) -> datetime:
        return self.fahrtdatumzeit

    def getDriveDateTimeStr(self) -> str:
        return datetime.strftime(self.getDriveDateTime(),  '%Y-%m-%d %H:%M:%S')

    def getDescription(self):
        return self.beschreibung

    def getDriverBID(self) -> int:
        return self.anbieter

    def getStatus(self):
        return self.status
