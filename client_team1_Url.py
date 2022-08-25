import cv2
from time import sleep
import requests
from PIL import Image
import pickle

# url = 'http://techlab.iptime.org:10000/query'
base_url = 'http://192.168.100.91:10016/'
QUERY_STR = 'query'
ENROLL_STR = 'enroll'

cam_port = 0
cam = cv2.VideoCapture(cam_port)
if (cam.isOpened() == False):
    print("Unable to read camera feed")

imgid = 0
winname = "hdc"
# cv2.namedWindow(winname)

while (True):
    result, image = cam.read()
    #fn = f'C:\\face_trainer_img\image_{imgid}.jpg'
    #cv2.imwrite(fn, image, [cv2.IMWRITE_PNG_COMPRESSION, 7])  # 0 ~9, 압축율
    #cv2.flip(image,1)
    # files = {'media': open(fn, 'rb')}

    #fnpkl = f'C:\\face_trainer_img\\image_{imgid}.pkl'
    #img = Image.open(fn)
    img = image
    #iname = input()

    res = requests.post(base_url + QUERY_STR, pickle.dumps({'img':img, 'name':''}))
    imgid += 1
    print (res.text)
    if(res.text=='fail') :
        cv2.putText(image, "fail", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow(winname, image)
    else :   
        x1 = eval(res.text)['x1']
        y1 = eval(res.text)['y1']
        x2 = eval(res.text)['x2']
        y2 = eval(res.text)['y2']
        confi = eval(res.text)['file'] + ' ' + str(eval(res.text)['score'])
        
        if result == True:
            cv2.putText(image, confi, (int(x2)+20,int(y2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.rectangle(image, (int(x1),int(y1)), (int(x2),int(y2)), (0,0,255),3)
            cv2.imshow(winname, image)
        else:
            break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('e'):
        print('click e')
        iname = input()
        res = requests.post(base_url + ENROLL_STR, pickle.dumps({'img':img, 'name':iname}))
        print(res.text)

    sleep(0.1)
cam.release()
cv2.destroyWindow("GFG")