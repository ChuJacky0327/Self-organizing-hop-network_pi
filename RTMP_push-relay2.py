import subprocess as sp
import cv2 as cv
#rtmpUrl = "rtmp://10.0.2.15:1935/rtmp/live"
#rtmpUrl = "rtmp://192.168.43.112:1935/rtmp/live"
#rtmpUrl = "rtmp://192.168.0.166:1935/rtmp/live"
rtmpUrl = "rtmp://192.168.53.15:1935/rtmp/live"
camera_path = "relay.mp4"
cap = cv.VideoCapture(camera_path)

# Get video information
fps = int(cap.get(cv.CAP_PROP_FPS))
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# ffmpeg command
command = ['ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', "{}x{}".format(width, height),
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        '-f', 'flv', 
        rtmpUrl]

# 管道配置
p = sp.Popen(command, stdin=sp.PIPE)
        
# read webcamera
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        print("Opening camera is failed")
        break
            
    # process frame
    # your code
    # process frame
   
    # write to pipe
    p.stdin.write(frame.tostring())
