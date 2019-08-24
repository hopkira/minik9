import os
import sys
import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from queue import Queue, Full

stop_now = False

def listen_for_move():
    global stop_now, text, q, service, audio_source
    iam_apikey = os.environ['IAM_APIKEY']
    service = SpeechToTextV1(
    url = 'https://gateway-lon.watsonplatform.net/speech-to-text/api',
    iam_apikey = iam_apikey
    )
    CHUNK = 1024
    BUF_MAX_SIZE = CHUNK * 10
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))
    audio_source = AudioSource(q, True, True)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
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
    return text

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
    global service, audio_source
    mycallback = MyRecognizeCallback()
    service.recognize_using_websocket(audio=audio_source,
                                      content_type='audio/l16; rate=44100',
                                      recognize_callback=mycallback,
                                      interim_results=True,
                                      language_customization_id='43d9a145-e6df-47a6-9a91-71315681694d',
                                      customization_weight=0.8
                                      )

def pyaudio_callback(in_data, frame_count, time_info, status):
    global q
    try:
        q.put(in_data)
    except Full:
        pass # discard
    return (None, pyaudio.paContinue)
