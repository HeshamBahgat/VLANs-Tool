import paramiko, socket, time, datetime, sys
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException, AuthenticationException, NetMikoTimeoutException
from paramiko.ssh_exception import SSHException, NoValidConnectionsError
from colorama import init, deinit, Fore, Style
init()


class SSH_Connection(object):
    def __init__(self, Host ,user, psw):
        self.Host = Host
        self.user = user
        self.psw = psw


    def try_login(self):
        print(Fore.GREEN + "Connecting to device' " + self.Host)
        ip_address_of_device = self.Host
        ios_device = {
            "device_type": "cisco_ios",
            "ip": ip_address_of_device,
            "username": self.user,
            "password": self.psw
        }
        try:
            self.net_connect = ConnectHandler(**ios_device)
            print(Fore.GREEN + "connection is okay")

        except NoValidConnectionsError:
            print(Fore.RED + "Unable to connect to port 22 either no route to the host or not configured")
            sys.exit()
        except NetMikoTimeoutException:
            print(Fore.RED + "Time out")
            sys.exit()

        except (AuthenticationException):

            print (Fore.RED + "Authentication failure: ")
            sys.exit()
        except (NetMikoAuthenticationException):
            print(Fore.RED + "Timeout to device: ")
            sys.exit()
        except (EOFError):
            print(Fore.RED + "End of file while attempting device ")
            sys.exit()
        except (SSHException):
            print(Fore.RED + "End Issue. Are you sure SSH is enabled?")
            sys.exit()
        except Exception as unknown_error:
            print (Fore.RED + " Some other error: %d" %(unknown_error))
            sys.exit()
        except (socket.error, socket.gaierror):
            print(Fore.RED + "socket error")
            sys.exit()
        except(EOFError or SSHException):
            print(Fore.RED + "lets see")
            sys.exit()

    def connect(self):
        self.try_login()
        self.prompt = self.net_connect.find_prompt()
        self.hostname = self.prompt[:-1]
        return self.net_connect, self.hostname
