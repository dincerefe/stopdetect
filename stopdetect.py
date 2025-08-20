import cv2 as cv
import numpy as np

plist = ["photo-1558626219-fa0c107b5613.jpg","photo-1518749031467-bb37f48aee10.jpg",
         "photo-1635481585588-2440d43b6747.jpg", "photo-1727156275339-aad186798856.jpg",
         "premium_photo-1731192705955-f10a8e7174d2.jpg"]

def find_stop_sign(path):
    low1 = np.array([0,60,70])
    low2 = np.array([160,60,60])
    up1 = np.array([10,255,255])
    up2 = np.array([180,255,255])

    img = cv.imread(path)
    rs = cv.resize(img, (int(img.shape[1]*0.3),int(img.shape[0]*0.3)))
    blured = cv.medianBlur(rs, 7)
    hsv = cv.cvtColor(blured, cv.COLOR_BGR2HSV)

    mask1 = cv.inRange(hsv, lowerb=low1,upperb=up1)
    mask2 = cv.inRange(hsv, lowerb=low2, upperb=up2)
    mask = cv.bitwise_or(mask1,mask2)
    kernel = np.ones((5,5), dtype="uint8")
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)

    c, h = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cn in c:
        area = cv.contourArea(cn)
        if area >600:
            x,y,w,h = cv.boundingRect(cn)
            if (w+20>h and w-20<h):
                x,y,w,h = int(x*100/30), int(y*100/30), int(w*100/30), int(h*100/30)
                cv.rectangle(img,(x,y), (x+w, y+h), (255,0,0), 2)

                cx = x+w//2
                cy= y+h//2
                cv.circle(img, (cx,cy), 2, (255,0,0), -1)
                print(cx,cy)


    cv.imshow(path, img)
    cv.imwrite(f"photo{w}.jpg", img)


for p in plist:
    find_stop_sign(p)

cv.waitKey(0)
cv.destroyAllWindows()