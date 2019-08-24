import json
import time
import os
from ibm_watson import SpeechToTextV1
from os.path import join, dirname

# retrieve key from bash environment variable
iam_apikey = os.environ['IAM_APIKEY']

def wait(wait_until):
    waiting = True
    while waiting:
        status = service.get_language_model(customization_id).get_result()
        print (status['status']+"...")
        if status['status'] == wait_until: break
        time.sleep(10)

# create instance of STT class
service = SpeechToTextV1(
    url = 'https://gateway-lon.watsonplatform.net/speech-to-text/api',
    iam_apikey = iam_apikey
)

# this program assumes a language customisation model already exists
customization_id='43d9a145-e6df-47a6-9a91-71315681694d'

# word list should be a valid JSON array string
word_list = [{"word":"K9","sounds_like":["kay nine","K. nine","canine"],"display_as":"K9"},{"word":"Alpha","sounds_like":["how for","offer","how four","office","Alfa"],"display_as":"A"},{"word":"Bravo","display_as":"B"},{"word":"Charlie","display_as":"C"},{"word":"Delta","sounds_like":["tell to","tell two","tell too"],"display_as":"D"},{"word":"Echo","display_as":"E"},{"word":"Foxtrot","display_as":"F"},{"word":"gofree","sounds_like":["go free"],"display_as":"G3"},{"word":"Bright","sounds_like":["brite","bright"],"display_as":"B8"},{"word":"Golf","sounds_like":["gulf","Gulf","call","go"],"display_as":"G"},{"word":"Hotel","sounds_like":["how"],"display_as":"H"},{"word":"alpha","sounds_like":["how for","offer","how four","office","alfa"],"display_as":"A"},{"word":"Gulf","display_as":"G"},{"word":"Alfa","display_as":"A"},{"word":"bravo","display_as":"B"},{"word":"charlie","display_as":"C"},{"word":"delta","display_as":"D"},{"word":"echo","sounds_like":["Ican"],"display_as":"E"},{"word":"foxtrot","display_as":"F"},{"word":"golf","display_as":"G"},{"word":"hotel","display_as":"H"},{"word":"1","sounds_like":["long","will","wall","bone"],"display_as":"1"},{"word":"2","sounds_like":["to","two","too"],"display_as":"2"},{"word":"4","sounds_like":["full","for"],"display_as":"4"},{"word":"5","sounds_like":["fall if"],"display_as":"5"},{"word":"one","display_as":"1"},{"word":"two","display_as":"2"},{"word":"three","display_as":"3"},{"word":"four","display_as":"4"},{"word":"five","display_as":"5"},{"word":"six","display_as":"6"},{"word":"seven","display_as":"7"},{"word":"eight","display_as":"8"}]

print("Adding words to custom model...")
add_words = service.add_words(customization_id=customization_id, words=word_list).get_result()
print("Words added, waiting to train model...")
wait("ready")
service.train_language_model(customization_id=customization_id, word_type_to_add='user', customization_weight=0.3,)
wait("available")

print("Custom model " + customization_id + " is ready for use...")