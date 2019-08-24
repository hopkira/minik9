import json
import os
from ibm_watson import SpeechToTextV1
from os.path import join, dirname

# retrieve key from bash environment variable
iam_apikey = os.environ['IAM_APIKEY']

# set up an instance of the STT service
service = SpeechToTextV1(
    url = 'https://gateway-lon.watsonplatform.net/speech-to-text/api',
    iam_apikey = iam_apikey
)

# this program assumes that a custom model has already been created
# and trained
language_customization_id = '43d9a145-e6df-47a6-9a91-71315681694d'

# the recordings are in FLAC format created by Audacity
# each recording has a sequential number, starting with 1
# each dataset has its own suffix, so for the truth_data_set
# which has a suffix of 'p', the first audio file is '1p.flac' 

truth_data = [['A1B2', 'C3D4', 'E5F6', 'G7H8'],
              ['H4D2', 'A5C3', 'B1G8', 'E7F6'],
              ['D4E3', 'C1F5', 'H6B2', 'G8A7'],
              ['D2G6', 'B4H7', 'F3A8', 'C5E1'],
              ['F7A1', 'E6B2', 'C8D3', 'H4G5']]

truth_data_set = {
    "eng_name": "Truth Data Set",
    "data": truth_data,
    "weight": 0.8,
    "language_customization_id": language_customization_id,
    "file_suffix": "p"
}

test_data =  [['A8B7','C6D5','E4F3','G2H1'],
              ['F4E2','G5B3','C1A8','D7H6'],
              ['A4G3','B1H5','F6C2','E8D7'],
              ['E2C6','A4F7','H3B8','G5D1'],
              ['G7H1','D6C2','B8E3','A4F5'],
              ['A8B7','C6D5','E4F3','G2H1'],
              ['F4E2','G5B3','C1A8','D7H6'],
              ['A4G3','B1H5','F6C2','E8D7'],
              ['E2C6','A4F7','H3B8','G5D1'],
              ['G7H1','D6C2','B8E3','A4F5']]

test_data_set = {
    "eng_name": "Test Data Set",
    "data": test_data,
    "weight": 0.8,
    "language_customization_id": language_customization_id,
    "file_suffix": "t"
}

# clean the STT text output by substituting "tell 2" for "D" (Delta)
# remove the extraneous spaces and remove the "2" (to) if present
def clean_output(output):
    output = output.replace("tell 2", "D")
    output = output.replace(" ", "")
    if len(output) == 5:
        output = output[0:2]+output[3:5]
    return output

def go(data_set):
    print()
    print('=================== Start '+ data_set['eng_name']  +' =======================')
    print()
    for test_num, test in enumerate(data_set['data']):
        print('================== ' + data_set['eng_name'] + " - Test " + str(test_num+1) +' =====================')
        # send the test file to STT and retrieve list of results
        with open(join(dirname(__file__), ('./' + str(test_num+1) + data_set['file_suffix']+ '.flac')),'rb') as audio_file:
            result = service.recognize(
                audio=audio_file,
                language_customization_id=data_set['language_customization_id'],
                customization_weight=data_set['weight']
                ).get_result()
        # for each result from STT, show the output vs. what was expected
        for count, sentence in enumerate(result['results']):
            # use the transcript of the first alternative in each case
            print(clean_output(sentence['alternatives'][0]['transcript']))
            print(test[count])
    print()
    print('=================== End '+ data_set['eng_name']  +' ======================')
    print()

go(truth_data_set)
go(test_data_set)