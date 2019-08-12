from SSH_connection import SSH_Connection
from Mysql_connection import MYSQL_Connection
import MySQLdb as mdb
from colorama import init, deinit, Fore, Style
import re, jinja2

init()


vlan_template_file = "templates/vlan_config.j2"
with open(vlan_template_file) as f:
    jinja_template_vlan = f.read()


class Sync_Data(SSH_Connection, MYSQL_Connection):
    def __init__(self, switch_credential, server_credential):
        self.switch_credential = switch_credential
        self.server_credential = server_credential

    def connect_ssh(self):
        ssh_host = SSH_Connection(self.switch_credential[0], self.switch_credential[1], self.switch_credential[2])
        self.net_connect, self.hostname = ssh_host.connect()



    def connect_all(self):
        # connect to the Switch
        print(Fore.GREEN + "trying to connect via SSH")
        self.connect_ssh()

        # Connect to the SQL server
        self.sql = MYSQL_Connection(self.server_credential[0], self.server_credential[1], self.server_credential[2])
        print(Fore.GREEN + "Connected to SQL")
        self.sql_connection, self.cursor = self.sql.sql_connect()

        # check if the database and tables are created
        self.sql.create_databae("VLANs")
        self.cursor.execute("use VLANs")
        self.sql.create_tables("VLANs", self.hostname)
        return self.sql_connection, self.cursor


    def refresh_data(self):
        print(Fore.GREEN + "Refresh the Data on the Switch")
        self.connect_ssh()

        # Connect to the SQL server
        print(Fore.GREEN + "Refresh the Data on the Server")
        self.sql = MYSQL_Connection(self.server_credential[0], self.server_credential[1], self.server_credential[2])
        self.sql_connection, self.cursor = self.sql.sql_connect()
        self.cursor.execute("use VLANs")



    def run_data(self):
        # Collecting all vlans on The Swtich and SQL server
        all_gns3_vlan = self.all_switch_vlans()
        all_sql_vlan = self.all_sql_Data()
        self.check_all_data()
        return all_gns3_vlan , all_sql_vlan, self.hostname


    def all_switch_vlans(self):
        # creating dict for all vlan on the Swtich
        print(Fore.LIGHTBLUE_EX + f"Collecting all vlans from {self.hostname}")
        all_vlans = self.net_connect.send_command("show vlan brief")
        pattern = (r"(\d+?) +((\w+)|(\w+[ -]\w+)) +((act/unsup)|([a-zA-Z]+)) +(.+)")
        find = re.finditer(pattern, all_vlans)

        self.all_dev_gns3 = {}
        vlan = {}
        for vlans in find:
            vlan_id, vlan_name, vlan_ports = (vlans.group(1), vlans.group(2), [vlans.group(8)])
            vlan[int(vlan_id)] = vlan_name
        self.all_dev_gns3[self.hostname] = vlan
        return self.all_dev_gns3

    def all_sql_Data(self):
        print(Fore.LIGHTBLUE_EX + f"Collecting all vlans from Database")
        # checking all the tables for the cuuren added vlan
        self.all_dev_sql = {}
        tables = []
        self.cursor.execute("show tables")
        for row in self.cursor.fetchall():
            row = list(row)
            if row[0][-8:] == "VLANDATA":
                tables.append(row[0])
                self.cursor.execute(f"select * from {row[0]}")
                vlan = {}
                for data in self.cursor.fetchall():
                    vlan_id, vlan_name = data[0], data[1]
                    vlan[int(vlan_id)] = vlan_name
                self.all_dev_sql[row[0][:-8]] = vlan
        return self.all_dev_sql

    def check_all_data(self):
        # comparing all vlans on The Switch and Server
        l1 = list(self.all_dev_gns3[self.hostname].keys())
        #print(Fore.BLUE + str(l1))
        l2 = list(self.all_dev_sql[self.hostname].keys())
        #print(Fore.BLUE + str(l2))

        self.value1 = {k: self.all_dev_gns3[self.hostname][k] for k in set(self.all_dev_gns3[self.hostname]).difference(set(self.all_dev_sql[self.hostname]))}
        #print(Fore.BLUE + "self.all_dev_gns3", self.value1)
        self.value2 = {k: self.all_dev_sql[self.hostname][k] for k in set(self.all_dev_sql[self.hostname]).difference(set(self.all_dev_gns3[self.hostname]))}
        #print(Fore.BLUE + "self.all_dev_sql", self.value2)

    def sync_to(self):
        # from SQL to Switch
        print("Sync to SW")
        if len(self.value2.items()) > 0:
            for vlan_id, vlan_name in self.value2.items():
                print(Fore.CYAN + f"adding {vlan_id} to {self.hostname}")
                template_vars_vlan = {"vlan_id": vlan_id,
                                      "vlan_name": vlan_name}

                template = jinja2.Template(jinja_template_vlan)
                commands = (template.render(template_vars_vlan))
                self.net_connect.send_config_set(commands)
                self.net_connect.save_config()
                print(Fore.CYAN + f"{vlan_id} added")
        elif len(self.value2.items()) == 0:
            print(Fore.BLUE + "All Vlans Already Synced")

    def sync_from(self):
        # from Switch to SQL
        print("Sync from SW")
        if len(self.value1.items()) > 0:
            for vlan_id, vlan_name in self.value1.items():
                print(Fore.CYAN + f"adding {vlan_id} to SQL ")
                values = f"values({vlan_id}, '{vlan_name}', 'python-insert')"
                colums = f"insert into {self.hostname}VLANDATA (VLANId, NAME, Description)"
                print(colums, values)
                self.sql.insert_data(colums, values)
                print(Fore.CYAN + f"{vlan_id} added")
        elif len(self.value2.items()) == 0:
            print(Fore.BLUE + "All Vlans Already Synced")

    def sql_vlan(self, vlan_input_user, option):
        # Adding VLANS to the SQL
        print(Fore.GREEN + "Connected to SQL")
        #all_dev_gns3 = {}
        #vlan = {}
        for vlan_id, vlan_name in vlan_input_user.items():
            print(Fore.BLUE, f"{option} {vlan_id} to database")
            #vlan[vlan_id] = vlan_name

            values = f"values({vlan_id}, '{vlan_name}', 'python-insert')"
            colums = f"insert into {self.hostname}VLANDATA (VLANId, NAME, Description)"
            print(Fore.BLUE + colums, values)
            try:
                self.sql.insert_data(colums, values)
            except (mdb.Error, mdb.Warning) as e:
                if e.args[0] == 1062:
                    print(Fore.RED, f"Duplicated entry for vlan {vlan_id}")
                else:
                    print(e)

    def switch_vlan(self, vlan_input_user, option):
        # Adding Vlan to Switch
        for vlan_id, vlan_name in vlan_input_user.items():
            print(f"{option} vlan {vlan_id}")
            template_vars_vlan = {"vlan_id": vlan_id,
                                  "vlan_name": vlan_name}

            template = jinja2.Template(jinja_template_vlan)
            commands = (template.render(template_vars_vlan))
            self.net_connect.send_config_set(commands)
            self.net_connect.save_config()
            print(f"{vlan_id} added")

    def run_creation(self, vlan_input_user, option):
        self.switch_vlan(vlan_input_user, option)
        self.sql_vlan(vlan_input_user, option)

    def modify_vlan(self, sw_dict, sql_dict, option, sql_o):
        # For the Switch modify vlan same as create new vlan
        self.switch_vlan(sw_dict, option)
        print(option)

        # For Sql Modify and Create Vlans are different command
        if sql_o == "A":
            print("A")
            self.sql_vlan( sql_dict, option)
        elif sql_o == "U":
            print("U")
            for vlan_id, vlan_name in sql_dict.items():
                update = f"update {self.hostname}VLANDATA set NAME = '{vlan_name}' where VLANID = {vlan_id}"
                print(update)
                try:
                    self.cursor.execute(update)
                    self.sql_connection.commit()
                except(mdb.Error, mdb.Warning) as e:
                    print(Fore.RED + e)

    def del_vlan_switch(self, del_from_sw):
        # Deleting Vlan from Switch
        for vlan_id in del_from_sw:
            print(f"Deleting vlan {vlan_id}")
            template_vars_vlan = {"del_vlan_id": vlan_id}

            template = jinja2.Template(jinja_template_vlan)
            commands = (template.render(template_vars_vlan))
            self.net_connect.send_config_set(commands)
            self.net_connect.save_config()
            print(f"{vlan_id} deleteded")

    def del_vlan_sql(self, del_from_sql):
        for vlan_id in del_from_sql:
            delete = f"delete from {self.hostname}VLANDATA where VLANID = {vlan_id}"
            try:
                self.cursor.execute(delete)
                self.sql_connection.commit()
                print(delete)
            except(mdb.Error, mdb.Warning) as e:
                print(Fore.RED + e)
    def del_vlan_both(self, del_from_sw, del_from_sql) :
        self.del_vlan_switch(del_from_sw)
        self.del_vlan_sql(del_from_sql)