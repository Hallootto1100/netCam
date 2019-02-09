from PIL import Image
import io
import socket
from threading import Thread
import struct



class ImageReceiver():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ipAdress = '192.168.1.59'
        hostName = socket.gethostbyaddr(ipAdress)
        print('working on %s with IP %s' % (hostName[0], hostName[2]))

        serverAdress = (ipAdress, 23456)
        print ('starting up on %s port %s' % serverAdress)
        self.sock.bind(serverAdress)

        self.sock.listen(1)
        self.image = Image.Image()

    def reciveData(self):
        print('waiting for a connection')
        try:
            connection = self.sock.accept()[0].makefile('rb')
            print('connection...')
            while True:
                imgLen = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not imgLen:
                    break

                imgStream = io.BytesIO()
                imgStream.write(connection.read(imgLen))
                imgStream.seek(0)
                img = Image.open(imgStream)
                print('Image is %dx%d' % img.size)
                img.verify()
                self.image = img
                print('Image is verified')
        finally:
            connection.close()
            self.sock.close()




if __name__ == "__main__":
    stream = ImageReceiver()
    receiveThread = Thread(target=stream.reciveData)

    receiveThread.start()



    receiveThread.join()
