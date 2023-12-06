#!/usr/bin/python3
import time
from time import sleep
from datetime import datetime
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
import sounddevice as sd
from scipy.io.wavfile import write

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

def PhotoCapture():
    print("Capturing")
    sleep(2)    
    picam2.capture_file(f"/media/philipmill/KINGSTON/{int(time.strftime('%Y%m%d%H%M%S'))}.jpg")


def AudioCapture():
    fs = 44100
    seconds = 120
    print("audio start")
    myrecording = sd.rec(int(seconds * fs), samplerate = fs, channels = 2)
    sd.wait()
    write(f"/media/philipmill/KINGSTON/{int(time.strftime('%Y%m%d%H%M%S'))}.wav", fs, myrecording)
    print("Audio finished")
    
while True:
    cur = picam2.capture_buffer("lores")
    cur = cur[:w * h].reshape(h, w)
    if prev is not None:
        # Measure pixels differences between current and
        # previous frame
        mse = np.square(np.subtract(cur, prev)).mean()
        if mse > 7:
            if not encoding:
       
                PhotoCapture()
                AudioCapture()
                encoder.output.start()
                encoding = True
                print("New Motion", mse)
            ltime = time.time()
        else:
            if encoding and time.time() - ltime > 5.0:
                encoder.output.stop()
                encoding = False
    prev = cur

picam2.stop_encoder()