import numpy as np
import cv2
from time import sleep

class Sensor:
    def __init__(self):
        self.camera=cv2.VideoCapture(-1)
        img=self.capture()

    def capture(self):
        ret, frame = self.camera.read()
        return frame

    def finish(self):
        self.camera.release()

    def bright(self,img):
        img=cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        img[:,:,0]*=1
        img=cv2.cvtColor(img, cv2.COLOR_LAB2BGR)
        return img
        
    def color_mask(self,img,color,cutoff=500):
        img=img.copy()
        h,w,_=img.shape
        img=np.reshape(img,(h*w,3))
        img=img.astype(float)

        color=np.array(color)
        img=np.mean((img-color)**2.0,axis=1)
        #print(img.shape)
        
        mask=np.zeros((h*w),dtype=np.uint8)
        mask[img<cutoff]=255.
        mask=np.reshape(mask,(h,w))
        kernel=np.ones((7, 7), np.uint8)
        mask=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        return mask

    def find_square(self,mask):
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
        #print(len(contours))
        if len(contours)==0:
            return []
            
        cnt=max(contours,key=lambda x:len(x))
        if len(cnt)<100:
            return []

        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        return box

    def draw_square(self,im,box):
        return cv2.drawContours(im,[box],0,(255,255,255),2)


    def identify(self,im,draw=1):
        #           red      green      blue
        colors=[[10,20,110],[10,20,20],[100,50,50]]
        boxes=[]
        for c in colors:
            mask=self.color_mask(im,c)
            box=self.find_square(mask)
            if len(box) > 0:
                boxes.append(box)
        if draw:
            for b in boxes:
                im=self.draw_square(im,b)
        return boxes,im
if __name__ == "__main__":
    
    

    sensor = Sensor()
    img=sensor.capture()
    mask=sensor.color_mask(img,[10,20,20])
    #box=sensor.find_square(mask)
    #img=sensor.draw_square(img,box)
    #print(img.shape)
    boxes,img=sensor.identify(img)
    cv2.imshow("1",mask)
    cv2.imshow("2",img)
    cv2.waitKey(0) 
    
    cv2.destroyAllWindows()
    sensor.finish()
