#time
from gpiozero import MotionSensor
from time import sleep
from datetime import datetime

import time
from multiprocess import Process
from time import sleep
from datetime import datetime
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
import sounddevice
import sounddevice as sd
from scipy.io.wavfile import write 
import sys

#alsa stuff(Audio related)
#alsa config: sudo namo /usr/share/alsa/alsa.conf

#paths



#Sensor Input

pir = MotionSensor(4)

def MotionDetected():
    pir.when_motion
    print("Motion Detected!")
    
def NoMotionDetected():
    pir.when_no_motion
    print("motion stopped!")
    
lsize = (320, 240)
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"}, lores={
                                                 "size": lsize, "format": "YUV420"})
picam2.configure(video_config)
picam2.start_preview()
encoder = H264Encoder(1000000, repeat=True)
encoder.output = CircularOutput()
picam2.encoder = encoder
picam2.start()
picam2.start_encoder(encoder)

w, h = lsize
prev = None
encoding = False
ltime = 0
loop_delay = 0.1

def photo_capture():
    print("Capturing")
    
    picam2.capture_file(f"/media/badgercam/KINGSTON/{int(time.strftime('%Y%m%d%H%M%S'))}.jpg")


def audio_capture():
    fs = 44100
    seconds = 270
    print("audio start")
    myrecording = sd.rec(int(seconds * fs), samplerate = fs, channels = 2, device=1)
    sd.wait()
    write(f"/media/badgercam/KINGSTON/{int(time.strftime('%Y%m%d%H%M%S'))}.wav", fs, myrecording)
    print("Audio finished")
    
while True:
    
    pir.wait_for_motion()
    MotionDetected()
    Process(target=photo_capture())
    Process(target=audio_capture())
    sleep(270)
    pir.wait_for_no_motion()
    NoMotionDetected()
    sleep(5)