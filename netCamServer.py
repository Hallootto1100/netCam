import socket
import struct
import time
import picamera
import io

class CamSender():
    def __init__(self):
        self.sock = socket.socket()
        ipAdress = '192.168.1.59'
        hostName = socket.gethostbyaddr(ipAdress)[0]
        print('connecting to %s with IP %s' % (hostName, ipAdress))
        self.sock.connect((ipAdress, 23456))
        self.connection = self.sock.makefile('wb')

    def streamCam(self):
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                time.sleep(2)
                stream = io.BytesIO()

                for foo in camera.capture_continuous(stream, 'jpeg'):
                    self.connection.write(struct.pack('<L', stream.tell()))
                    self.connection.flush()
                    stream.seek(0)
                    self.connection.write(stream.read())
                    stream.seek(0)
                    stream.truncate()
            self.connection.write(struct.pack('<L', 0))
        finally:
            self.connection.close()
            self.sock.close()

if __name__ == '__main__':
    cam = CamSender()
    print('start Streaming...')
    cam.streamCam()
    print('End reached')
