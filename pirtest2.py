#time
from gpiozero import MotionSensor
from time import sleep
from datetime import datetime


#video
import imutils
from imutils.video import VideoStream
from multiprocess import Process

#audio
import pyaudio
import wave
import sounddevice
import sys

#alsa stuff(Audio related)
#alsa config: sudo namo /usr/share/alsa/alsa.conf

#paths
rtsp_url = rtsp_url = "rtsp://badgercam:badgercam@192.168.0.40/stream2"
writepath = "/home/badgercam/Pictures/wildcam/"

#Sensor Input

pir = MotionSensor(4)

def MotionDetected():
    pir.when_motion
    print("Motion Detected!")
    
def NoMotionDetected():
    pir.when_no_motion
    print("motion stopped!")
    
def vidRec():

    vs = VideoStream(rtsp_url).start()
    
    while True:
        frame = vs.read()
        if frame is None:
            continue
        
        frame = imutils.resize(frame, width = 1200)
        cv2.imshow('frame', frame)
               
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
        cv2.startWindowThread()
        cc1 = datetime.now()
        c2 = cc1.strftime("%Y")
        c3 = cc1.strftime("%M")
        c4 = cc1.strftime("%D")
        c5 = cc1.strftime("%H%M%S")
        hello = "image"+c2+c3+c5
        hellojoin = "".join(hello.split())
        cv2.imwrite(f'{writepath}/{hellojoin}.png', frame)
    
    cv2.destroyAllWindows()
    vs.stop()
    
def audioRec():
    
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 48000
    seconds = 273
    path = '/home/badgercam/Pictures/wildcam'
    filename = time.strftime("%Y%m%d-%H%M%S.wav")
    
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
    Process(target=vidRec())
    Process(target=audioRec())
    sleep(270)
    pir.wait_for_no_motion()
    NoMotionDetected()
    sleep(5)
