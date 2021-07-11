from fastapi import FastAPI
from pydantic import BaseModel
import utils
import json
import os

if os.environ.get('creds'):
  azure_creds = os.getenv('creds')
else:
  with open('secrets/azure.json', 'r') as creds:
    azure_creds = json.load(creds)

headers = {
  'Ocp-Apim-Subscription-Key': azure_creds.key,
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

print(azure_creds)

app = FastAPI()

class Model(BaseModel):
  text_to_analyze: list

@app.post('/')
def analyze_text(text: Model):
  response = {'sentiment': [], 'keyphrases': []}
  number_of_text = len(text.text_to_analyze)

  for index in range(number_of_text):
    document = {'documents': [{'id': index + 1, 'language': 'en', 'text': text.text_to_analyze[index]}]}

    sentiment = utils.call_text_analytics_api(headers, document, endpoint='sentiment')
    keyphrases = utils.call_text_analytics_api(headers, document, endpoint='keyPhrases')

    response['sentiment'].append(sentiment['documents'][0])
    response['keyphrases'].append(keyphrases['documents'][0])
  
  return response
