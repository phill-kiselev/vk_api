# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:07:50 2019

@author: user
"""

import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pickle, random, time

all_data = []
need_data = []

tok = [DELETED]
proxies = ["64.235.204.107:8080", "51.89.227.85:9999", "51.89.226.241:9999", "51.158.98.121:8811",
           "51.158.111.242:8811", "51.158.123.35:8811", "54.37.103.99:3128", "163.172.189.32:8811",
           "46.235.53.26:3128", "51.158.68.133:8811", "51.158.186.255:8811", "51.158.186.242:8811"]


def fetch(t, proxy, ps):
    ACCESS_PS = []
    for i,PH in enumerate(ps):
        response = requests.get('https://api.vk.com/method/{METHOD_NAME}'.format(METHOD_NAME='likes.add'),
                                          params={'owner_id': 110606704, #378767645, 
                                                  'type': 'photo',
                                                  'item_id': PH,
                                                  'access_token': t,
                                                  'v': 5.59},
                                          proxies={"http": proxy, "https": proxy}).json()
        try:
            if (response['response']): ACCESS_PS.append(PH)
        except: 
            pass
        if (i % 6 == 0): time.sleep(2)
    return ACCESS_PS


async def get_data_asynchronous(proxies, ps, tok):
    with ThreadPoolExecutor(max_workers=12) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                fetch,
                *(t, proxy, p)  # Allows us to pass in multiple arguments to `fetch`
            )
            for (t, proxy, p) in zip(tok, proxies, [ps[i:i + 12] for i in range(0, len(ps), 12)])
        ]
        for dat in await asyncio.gather(*tasks):
            photos = list(set(photos) - set(dat))
            with open('photos.txt', 'wb') as f:
                pickle.dump(photos, f)
            #need_data.append({dat[0]: [x[0] for x in dat[2]]})


with open('photos.txt', 'rb') as fp:
    photos = pickle.load(fp)

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(get_data_asynchronous(proxies[:12], photos, tok))
loop.run_until_complete(future)
# loop.create_task(get_data_asynchronous())
