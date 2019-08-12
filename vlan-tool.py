#!/usr/bin/env python

import sys
from credential import Get_Credential
from sync_data import Sync_Data
from create_vlan import Create_Vlans
from colorama import init, deinit, Fore, Style
import time
init()

###################### Getting Input From the user and check all entry before any action ###########################################################
def check_name(dict_vlan, host_name, vlan_name, device):
    for k, v in dict_vlan[host_name].items():
        if vlan_name == v:
            print(Fore.RED + f"We Found Dup vlan_name vlan {k}, named {v} on the {device}")
            return (k, v)

def get_vlan_name():
    while True:
        vlan_name = input(Fore.GREEN + f"VLAN Name: ")
        if check_name(all_gns3_vlan, host_name, vlan_name, host_name):
            print(Fore.RED + "name already Exist on the SWitch")
        elif check_name(all_sql_vlan, host_name, vlan_name, "Database"):
            print(Fore.RED + "name already Exist on the Database")
        #elif vlan_name in vlan_input_user.values():
        #    print(Fore.RED + "name already Entered")
        else:
            print("Continue")
            break
    return vlan_name

def vlan_input(option):
    # Getting vlan-Id and name form the user

    if option == "create":
        while True:
            try:
                valn_numbers = int(input(Fore.GREEN  + f"how many vlans want to {option}: "))
                break
            except ValueError as Er:
                print(Fore.RED + "Wrong input please Enter an integer")
        vlan_input_user = {}
        for n in range(int(valn_numbers)):
            while True:
                try:
                    while True:
                        vlan_Id = int(input(Fore.GREEN + f"VLAN{n + 1} Id: "))

                        if vlan_Id in all_gns3_vlan[host_name].keys():
                            print(Fore.RED + f"We Found Dup vlan in the switch {host_name}")
                            print(vlan_Id, all_gns3_vlan[host_name][vlan_Id])
                        elif vlan_Id in all_sql_vlan[host_name].keys():
                            print(Fore.RED + f"We Found Dup vlan in the switch {host_name}")
                            print(vlan_Id, all_sql_vlan[host_name][vlan_Id])
                        elif vlan_Id in vlan_input_user.keys():
                            print(Fore.RED + "Vlan already Entered")
                        elif vlan_Id == 1:
                            print(Fore.RED + "Its The Default Vlan")
                        elif vlan_Id > 4094:
                            print(Fore.RED + " a VLAN number which is out of the range 1..4094.")
                        else:
                            break
                    break
                except ValueError as Er:
                    print(Fore.RED + "Wrong input please Enter an integer")
            while True:
                vlan_name = input(f"VLAN{n + 1}Name: ")
                if check_name(all_gns3_vlan, host_name, vlan_name, host_name):
                    print(Fore.RED + "name already Exist on the SWitch")
                elif check_name(all_sql_vlan, host_name, vlan_name, "Database"):
                    print(Fore.RED + "name already Exist on the Database")
                elif vlan_name in vlan_input_user.values():
                    print(Fore.RED + "name already Entered")
                else:
                    print("Continue")
                    break
            vlan_input_user[vlan_Id] = vlan_name
        return vlan_input_user, option

    elif option == "update":
        while True:
            try:
                valn_numbers = int(input(Fore.GREEN  + f"how many vlans want to {option}: "))
                break
            except ValueError as Er:
                print(Fore.RED + "Wrong input please Enter an integer")
        modify_both_sides, modify_sw_side, add_sql_side, modify_sql_side, add_sw_side, add_both_sides = False, False, False, False, False, False
        modify_both, modify_sw, add_sql, modify_sql, add_sw, add_both = {}, {}, {}, {}, {}, {}
        vlan_input_user = {}
        for n in range(int(valn_numbers)):
            while True:
                try:
                    while True:
                        vlan_Id = int(input(Fore.GREEN + f"VLAN{n + 1} Id: "))

                        if vlan_Id in modify_both.keys() or vlan_Id in modify_sw.keys() or vlan_Id in add_sql.keys() or \
                                vlan_Id in modify_sql.keys() or vlan_Id in add_sw.keys() or vlan_Id in add_both.keys():
                            print(Fore.RED + "Vlan already Entered")
                        elif vlan_Id == 1:
                            print(Fore.RED + "Its The Default Vlan")
                        elif vlan_Id > 4094:
                            print(Fore.RED + " a VLAN number which is out of the range 1..4094.")

                        elif  vlan_Id != 1 and vlan_Id in all_gns3_vlan[host_name].keys() and vlan_Id in all_sql_vlan[host_name].keys():
                            print(Fore.BLUE + f"{vlan_Id} exist on both SW and database")
                            print(vlan_Id, all_gns3_vlan[host_name][vlan_Id],"\n", vlan_Id, all_sql_vlan[host_name][vlan_Id])
                            modify_both_sides = True
                            break
                        elif  vlan_Id != 1 and vlan_Id in all_gns3_vlan[host_name].keys():
                            print(Fore.BLUE + f"{vlan_Id} exist on SW only ")
                            print(vlan_Id, all_gns3_vlan[host_name][vlan_Id])
                            modify_sw_side = True
                            add_sql_side = True
                            break
                        elif vlan_Id != 1 and vlan_Id in all_sql_vlan[host_name].keys():
                            print(Fore.BLUE + f"{vlan_Id} exist on data-base only")
                            print(vlan_Id, all_sql_vlan[host_name][vlan_Id])
                            modify_sql_side = True
                            add_sw_side = True
                            break
                        else:
                            print(f"{vlan_Id} doesn't exist")
                            add_both_sides = True
                            break
                    break
                except ValueError as Er:
                    print(Fore.RED + "Wrong input please Enter an integer")

            if modify_both_sides:
                vlan_name = get_vlan_name()
                modify_both[vlan_Id] = vlan_name
                print("modify_both_sides")
                #return modify_both, modify_both, option, "U"

            elif modify_sw_side and add_sql_side:
                vlan_name = get_vlan_name()
                modify_sw[vlan_Id] = vlan_name
                add_sql[vlan_Id] = vlan_name
                print("modify_sw_side, add_sql_side")
                #return modify_sw, add_sql, option, "A"

            elif modify_sql_side and add_sw_side:
                vlan_name = get_vlan_name()
                modify_sql[vlan_Id] = vlan_name
                add_sw[vlan_Id] = vlan_name
                print("modify_sql_side, add_sw_side")
                #return add_sw, modify_sql, option, "U"

            elif add_both_sides:
                vlan_name = get_vlan_name()
                add_both[vlan_Id] = vlan_name
                print("add_both_sides")
                #return add_both, add_both, option, "A"

        return modify_both, modify_sw, add_sql, add_sw, modify_sql, add_both

    elif option == "delete":
        while True:
            try:
                valn_numbers = int(input(Fore.GREEN  + f"how many vlans want to {option}: "))
                break
            except ValueError as Er:
                print(Fore.RED + "Wrong input please Enter an integer")
        del_from_both, del_from_sw, del_from_sql = [], [], []
        for n in range(int(valn_numbers)):
            while True:
                try:
                    while True:
                        vlan_Id = int(input(Fore.GREEN + f"VLAN{n + 1} Id: "))

                        if vlan_Id in del_from_both or vlan_Id in  del_from_sw or vlan_Id in del_from_sql:
                            print(Fore.RED + "Vlan already Entered")

                        elif vlan_Id == 1:
                            print(Fore.RED + "Its The Default Vlan")

                        elif vlan_Id > 4094:
                            print(Fore.RED + " a VLAN number which is out of the range 1..4094.")

                        elif  vlan_Id != 1 and vlan_Id in all_gns3_vlan[host_name].keys() and vlan_Id in all_sql_vlan[host_name].keys():
                            print(Fore.BLUE + f"{vlan_Id} exist on both SW and database")
                            print(vlan_Id, all_gns3_vlan[host_name][vlan_Id],"\n", vlan_Id, all_sql_vlan[host_name][vlan_Id])
                            del_from_both.append(vlan_Id)
                            print("del_from_both_sides")
                            break
                        elif  vlan_Id != 1 and vlan_Id in all_gns3_vlan[host_name].keys():
                            print(Fore.BLUE + f"{vlan_Id} exist on SW only ")
                            print(vlan_Id, all_gns3_vlan[host_name][vlan_Id])
                            del_from_sw.append(vlan_Id)
                            print("del_from_sw_side")
                            break
                        elif vlan_Id != 1 and vlan_Id in all_sql_vlan[host_name].keys():
                            print(Fore.BLUE + f"{vlan_Id} exist on data-base only")
                            print(vlan_Id, all_sql_vlan[host_name][vlan_Id])
                            del_from_sql.append(vlan_Id)
                            print("modify_sql_side, add_sw_side")
                            break
                        else:
                            print(f"{vlan_Id} doesn't exist")
                    break
                except ValueError as Er:
                    print(Fore.RED + "Wrong input please Enter an integer")
        return del_from_both, del_from_sw, del_from_sql


################## USER MENU #################
print(Fore.LIGHTGREEN_EX + """
############################################################
#########################################################
Welcome To VLAN-Tool
#########################################################
###########################################################
""")

all_gns3_vlan = {}
all_sql_vlan = {}
host_name = ""

def Main():
    """ Interview Task"""

    global all_gns3_vlan
    global all_sql_vlan
    global host_name

    while True:
        all_credential = Get_Credential()
        device_credential, server_credential = all_credential.run_credential()
        data = Sync_Data(device_credential, server_credential)
        data.connect_all()


        try:
            #Enter option for the first screen
            while True:
                print(Fore.MAGENTA + "Gathering all vlans from SW and sql")
                data.refresh_data()
                all_gns3_vlan, all_sql_vlan, host_name = data.run_data()
                print(Fore.YELLOW + "\nUse this tool to:\na - Sync-To(From MYSQL to Sw)\nb - Sync-From(From Sw to SQL)\nc - Create VLAN\nd - update vlan\ne - delete vlan\nf - Connect Another Device\ng - Exit program\nchoose(a, b, c, d, e)")
                user_option_sim = input("Enter your choice: ")

                if user_option_sim == "a":
                    data.sync_to()

                elif user_option_sim == "b":
                    data.sync_from()

                elif user_option_sim == "c":
                    vlan_input_user, option = vlan_input("create")
                    data.run_creation(vlan_input_user, option)

                elif user_option_sim == "d":
                    option = "update"
                    modify_both, modify_sw, add_sql, add_sw, modify_sql, add_both = vlan_input("update")
                    if len(modify_both) > 0:
                        data.modify_vlan(modify_both, modify_both, option, "U")
                    if len(modify_sw) > 0 and len(add_sql) > 0:
                        data.modify_vlan(modify_sw, add_sql, option, "A")
                    if len(add_sw) > 0 and len(modify_sql) > 0:
                        data.modify_vlan(add_sw, modify_sql, option, "U")
                    if len(add_both) > 0:
                        data.modify_vlan(add_both, add_both, option, "A")

                elif user_option_sim == "e":
                    option = "delete"
                    del_from_both, del_from_sw, del_from_sql = vlan_input("delete")
                    if len(del_from_both) > 0:
                        data.del_vlan_both(del_from_both, del_from_both)
                    if len(del_from_sw) > 0 > 0:
                        data.del_vlan_switch(del_from_sw)
                    if len(del_from_sql) > 0:
                        data.del_vlan_sql(del_from_sql)

                elif user_option_sim == "f":
                    break
                elif user_option_sim == "g":
                    print("Exiting... See ya...\n\n")
                    sys.exit()
                else:
                    print(Fore.RED + "Choose Correct Option")
                    continue

        except KeyboardInterrupt:
            print ("\n\nProgram aborted by user. Exiting...\n")
            sys.exit()

if __name__ == "__main__":
    Main()



"""
 print("\n" ,Fore.RED + "Do you want to continue?")
            answer = input("y/n: ")
            if answer.capitalize() == "Y":
                print("Hold 5 sec")
                time.sleep(5)
                continue
            elif answer.capitalize() == "N":
                break"""