import pytesseract
import asyncio

async def read_image(path, lang='eng'):
  try:
    text = pytesseract.image_to_string(path, lang=lang)
    await asyncio.sleep(2)
    return text
  except:
    return '[ERROR] Unable to process file: {0}'.format(path)