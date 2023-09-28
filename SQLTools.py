import mysql.connector

class sqlInterpreter:
    def __init__(self, pwd):
        self.db = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                passwd=str(pwd),
                                database="mydatabase"
                            )
        self.mycursor = self.db.cursor()
    
    def logInfo(self, fileName, n, privateKey):
        sql = "INSERT INTO EncImg_lists (EncTime, fileName, n, privateKey) VALUES (NOW(), %s, %s, %s)"
        val = [(fileName, n, privateKey)]
        self.mycursor.executemany(sql, val)
        self.db.commit()

    def getPrivateKeyPair(self, fileName):
        sql = "SELECT privateKey, n FROM EncImg_lists WHERE fileName = %s"
        val = [fileName]
        self.mycursor.execute(sql, val)
        records = self.mycursor.fetchone()
        self.db.commit()
        return records[0], records[1]
        