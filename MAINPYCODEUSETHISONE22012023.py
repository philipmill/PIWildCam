#time 
from gpiozero import MotionSensor
from time import sleep
import time
from datetime import datetime


#video
import imutils
from imutils.video import VideoStream
#import multiprocessing as mp
#from multiprocess import Process
#pip install multithreading
from threading import Thread
import cv2

#audio 
import pyaudio
import wave
import sounddevice
import sys

#alsa stuff(Audio related)
#alsa config: sudo namo /usr/share/alsa/alsa.conf

#paths
#rtsp_url = "rtsp://badgercam:badgercam@192.168.0.40/stream2"
writepath = "/media/badgercam/E9F9-D9FC"
#VideoStream(rtsp_url).start()
#cap = cv2.VideoCapture("rtsp://badgercam:badgercam@192.168.1.40/stream2")
#Sensor Input

pir = MotionSensor(4)
#sleep(60)
#use older version of opencv-python (2022)
def MotionDetected():
    pir.when_motion
    print("Motion Detected!")
    
def NoMotionDetected():
    pir.when_no_motion
    print("motion stopped!")
    
def PhotoCap():
    sleep(2)
    cap = cv2.VideoCapture("rtsp://badgercam:badgercam@192.168.1.40/stream1")

    _,frame = cap.read()
    if cap.isOpened():
        print("Its opened")
    #ret,frame = cap.read()

 
    #while True:
    print("vidloop")
    while True:

        frame = imutils.resize(frame, width = 1200)
        cv2.startWindowThread()
        cc1 = datetime.now()
        c2 = cc1.strftime("%Y")
        c3 = cc1.strftime("%M")
        c4 = cc1.strftime("%D")
        c5 = cc1.strftime("%H%M%S")
        hello = "image"+c2+c3+c5
        print(hello)
        hellojoin = "".join(hello.split())
        cv2.imwrite(f'{writepath}/{hellojoin}.png', frame)
        print("done")
        sleep(5)
        break
       
    
    cv2.destroyAllWindows()
    cap.release()
    
def audioRec():
    
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 48000
    seconds = 273
    filename = time.strftime("/media/badgercam/E9F9-D9FC/%Y%m%d-%H%M%S.wav")
    
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate = fs,
                    frames_per_buffer=chunk,
                    input=True)
                   
                        
    frames = []
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
                        
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Finished Recording!")
    
    file = wave.open(filename, 'wb')
    file.setnchannels(channels)
    file.setsampwidth(p.get_sample_size(sample_format))
    file.setframerate(fs)
    
    file.writeframes(b''.join(frames))
    file.close()


while True:
        pir.wait_for_motion()
        MotionDetected()
        v = Thread(target=PhotoCap)
        print("vid started")
        v.start()
        v.join()
        a = Thread(target=audioRec)
        print("audio started")
        a.start()
        a.join()
        pir.wait_for_no_motion()
        NoMotionDetected()

