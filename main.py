import cv2
import numpy as np
import os

class copy_paste:
    def __init__(self):
        self.positions=[] 
        self.positions2=[]
        self.count=0

    def on_mause(self,event,x,y,flags,param):
        global positions,count
        if event == cv2.EVENT_LBUTTONUP:
            cv2.circle(destination_img,(x,y),1,(0,0,255),-1)
            self.positions.append([x,y])
            if(self.count!=3):
                self.positions2.append([x,y])
            elif(self.count==3):
                self.positions2.insert(2,[x,y])
            self.count+=1
        self.callback_uai()

    def callback_uai(self):

        height, width = destination_img.shape[:2]
        h1,w1 = source_img.shape[:2]
        pts1=np.float32([[0,0],[w1,0],[0,h1],[w1,h1]])
        pts2=np.float32(self.positions)

        h1,_ = cv2.findHomography(pts1, pts2, cv2.RANSAC,5.0)
        persv_img = cv2.warpPerspective(source_img, h1, (width, height))
        self.paste(persv_img)

    def paste(self,persv_img):
        y_offset=0
        x_offset=0

        y1, y2 = y_offset, y_offset + persv_img.shape[0]
        x1, x2 = x_offset, x_offset + persv_img.shape[1]

        alpha_s = persv_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            destination_img[y1:y2, x1:x2, c] = (alpha_s * persv_img[:, :, c] + alpha_l * destination_img[y1:y2, x1:x2, c])  
            cv2.imwrite(output_path + "/{}".format(i),destination_img)



 


if __name__ == "__main__":

    # destination_img_folder_path = "/destination_img/" #enter your destination img folder path
    # source_img_path = "/source_img/logo_IG.png" #enter your source img path
    # output_path = "/copy_paste/output" #enter your output folder path
    # img_liste = os.listdir(destination_img_folder_path)

    destination_img_folder_path = "/home/furkan/Desktop/copy_paste/destination_img/" #enter your destination img folder path
    source_img_path = "/home/furkan/Desktop/copy_paste/source_img/source_img.png" #enter your source img path
    output_path = "/home/furkan/Desktop/copy_paste/output" #enter your output folder path
    img_liste = os.listdir(destination_img_folder_path)
    
    source_img = cv2.imread(source_img_path,cv2.IMREAD_UNCHANGED)

    for i in img_liste:
        try:
            full_path1 = destination_img_folder_path + i
            destination_img = cv2.imread(full_path1)

            bgrr=destination_img[:,:,:3]
            sp=destination_img[:,:,1].shape
            alphaa = np.ones(sp, dtype=np.uint8)
            destination_img=np.dstack([bgrr, alphaa])

            cp = copy_paste()
            cv2.namedWindow('image')
            cv2.setMouseCallback('image',cp.on_mause)
            while True:
                cv2.imshow('image',destination_img)
                k = cv2.waitKey(20) & 0xFF
                if k == 27:
                    break
        except:
            pass
