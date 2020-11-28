import os
import constant as C
import asyncio
import json
from controller import login, get_all_audio

import logging
logging.basicConfig(level=logging.INFO)

root_path = os.path.dirname(os.path.abspath(__file__))

def get_audio():
    logging.info(f"Loin with email '{C.EMAIL}' and password '{C.PASSWORD}'")
    access_token = login(C.EMAIL, C.PASSWORD)

    if access_token is None:
        logging.error("Can't log-in!!")
        return None

    with open(f"{root_path}{C.DATA_FILE}") as jsonfile:
        data = json.load(jsonfile)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_all_audio(access_token, data))
    logging.info("Load audio sucess")

if __name__ == '__main__':
    get_audio()
