

import cv2
from picamera import PiCamera
from time import sleep
import numpy as np

class Camera:
    def __init__(self):
        
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(0.5)

        
    def read(self):
        #read in image
        output = np.empty((720 * 1280 * 3,), dtype=np.uint8)
        self.camera.capture(output, 'rgb')
        image= output.reshape((720, 1280, 3))
        #image=np.mean(image,axis=2)
        image=np.uint8(image)
        
        #find edges
        image=cv2.Canny(image,50,100)
        image=image[200:,:]
        
        #find lines of track
        mids=[]
        lines = cv2.HoughLines(image,1,np.pi/180,100)
        if type(lines) != type(None):
            for line in lines:
                rho,theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                xmid=(x1+x2)/2
                #print(xmid)
                mids.append(xmid)
                #cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
        #cv2.imwrite('static/ims/color.jpg', image)
        #locate the midpoint of the track and
        #scale location to [-1.0,1.0]
        if len(mids)>0:
            mid=np.mean(mids)
            mid-=1280/2
            mid/=1280/2
        else:
            mid=0.0
        #print(mid)
        return mid

if __name__=="__main__":
    camera=Camera()
    camera.read()
#    while 1:
#        sleep(0.5)
#        camera.read()
    
