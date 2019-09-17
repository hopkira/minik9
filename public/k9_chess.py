import chess
import chess.engine
import random
import subprocess
import requests
import sys
import time
import os
import pyaudio
import string
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from queue import Queue, Full

sim = False

if (len(sys.argv)>1):
    if (sys.argv[1] == "test"):
        sim = True
        print ("Executing in simulation mode")

if not sim:
    print ("Importing Pi GPIO library...")
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    pin_list = [16,20]
    GPIO.setup(pin_list, GPIO.OUT)
    on = GPIO.HIGH
    off = GPIO.LOW
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
else:
    on = True
    off = False
    engine = chess.engine.SimpleEngine.popen_uci("./stockfish")

INFO_SCORE = 2
    
board = chess.Board()

pieces = ("Pawn","Knight","Bishop","Rook","Queen","King")
message = ""

your_move = ("What's your move?","Your move!","You're up!","Your go!","It's your move!","It's your turn!","Your turn!","Your chance now","Over to you","Your turn now","Your turn to move")
invalid_move = ("Invalid move","Sorry, invalid move","Incorrect move","That move is not valid","You have miscalculated, that is an invalid move","Move not valid","Improper move", "You are at fault - improper move", "Sorry you can't make that move")
check = ("Check","You are in check","I have you in check","You're in check")
winning = ("I think I'm winning","I'm now in front","This is looking good for me","My position looks strong","Things are looking negative for you","I am very happy with this game","It's not looking good for you","I like winning")
takes = ("takes","captures","takes","triumphs over","takes","prevails over","takes","takes","destroys","seizes","traps","secures","gets","nabs")
losing = ("I am losing, this is not good","You are a very good player","I'm feeling rather negative about this")
mate_win = ("You should prepare for your end", "It's almost over for you", "The end is near for you", "I will mate soon","We are near the end of the game")
mate_lose = ("this is not possible","how can I be losing?","you are the better player","this is not logical - I am losing")
draw = ("We are heading for a draw","The game is looking very even", "This is a well-balanced game", "We are drawing, who will make the winning move?")
instruction = ("Please move my","I will move","I will move my","My move is")
context = {}

eyes = 16
back = 20

def light(pin,value):
    if not sim:
        GPIO.output(pin,value)
    else:
        print("GPIO pin "+str(pin)+" set to "+str(value)+".")

def send_board(board):
    URL = "http://localhost:3001/api/board"
    params ={'board':board}
    response = requests.post(URL, params=params)
    print(response.text)

def get_phrase():
    if (context['score'].is_mate()):
        context.update(to_mate = context['score'].mate())
        if context['player']:
            # human player is white
            if context['to_mate'] >= 0: return random_msg(mate_lose)
            if context['to_mate'] < 0: return random_msg(mate_win)
        else:
            if context['to_mate'] >= 0: return random_msg(mate_win)
            if context['to_mate'] < 0: return random_msg(mate_lose)
    else:
        context.pop('to_mate', None)
        return interpret_score(context['score'].score())

def interpret_score(score):
    if context['player']:
        if score > 60: return random_msg(losing)
        if score < -60: return random_msg(winning)
    else:
        if score > 60: return random_msg(winning)
        if score < -60: return random_msg(losing)
    return random_msg(draw)

def get_color(bool):
    string = "white" if bool else "black"
    return string

def random_msg(phrase_dict):
    length = len(phrase_dict)
    index = random.randint(0,length-1)
    message = phrase_dict[index] 
    return message

def speak(text: str, pitch: int=50, voice: str='en', speed: int=175, capital: int=0) -> int:
    return subprocess.run(['espeak','-v',voice,'-p',str(pitch),'-s',str(speed),'-k',str(capital),text]).returncode

def k9speak(text: str) -> int:
    light(eyes,on)
    speak(text, pitch=99, voice='en-uk-rp', speed=180, capital=20)
    light(eyes,off)  

stop_now = False

def listen_for_text(context="none"):
    global stop_now, text, q, service, audio_source
    stop_now=False
    # print("1. Context is "+context)
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

def listen_for_move():
    move = listen_for_text()
    return move

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        global stop_now, text
        text = transcript[0]['transcript']
        stop_now = True
        light(back,off)

    def on_connected(self):
        print('Connecting...')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Speak now!')
        light(back,on)

    def on_close(self):
        print("Connection closed")

def recognize_using_websocket(*args):
    # print("2. The context I got was "+str(args))
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

print("Turning lights off...")
light(back,off)
light(eyes,off)
print("Lights turned off...")

k9speak("what is your name?")
name = listen_for_text()
# name = input ("What is your name? ")
k9speak("Hello " + str(name) + "!")

k9speak("Do you want to play black or white?")

while True:
    # side = input ("Do you want to play black or white? ")
    side = str(listen_for_text())
    print("I heard: "+side)
    if "white" in side or "what" in side:
        player = chess.WHITE
        side = "white"
        break
    if "black" in side:
        player = chess.BLACK
        side = "black"
        break

k9speak("Affirmative. You are playing " + str(side))

while not board.is_game_over():
    send_board(board.board_fen())
    print(board)
    if board.turn == player:
        # analyse the board
        if board.is_check(): k9speak(random_msg(check)) # announce check
        result = engine.analyse(board=board, limit=chess.engine.Limit(time=0.100),info=INFO_SCORE)
        score = result.score.pov(chess.WHITE)
        # prompt player for their move
        k9speak(random_msg(your_move))
        while True:
            move_str = str(listen_for_move())
            # move_str = input("Move?: ")
            print("I heard: "+move_str)
            move_str = move_str.translate({ord(c): None for c in string.whitespace})
            if len(move_str)>4:
                move_str = move_str[0:2] + move_str[3:5]
                move_str = move_str.lower()
            print("I converted it to: "+move_str)
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    break
            except:
                k9speak(random_msg(invalid_move))
    else:
        # determine the best move for K9 and analyse the board
        result = engine.play(board=board, limit=chess.engine.Limit(time=0.100),info=INFO_SCORE)
        move = result.move
        score = result.info.score.pov(chess.WHITE)
    # Extract move context from board
    move_piece = pieces[board.piece_type_at(move.from_square)-1] 
    move_color = board.turn
    move_from = chess.SQUARE_NAMES[move.from_square]
    move_to = chess.SQUARE_NAMES[move.to_square]  
    if 'score' in context:
        old_score = context["score"]
        context.update(old_score = old_score)
    # Announce if piece is taken
    taken = board.piece_type_at(move.to_square)
    if taken is not None:
        if (board.turn == player):
            if (random.random() < (taken*0.2)):
                k9speak("You have taken my " + pieces[taken-1])
        else:
            k9speak("My " + move_piece + " " + random_msg(takes) + " your " + pieces[taken-1])
    # if no piece is taken, announce K9's move
    else:
        if (board.turn != player):
            k9speak(random_msg(instruction) + move_piece + " from " + move_from + " to " + move_to)
    context.update(player = player,
                   mv_color = move_color,
                   mv_from = move_from,
                   mv_to = move_to,
                   score = score,
                   piece = move_piece)
    # number = 3 and random 0.8
    if ((board.fullmove_number > 3) and (random.random()>0.7)): k9speak(get_phrase())
    board.push(move)
    print()

engine.quit()
print(board)
if board.is_checkmate():
    if board.turn == player:
        k9speak("Checkmate - I have won")
    else:
        k9speak("Congratulations - you have won")
if board.is_stalemate(): message = "We have drawn through stalemate"
if board.is_insufficient_material(): message = "A draw is now inevitable due to insufficient material."
if board.is_seventyfive_moves(): message = "I am really bored.  We have drawn through repetition." 
if board.is_fivefold_repetition(): message= "The game is over, it has been drawn through repetition." 
k9speak(message)
k9speak("Thank you for a lovely game")
