import telnetlib
import config

    #Nawiązanie połączenia
def OpenConnection(IP):
    try:
        tn = telnetlib.Telnet(IP)
        tn.read_until(b'login:')
        tn.write(config.DCN_telnet['user'].encode('ascii') + b"\n")
        tn.read_until(b'Password:')
        tn.write(config.DCN_telnet['password'].encode('ascii') + b"\n")
        return tn
    except:
        return False
        print("TIMEOUT")
