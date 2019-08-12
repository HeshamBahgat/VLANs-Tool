from valid_ip import Validate_IP
import getpass
from colorama import init, deinit, Fore, Style
init()


# Getting user Credentials
class Get_Credential(Validate_IP):
    def __init__(self):
        print(Fore.MAGENTA + f"Getting IP Address, UserName, Password for all Switches & MySQL Database")

    def switches_credential(self):
        check = False
        while True:
            device_ip = input(Fore.GREEN + f"Switch IP Address: ")
            check = self.device_ip(device_ip)
            print(Fore.CYAN + "Validating IP", device_ip)

            if check == True:
                if self.ping(device_ip):
                    print(Fore.GREEN + f" {device_ip} reachable")
                    break
                else:
                    print(Fore.RED + f"{device_ip} not reachable")
            elif check == False:
                print(Fore.RED + "Write an IP again!!! ")
        username = input("UserName: ")
        psw = getpass.getpass()

        switch_cre = [device_ip, username, psw]
        return switch_cre

    def database_credential(self):
        check = False
        while True:
            server_ip = input(Fore.GREEN + "Server IP Address: ")
            check = self.server_ip(server_ip)
            if check == True:
                if self.ping(server_ip):
                    print(Fore.GREEN + f"{server_ip} reachable")
                    break
                else:
                    print(Fore.RED + f"{server_ip} not reachable")
            elif check == False:
                print(Fore.RED + "Write an IP again!!! ")

        username = input("UserName: ")
        psw = getpass.getpass()

        server_cre = [server_ip, username, psw]
        return server_cre

    def run_credential(self):
        device_cre = self.switches_credential()
        server_cre = self.database_credential()
        return device_cre, server_cre

