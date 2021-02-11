from typing import Text
from bs4 import BeautifulSoup
import requests as req
import feedparser
import pandas as pd
import time
import threading as thr
import multiprocessing as mp
import os
from yaspin import yaspin


def find(arr, title):
    for x in arr:
        if str(x["title"]) == str(title):
            return True
        else:
            return False


def pantip_extract():
    feed = feedparser.parse('https://pantip.com/forum/feed')
    new_items = []
    for item in feed.entries:
        _item = {}
        _item['title'] = item.title
        _item['description'] = item.summary
        _item['link'] = item.link
        _item['published'] = item.published
        new_items.append(_item)

    return new_items


pantip_data = []


def get_data(kill):
    pantip_data = []
    with yaspin(text='scraping..........'):
        while True:
            if kill():
                break
            data = pantip_extract()
            pantip_data.extend(data)
            data_clean = []
            for i in range(len(pantip_data)):
                if pantip_data[i] not in pantip_data[i + 1:]:
                    data_clean.append(pantip_data[i])
            data_frame = pd.DataFrame(
                data_clean, columns=['title', 'description', 'link', 'published'])
            # os.system('clear')
            print("data length : ", len(data_frame))
            path = os.getcwd()
            data_frame.to_csv(path + '/export_dataframe.csv', header=True)
            time.sleep(60)


def main():
    kill = False
    que = mp.Queue()
    thread = thr.Thread(target=get_data, args=[lambda:kill])
    thread.start()
    _input = input('want to exit ? (q)')
    if _input.lower() == 'q':
        kill = True
        thread.join()
        print('has exit')


main()
