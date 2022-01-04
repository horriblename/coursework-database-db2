import jaydebeapi
import os
import csv
import re
from typing import cast, Union

def csv_reader(path):
    with open(path, "r") as csvfile:
        tmp = {}
        reader = csv.reader(csvfile, delimiter='=')
        for line in reader:
            tmp[line[0]] = line[1]
    return tmp

config = csv_reader("properties.settings")

rechnername = config["rechnername"]
username = config["username"]
password = config["password"]
database = config["database"]

class DBUtil:

    def __init__(self):
        pass

    def getConnection(self):
        try:
            import jpype
            if jpype.isJVMStarted() and not jpype.isThreadAttachedToJVM():
                jpype.attachThreadToJVM()
                jpype.java.lang.Thread.currentThread().setContextClassLoader( # type: ignore
                    jpype.java.lang.ClassLoader.getSystemClassLoader()) # type: ignore
            conn = jaydebeapi.connect("com.ibm.db2.jcc.DB2Driver",
                                      "jdbc:db2:{database}".format(
                                          database=database
                                      ),
                                      {
                                          'securityMechanism': "4"
                                      },
                                      "jdbc-1.0.jar"
                                      )
            return conn
        except Exception as e:
            print(e)

    def getExternalConnection(self) -> jaydebeapi.Connection:

        try:
            # Fix
            import jpype
            if jpype.isJVMStarted() and not jpype.isThreadAttachedToJVM():
                jpype.attachThreadToJVM()
                jpype.java.lang.Thread.currentThread().setContextClassLoader( # type: ignore
                    jpype.java.lang.ClassLoader.getSystemClassLoader()) # type: ignore
            conn = jaydebeapi.connect("com.ibm.db2.jcc.DB2Driver",
                                      "jdbc:db2://"
                                      "{rechnername}.is.inf.uni-due.de:50{gruppennummer}/{database}".format(
                                          rechnername=rechnername,
                                          gruppennummer=cast(re.Match[str], re.match(r"([a-z]+)([0-9]+)", username, re.I)).groups()[1],
                                          database=database
                                          #user=username.strip()
                                      ),
                                      {
                                          'user': username,
                                          'password': password,
                                          'securityMechanism': "3"
                                      },
                                      os.path.join(os.getcwd(), 'jdbc-1.0.jar')
                                      )
            return cast(jaydebeapi.Connection, conn)
        except Exception as e:
            print(e)

        return jaydebeapi.Connection(None, None) # appease debugger, this will never be reached

    def checkDatabaseExists(self) -> bool:
        exists = False
        conn: Union[jaydebeapi.Connection, None]  = None 

        try:
            conn = self.getConnection()
            if conn is not None:
                exists = True
        except Exception as e:
            print(e)
        finally:
            conn = cast(jaydebeapi.Connection, conn)
            conn.close()

        return exists

    def checkDatabaseExistsExternal(self) -> bool:
        exists = False
        conn = None

        try:
            conn = self.getExternalConnection()
            if conn is not None:
                exists = True
        except Exception as e:
            print(e)
        finally:
            if exists:
                cast(jaydebeapi.Connection, conn).close()

        return exists
