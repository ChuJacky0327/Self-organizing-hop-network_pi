
import cv2 

cap = cv2.VideoCapture("rtmp://192.168.52.17:1935/rtmp/live")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('relay.mp4', fourcc, 20.0, (width,  height))
while 1:
    try:
        ret,frame = cap.read()
        cv2.imshow('frame',frame)
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print("receive frame is over")
        print("save video")
        break

cap.release()
out.release()
cv2.destroyAllWindows()
