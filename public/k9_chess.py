import chess
import chess.engine
import random
import subprocess
import requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pin_list = [16,20]
GPIO.setup(pin_list, GPIO.OUT)

INFO_SCORE = 2

engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
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
on = GPIO.HIGH
off = GPIO.LOW

def light(pin,value):
    GPIO.output(pin,value)

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

light(back,off)
light(eyes,off)

k9speak("what is your name?")
light(back,on)
name = input ("What is your name? ")
light(back,off)
k9speak("Hello " + name + "!")
k9speak("Do you want to play black or white?")
light(back,on)
while True:
    side = input ("Do you want to play black or white? ")
    if (side == "white" or side == "black"):
        if side == "white":
            player = chess.WHITE
        else:
            player = chess.BLACK
        break
light(back,off)
k9speak("Affimative, you are playing " + side)

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
        light(back,on)
        while True:
            move_str = input("Move?: ")
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    break
            except:
                k9speak(random_msg(invalid_move))
        light(back,off)
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
