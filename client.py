from sys import argv
import os
import colorama
colorama.init(autoreset=True)
import socket
import progressbar


class cons_client():
    def __init__(self,back_dor_mode=False):
        if not back_dor_mode:
            self.server_ip=input(f"{colorama.Fore.RED}IP{colorama.Fore.GREEN}>>")
        else:
            self.server_ip="127.0.0.1"
        self.server_port=6996
        self.client=socket.socket()
        self.root=False
        self.connect_set=True

        self.server_connect()

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        self.Myip=IP

    def command_worker(self):
        if not self.root:
            client_messsage=input(f"{colorama.Fore.GREEN}User>>{colorama.Fore.WHITE}")
        else:
            client_messsage = input(f"{colorama.Fore.RED}Root{colorama.Fore.GREEN}>>{colorama.Fore.WHITE}")
        self.client.send(client_messsage.encode())

    def wait_server_answer(self,user_part=True,server_message=False):

        if user_part:
            server_message=self.client.recv(1024).decode()
            print(f"{colorama.Back.WHITE}{colorama.Fore.LIGHTBLUE_EX}Server>>{server_message}")
        if server_message=="exit" or server_message=="ex":
            self.connect_set=False
            print(f"{colorama.Fore.GREEN}GOODBYE")
        elif server_message=="enter_root_password":
            root_password=input(f"{colorama.Fore.RED}ROOT password {colorama.Fore.GREEN}>>")
            self.client.send(root_password.encode())
            server_message=self.client.recv(1024).decode()
            self.wait_server_answer(False,server_message)
        elif server_message=="set_root_user":
            self.root=True
        elif server_message=="not root":
            self.root=False
        elif server_message[0:4]=="wr_f":
            filename=server_message[5:]
            file_text="fil_txt "+input(f"Write file {filename}")
            self.client.send(file_text.encode())
            server_message=self.client.recv(1024).decode()
            self.wait_server_answer(False,server_message)
        elif server_message[0:10]=="set_nw_cfg":
            upgr_cfg="upgr_cfg "+input(f"{colorama.Fore.GREEN}>>")
            self.client.send(upgr_cfg.encode())
        elif server_message[0:14]=="start_acc_file":#принятие файла от сервера
            filename=server_message[15:]
            print(filename)
            temp=filename.split(sep="\\")
            print(temp)
            clear_filename=temp[-1]
            print(clear_filename)
            self.get_ip()
            get_file_sesrver=socket.socket()
            get_file_sesrver.bind((self.Myip,9696))
            get_file_sesrver.listen(1)
            file_client,file_client_ip=get_file_sesrver.accept()

            try:
                with open(f"files\\{clear_filename}",'wb') as file:
                    file_data=file_client.recv(1024)
                    while file_data:
                        file.write(file_data)
                        file_data = file_client.recv(1024)
                    file.close()
                get_file_sesrver.close()
                server_message=self.client.recv(1024)
                self.wait_server_answer(False,server_message)
            except:
                pass

        elif server_message[0:14]=="start file get":#Отправка файла серверу
            filename = server_message[15:]
            print(filename)
            send_file_client=socket.socket()
            send_file_client.connect((self.server_ip,6556))
            temp=filename
            prog=[]
            bar=progressbar.ProgressBar(maxval=progressbar.UnknownLength)
            for i in range(1,101):
                prog.append(i)
            try:
                with open(filename,'rb') as file:
                    file_data=file.read(1024)
                    while file_data:
                        send_file_client.send(file_data)
                        file_data=file.read(1024)
                    file.close()
                send_file_client.close()
                server_message=self.client.recv(1024)
                self.wait_server_answer(False,server_message)
            except:
                pass







    def server_connect(self):
        self.client.connect((self.server_ip,self.server_port))
        print(f"{colorama.Fore.GREEN}CONNECTED")
        while self.connect_set:
            self.command_worker()
            self.wait_server_answer()







if __name__ == '__main__':
    cons_client()