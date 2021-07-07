from fastapi import FastAPI, File, UploadFile
from typing import List
import time
import asyncio
import ocr
import utils

app = FastAPI()

@app.get('/')
def home():
  return {
    'message': 'Visit the endpoint: /api/v1/extract_text to perform OCR.'
  }

@app.post('/api/v1/extract_text')
async def extract_text(Images: List[UploadFile] = File(...)):
  response = {}
  start_time = time.time()
  tasks = []

  for img in Images:
    print('Images uploaded: ', img.filename)
    temp_file = utils._save_file_to_server(img, path='./uploads/', save_as=img.filename)
    tasks.append(asyncio.create_task(ocr.read_image(temp_file)))

  text = await asyncio.gather(*tasks)

  for item in range(len(text)):
    response[Images[item].filename] = text[item]
  
  response['Time Taken'] = round((time.time() - start_time), 2)

  return response
