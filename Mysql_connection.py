import sys
import MySQLdb as mdb
from colorama import init, deinit, Fore, Style
init()

class MYSQL_Connection(object):
    def __init__(self, server_ip, username, password):
        self.server_ip = server_ip
        self.username = username
        self.password = password


    def sql_connect(self):
        print(Fore.GREEN + "connecting to sql")
        try:
            self.sql_connection = mdb.connect(self.server_ip, self.username, self.password)
            self.cursor = self.sql_connection.cursor()
        except (mdb.Error, mdb.Warning) as e:
            if e.args[0] == 2002:
                print("Can't connect to MySQL")
                sys.exit()
            elif e.args[0] == 1045:
                print("Access denied for user")
                sys.exit()
            elif e.args[0] == 2005:
                print("Unknown MySQL server host")
                sys.exit()
            elif e.args[0] == 1698:
                print("Access denied for user")
                sys.exit()
            else:
                print(e)
                sys.exit()
        return self.sql_connection, self.cursor

    def create_databae(self, database):
        print("check database")
        try:
            self.cursor.execute(f"create database {database}")

        except (mdb.Error, mdb.Warning) as e:
            if e.args[0] == 1007:
                print("database exists")
            elif e.args[0] == 1064:
                print("You have an error in your SQL syntax")
            else:
                print(Fore.RED + e)

    def create_tables(self, database, hostname):
        vlan_table = f"create table {hostname}VLANDATA (VLANId INT PRIMARY KEY check (VLANId > 0 AND VLANId < 4095), NAME VARCHAR(255) UNIQUE, Description VARCHAR(255))"
        print(f"check {hostname}VLANDATA table ")
        try:
            self.cursor.execute(f"use {database}")
            #print(vlan_table)
            self.cursor.execute(vlan_table)
        except (mdb.Error, mdb.Warning) as e:
            if e.args[0] == 1050:
                print(f"{hostname}VLANDATA table exists")
            elif e.args[0] == 1064:
                print("You have an error in your SQL syntax")
            else:
                print(e.args[1])

    def insert_data(self, colums, values):
        self.cursor.execute(f"{colums} {values}")
        self.sql_connection.commit()