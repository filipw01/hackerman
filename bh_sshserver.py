import socket
import paramiko
import threading
import sys
import base64

host_key= paramiko.RSAKey(filename='C:\\Users\\Filip\\Desktop\\test_rsa.key')

class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event=threading.Event()
    def check_channel_request(self,kind,chanid):
        if kind=='session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHHIBITED
    def check_auth_password(self,username,password):
        if (username=='justin') and (password=='lovesthepython'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
ssh_port= 22
try:
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind(('127.0.0.1',ssh_port))
    sock.listen(100)
    print'[+] Nasluchiwanie polaczen...'
    client, addr= sock.accept()
except Exception, e:
    print '[-] Nasluch sie nie udal: '+str(e)
    sys.exit(1)
print '[+] Jest polaczone!'

try:
    bhSession=paramiko.Transport(client)
    bhSession.add_server_key(host_key)
    server=Server()
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException, x:
        print'[-] Negocjacja SSH nie powiodla sie.'
    chan=bhSession.accept(20)
    print'[+] Uwierzytelniono!'
    print chan.recv(1024)
    chan.send('Witaj w bh_sshh')
    while True:
        try:
            command=raw_input("Wprowadz polecenie: ").strip('\n')
            if command!='exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print 'exiting'
                bhSession.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            bhSession.close()
except Exception, e:
    print'[-] Przechwycono wyjatek: '+str(e)
    try:
        bhSession.close()
    except:
        pass
    sys.exit(1)
