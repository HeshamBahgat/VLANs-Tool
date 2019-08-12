from colorama import init, deinit, Fore, Style
import os


init()

class Validate_IP(object):
    def __init__(self, ip_address):
        pass

    def device_ip(self, ip_address):
        print("\n")
        # Checking IP address validity
        # Checking octets
        ip = ip_address.split(".")
        if (len(ip) == 4) and ("" not in ip) and \
                (1 <= int(ip[0]) <= 223) and \
                (int(ip[0]) != 127) and \
                (int(ip[0]) != 169 or int(ip[1]) != 254) and \
                (0 <= int(ip[1]) <= 255 and 0 <= int(ip[2]) <= 255 and 0 <= int(ip[3]) <= 255):
            print(Fore.BLUE + Style.BRIGHT + "ip_address: ", ip_address, "is valid")
            return True
        else:
            print(Fore.RED + Style.BRIGHT + f"Invalid ip_address {ip_address}")
            return False

    def server_ip(self, ip_address):
        print("\n")
        # Checking IP address validity for servers (localhost is allowed)
        #Checking octets
        ip = ip_address.split(".")
        if (len(ip) == 4) and ("" not in ip) and \
            (1 <= int(ip[0]) <= 223) and \
            (int(ip[0]) != 169 or int(ip[1]) != 254) and \
            (0 <= int(ip[1]) <= 255 and 0 <= int(ip[2]) <= 255 and 0 <= int(ip[3]) <= 255):
            print(Fore.BLUE +"ip_address: ", ip_address, "is valid")
            return True
        else:
            print(Fore.RED + Style.BRIGHT + f"Invalid ip_address {ip_address}")
            return False

    def ping(self, Device_IP):
        # check the devices reachabilty and retuen True or false
        # will involk the shell and try to ping
        print(f"pinging: {Device_IP}")
        response = os.system("ping -c 3 -W 3 " + Device_IP)
        Device_Status = ""
        # and then check the response...
        if response == 0:
            Device_Status = True
            print(Device_IP, " Is Up....")
        else:
            Device_Status = False
            print(Device_IP, "IS Down!!!")
        return Device_Status
