import socket
import errno
def udp():
      target_host = "192.168.1.255"
      target_port = 8080
      client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
      client.sendto("AAABBBCCC",(target_host,target_port))
      data, addr = client.recv(4096)
try:
      udp()
except socket.error as error:
     if error.errno == errno.WSAECONNRESET:
           udp()
     else:
           raise
print data
