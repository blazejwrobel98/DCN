import os
import time
import config
import dhcp
import db
import collections
import telnet
import sys
import re

def GlobalMenu():
    options = ["Start Update","Stop Update","Aktualizacja","Statystyki","Wyjście"]
    o = 0
    for i in range(len(options)):
        if options[i] =="Wyjście":
            print(f'[0] {options[i]}')
        else:
            o+=1
            print(f'[{o}] {options[i]}')

def Wait():
    input("Wciśnij dowolny przycisk aby kontynuować . . .")
        
def Error(fun):
    print(f'Wystąpił błąd podczas wywoływania funkcji: {fun}')

def StartUpdate():
    try:
        os.popen('screen -S update -dm bash -c "python3.8 DCN.py"')
        line = os.popen('screen -ls | grep update')
        output = line.read()
        str(output)
        match = "update"
        if (match in output):
            print('Pomyślnie uruchomiono usługę Update')
        Wait()
    except:
        print('Wystąpił błąd podczas uruchamiania usługi Update')
        Wait()

def StopUpdate():
    try:
        os.popen('pkill screen')
        print('Pomyślnie zakończono proces Update')
        Wait()
    except:
        print('Wystąpił błąd podczas zatrzymywania Update')
        Wait()
        
class Host:
    #definicja obiektu Host
    def __init__(self, IP):
        self.IP = IP

    #Rozpoczęcie procesu aktualizacji
    def StartUpdate(self, queue, bi):
        try:
            print('Connecting with: '+self.IP)
            while True:
                tn = telnet.OpenConnection(self.IP)
                if tn == False:
                    return
                else:
                    dev = self.CheckAll(tn)
                    Vlans(tn,dev.Port)
                    Progress(tn, 3)
                    Progress(tn, 4)
                    if dev.Check(tn):
                        DelCfg(tn)
                        dev.SendLog()
                        break
                    dev.Reload(tn)
                    dev.IsUp(tn)
            time.sleep(1)
            Progress(tn,dev.Port)
            time.sleep(1)
            print ("Z PROCESU " + str(bi))
            queue.put(bi)
            sys.exit()
        except:
            return

    #Wyciąganie informacji z urządzenia
    def CheckAll(self,tn):
        tn.write(b"\n")
        tn.read_until(b'#')
        #devtype id
        tn.write(b'show vendor | include DevType \n')
        tn.read_until(b'DevType(ID)')
        s = (tn.read_until(b'\n').decode('ascii').strip())
        print('DevTypeID '+ self.IP +' '+s[-3:])
        id = (s[-3:])
        #get show version
        tn.write(b'show version\n')
        string = str(tn.read_until(b'minutes').decode('ascii'))
        #fw
        fw = re.search("SoftWare.Version(.*)",string)
        fw = (fw.group(0)[16:])
        print("fw " +fw)
        #boot
        boot = re.search("BootRom.Version(.*)",string)
        boot = (boot.group(0)[15:])
        print("boot " +boot)
        #port
        port = re.search("-\d{2}[X|P|F]-",string)
        port = (port.group(0)[1:-2:]) 
        print("port "+port)
        #pn
        pn = re.search('^(.*).Device',string, re.MULTILINE)
        pn = (pn.group(0)[1:])
        print('pn '+pn)
        #sn
        sn = re.search("No.:.*",string)
        sn = (sn.group(0)[4:])
        print("sn "+sn)
        #mac
        mac = re.search("CPU.Mac.(.*)((\d|([a-f]|[A-F])){2}:){5}(\d|([a-f]|[A-F])){2}",string)
        mac = (mac.group(0))
        print("mac "+mac)    
        dev = Devices(IP=self.IP ,FW=fw ,BOOT=boot ,DevTypeID=id ,Port=port ,SN=sn , PN=pn , MAC=mac)
        return dev

class Devices:
    #Definicja obiektu Devices
    def __init__(self, IP, FW, BOOT, DevTypeID, Port, SN, PN, MAC):
        self.IP = IP
        self.FW = FW
        self.BOOT = BOOT
        self.DevTypeID = DevTypeID
        self.Port = Port
        self.SN = SN
        self.PN = PN
        self.MAC = MAC
        self.dbconn = db.DB()
        self.dbresult = self.dbconn.getDeviceInformation(self.DevTypeID)
        self.dbconn.closeConnection()

    #Sprawdzanie czy urządzenie wymaga aktualizacji
    def Check(self,tn):
            rom = self.UpdateBoot(tn)
            Progress(tn, 5)
            time.sleep(10)
            fw = self.UpdateFW(tn)
            Progress(tn, 6)
            if fw == True and rom == True:
                return True
            else:
                return False

    #Aktualizacja
    def UpdateBoot(self, tn):
        if (self.BOOT not in self.dbresult[3]):
            print('New BootRom avalible, start update '+ self.IP)
            print('Staring Boot update...')
            if self.dbresult[3] is not None:   
                tn.write(b"\n")
                tn.read_until(b"#")
                cmd = f"\ncopy ftp://{config.FTP['login']}:{config.FTP['password']}@{config.FTP['ip']}{self.dbresult[3]} boot.rom\n"
                tn.write(cmd.encode("ascii"))
                print(tn.read_until(b"[Y/N]"))
                tn.write(b"y\n")
                print( tn.read_until(b'Write ok.'))
                tn.write(b"\n")
                print('Boot update finished')
            else:
                print ("Missing boot.rom in DB")
        else:
            print('BootRom up to date '+ self.IP)
            return True

    def UpdateFW(self, tn):
        if (self.FW not in self.dbresult[2]):
            print('Avalible new FW, start update '+ self.IP)
            print('Starting FW update...')
            if self.dbresult[2] is not None:
                tn.write(b"\n")
                time.sleep(1)
                print(tn.read_very_lazy())
                print(tn.read_until(b"#"))
                cmd = f"copy ftp://{config.FTP['login']}:{config.FTP['password']}@{config.FTP['ip']}{self.dbresult[2]} nos.img\n"
                tn.write(cmd.encode("ascii"))
                print (tn.read_until(b"[Y/N]"))
                tn.write(b"y\n")
                print(tn.read_until(b'Write ok.'))
                tn.write(b"\n")
                print('FW update finished')
            else:
                print("Missing nos.img in DB")
        else:
            print('FW up to date '+ self.IP)
            return True

    #Przeładowanie urządzenia
    def Reload(self,tn):
        print('zrzut z reload '+ self.IP)
        print(tn.read_very_eager())
        print('Reloading host: '+ self.IP)
        tn.write(b"\n")
        tn.read_until(b"#")
        tn.write(b'reload\n')
        tn.read_until(b"[Y/N]")
        tn.write(b'y\n')
        tn.close()
        time.sleep(60)

    #Sprawdzanie czy host jest dostępny
    def IsUp(self,tn):
        print('zaczynam szukać '+self.IP)
        while True:
            hosts = dhcp.ScanIsAlive(self.IP)
            for host in hosts:
                if self.IP in host:
                    print('znalazlem '+self.IP)
                    return
                else:
                    print('nie znalazlem '+self.IP)
                    time.sleep(5)

    #Pasek postępu
def Progress(tn, nr):
    nr = str(nr)
    tn.write(b"\n")
    tn.read_until(b"#")
    for i in range(3,nr):
        csdm = ["conf","interface ethernet 1/0/{nr}","loopback","end"]
        p = str(i)
        csdm[1] = "interface ethernet 1/0/"+p
        for csd in csdm:
            cs = f"\n{csd}\n"
            tn.write(cs.encode("ascii"))
            time.sleep(1)

def Vlans(tn,port):
    for i in range(0,port):
        tn.write(b"\n")
        tn.read_until(b"#")
        cmds = ["conf","vlan 10","switchport interface ethernet 1/0/3-10","end"]
        vlan = str(10+i)
        inf = str(3+i)
        cmds[1] = "vlan "+ vlan
        cmds[2] = "switchport interface ethernet 1/0/"+ inf
        for cmd in cmds:
            cm = f"\n{cmd}\n"
            tn.write(cm.encode("ascii"))
            time.sleep(1)
     
def DelCfg(tn):
    print("usuwanie konfigu")
    time.sleep(5)
    tn.read_until(b"#")
    tn.write(b"delete startup.cfg\n")
    tn.read_until(b"\n")
    tn.write(b'y\n')
    tn.write(b'\n')

def SendLog(self):
    self.dbconn = db.DB()
    self.dbconn.SendLog(self.FW, self.BOOT, self.DevTypeID, self.SN, self.PN, self.MAC)
    self.dbconn.closeConnection()