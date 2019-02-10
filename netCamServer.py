import socket
import subprocess



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
        self.condition = Condition()

    def reciveData(self):
        print('waiting for a connection')
        try:
            connection = self.sock.accept()[0].makefile('rb')
            print('connection...')
            while True:

        finally:
            connection.close()
            self.sock.close()

class ImageDisplay():
    def __init__(self):
        print('ImageDisplay initialized')

    def display(self):
        try:
            while True:
                with stream.condition:
                    stream.condition.wait()
                    stream.image.show()
        finally:
            print('Ende')


if __name__ == "__main__":
    stream = ImageReceiver()
    receiveThread = Thread(target=stream.reciveData)
    displayer = ImageDisplay()
    dispThread = Thread(target=displayer.display)

    receiveThread.start()
    dispThread.start()

    dispThread.join()
    receiveThread.join()
