import re, jinja2
import MySQLdb as mdb
from SSH_connection import SSH_Connection
from Mysql_connection import MYSQL_Connection
from colorama import init, deinit, Fore, Style


vlan_template_file = "templates/vlan_config.j2"
with open(vlan_template_file) as file:
    jinja_template_vlan = file.read()

class Create_Vlans(SSH_Connection, MYSQL_Connection):
    def __init__(self, switch_credential, server_credential, vlan_input_user, cursor):

        self.switch_credential = switch_credential
        self.server_credential = server_credential
        self.vlan_input_user = vlan_input_user
        self.cursor = cursor


    def switch_vlan(self):
        # Adding VLANS to the SW
        print("trying to connect via SSH")
        ssh_host = SSH_Connection(self.switch_credential[0], self.switch_credential[1], self.switch_credential[2])
        self.net_connect, self.hostname = ssh_host.connect()

        # Adding Vlan to Switch
        for vlan_id, vlan_name in self.vlan_input_user.items():
            print(f"adding {vlan_id}")
            template_vars_vlan = {"vlan_id": vlan_id,
                                  "vlan_name": vlan_name}

            template = jinja2.Template(jinja_template_vlan)
            commands = (template.render(template_vars_vlan))
            self.net_connect.send_config_set(commands)
            print(f"{vlan_id} added")
        return self.net_connect, self.hostname

    def sql_vlan(self):
        # Adding VLANS to the SQL
        #self.sql = MYSQL_Connection(self.server_credential[0], self.server_credential[1], self.server_credential[2])
        #print(Fore.GREEN + "Connected to SQL")
        #self.sql_connection, self.cursor = self.sql.sql_connect()

        self.cursor.execute(f"use Vlans")
        print(Fore.GREEN + "Connected to SQL")

        all_dev_gns3 = {}
        vlan = {}
        for vlan_id, vlan_name in self.vlan_input_user.items():
            print(Fore.BLUE, f"Adding {vlan_id} to database")
            vlan[vlan_id] = vlan_name

            values = f"values({vlan_id}, '{vlan_name}', 'python-insert')"
            colums = f"insert into SW1VLANDATA (VLANId, NAME, Description)"
            print(Fore.BLUE + colums, values)
            try:
                self.sql.insert_data(colums, values)
            except (mdb.Error, mdb.Warning) as e:
                if e.args[0] == 1062:
                    print(Fore.RED, f"Duplicated entry for vlan {vlan_id}")
                else:
                    print(e)
    def run_creation(self):
        self.switch_vlan()
        self.sql_vlan()
