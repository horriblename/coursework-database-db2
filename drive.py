from datetime import datetime

class Drive:
    def __init__(
            self,
            depart: str,
            destination: str,
            vehicleType: str,
            maxCap:int,
            cost: float,
            driveDateTime: datetime,
            description: str,
            driverBID: int,
            status: str,
    ):
        self.depart: str            = depart
        self.destination: str       = destination
        self.vehicleType:str        = vehicleType
        self.maxCap: int            = maxCap
        self.cost: float            = cost
        self.driveDate: datetime    = driveDateTime
        self.description: str       = description
        self.driverBID: int         = driverBID
        self.status:    str         = status  # can be 'offen' or 'geschlossen'
        assert 1 <= maxCap <= 10, f'Drive got "{maxCap}" for parameter maxCap (Expected value between 1 and 10)'
        assert status == 'offen' or status == 'geschlossen', f'Drive got "{status}" for parameter status (Expected "offen" or "geschlossen")'

    def getDepart(self):
        return self.depart

    def getDestination(self):
        return self.destination

    def getVehicleType(self):
        return self.vehicleType

    def getVehicleTypeId(self) -> int:
        if self.vehicleType == 'Auto':  return 1
        if self.vehicleType == 'Bus':   return 2
        if self.vehicleType == 'Kleintransportmittel': return 3
        # TODO throw error?
        return 0

    def getMaxCap(self):
        return self.maxCap

    def getCost(self) -> float:
        return round(self.cost, 2)

    def getDriveDateTime(self) -> datetime:
        return self.driveDate

    def getDriveDateTimeStr(self) -> str:
        return datetime.strftime(self.getDriveDateTime(),  '%Y-%m-%d %H:%M:%S')

    def getDescription(self):
        return self.description

    def getDriverBID(self) -> int:
        return self.driverBID

    def getStatus(self):
        return self.status
