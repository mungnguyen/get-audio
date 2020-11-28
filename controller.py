import os
import time
import requests
import constant as C
import logging
import asyncio
logging.basicConfig(level=logging.INFO)

root_path = os.path.dirname(os.path.abspath(__file__))

def login(email, password):
    url = f"{C.URL}/login"
    access_token = None

    data = {
	"email": email,
	"password": password
    }

    try:
        logging.info(f'Get access_token from url: {url}')
        res = requests.post(url, json=data).json()
        access_token = res['result']['access_token']
        logging.info("Get access_token done!")
    except Exception as e:
        logging.error(f"Can't log-in!! Error: {e}")

    return access_token

def get_audio(access_token, text_item):
    logging.info(f"Start get audio with id '{text_item['id']}' and text '{text_item['rawOriginContent']}'")
    data = {'input_text': text_item['rawOriginContent']}
    url = f"{C.URL}/tts"

    res = requests.post(url, json=data, headers={'access_token': access_token}, stream=True)
    if not os.path.isdir(f"{root_path}/audio/team01"):
        os.makedirs(f"{root_path}/audio/team01")

    with open(f"{root_path}/audio/{C.TEAM_NAME}/{text_item['id']}.wav", mode='wb') as f:
        f.write(res.json()['result']['data'].encode('latin-1'))

    logging.info(f"Get audio with id {text_item['id']} and text {text_item['rawOriginContent']} done!")

async def get_all_audio(access_token, inputs):
    logging.info(f"Start get all audio: {len(inputs)} files")
    # with concurrent.futures.ThreadPoolExecutor(max_workers=len(inputs)) as executor:
    #     executor.map(get_audio, args)
    await asyncio.gather((get_audio(access_token, item) for item in inputs))

    logging.info(f"Get all audio done!!")
