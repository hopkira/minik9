import os
import sys
import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from queue import Queue, Full

stop_now = False

# retrieve key from bash environment variable
iam_apikey = os.environ['IAM_APIKEY']

# set up an instance of the STT service
service = SpeechToTextV1(
    url = 'https://gateway-lon.watsonplatform.net/speech-to-text/api',
    iam_apikey = iam_apikey
)

CHUNK = 1024
# Note: It will discard if the websocket client can't consumme fast enough
# So, increase the max size as per your choice
BUF_MAX_SIZE = CHUNK * 10
# Buffer to store audio
q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

# Create an instance of AudioSource
audio_source = AudioSource(q, True, True)

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        global stop_now, text
        text = transcript[0]['transcript']
        stop_now = True

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_close(self):
        print("Connection closed")

def recognize_using_websocket(*args):
    mycallback = MyRecognizeCallback()
    service.recognize_using_websocket(audio=audio_source,
                                             content_type='audio/l16; rate=44100',
                                             recognize_callback=mycallback,
                                             interim_results=True,
                                             language_customization_id='43d9a145-e6df-47a6-9a91-71315681694d',
                                             customization_weight=0.8
                                             )

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def pyaudio_callback(in_data, frame_count, time_info, status):
    try:
        q.put(in_data)
    except Full:
        pass # discard
    return (None, pyaudio.paContinue)

audio = pyaudio.PyAudio()

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    stream_callback=pyaudio_callback,
    start=False
)

stream.start_stream()

recognize_thread = Thread(target=recognize_using_websocket, args=())
recognize_thread.start()

while not stop_now:
    pass

stream.stop_stream()
stream.close()
audio.terminate()
audio_source.completed_recording()

print(text)
