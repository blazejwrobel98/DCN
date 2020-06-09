import mysql.connector

class DB(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host='172.16.12.13',
            user='update',
            passwd='update_up',
            database='Update',
        )
        self.mycursor = self.mydb.cursor()

    def createDeviceDBContent(self, devType, pn, fwPath):
        dt = ' '.join(devType)
        if fwPath is not None:
            query = f"insert into Software (DevTypeID, PN, NOS, BOOT) values (\"{dt}\", \"{pn}\", \"{fwPath[0] + fwPath[1]}\", \"{fwPath[0] + fwPath[2]}\");"
        else:
            query = f"insert into Software (DevTypeID, PN) values (\"{dt}\", \"{pn}\");"

        self.mycursor.execute(query)
        self.mydb.commit()
        return query

    def dropSoftwareTableContent(self):
        query = "DELETE FROM `Software`;"
        self.mycursor.execute(query)
        self.mydb.commit()

    def getDeviceInformation(self, devType):
        query = f"select `DevTypeID`,`PN`,`NOS`,`BOOT` from Software where DevTypeID like \"%{devType}%\";"
        self.mycursor.execute(query)
        self.result = self.mycursor.fetchall()
        return self.result[0]

    def closeConnection(self):
        self.mydb.close();

    def SendLog(self, FW, BOOT, DevTypeID, SN, PN, MAC):
        query = f"insert into Updated(PN, FW, BOOT, SN, MAC, DevTypeID) values (\"{PN}\",\"{FW}\",\"{BOOT}\",\"{SN}\",\"{MAC}\",\"{DevTypeID}\");"
        self.mycursor.execute(query)
        self.mydb.commit()
        return query

