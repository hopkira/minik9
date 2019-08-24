from ibm_watson import SpeechToTextV1
import os

# retrieve key from bash environment variable
iam_apikey = os.environ['IAM_APIKEY']

service = SpeechToTextV1(
    url = 'https://gateway-lon.watsonplatform.net/speech-to-text/api',
    iam_apikey = iam_apikey
)

model = service.create_language_model(name='chess',base_model_name='en-US_BroadbandModel')
print(model)