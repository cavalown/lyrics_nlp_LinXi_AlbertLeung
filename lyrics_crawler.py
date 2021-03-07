
import re
import time

import bs4
import requests
from bs4 import BeautifulSoup
import base64
import mongoServer as mon

url = 'https://mojim.com/%E4%BD%9C%E8%A9%9E%E6%9E%97%E5%A4%95%EF%BC%8B%E5%9C%8B%E8%AA%9E.html?t4'
headers = {'user-agent': 'Googlebot'}

# mongo connection and collection
client = mon.mongo_connection('linode1', 'mongo')
collection = mon.mongo_collection(client, 'lyrics', 'linxi_mandarin')


def lyrics_crawler():
    res = requests.get(url, headers=headers, timeout=8)
    soup = BeautifulSoup(res.text, "lxml")
    lyrics_list = soup.select('span[class="mxsh_ss3"]>a')
    for lyrics_url_shortcut in lyrics_list:
        lyrics_url = 'https://mojim.com' + lyrics_url_shortcut["href"]
        # print(lyrics_url)
        lyr_res = requests.get(lyrics_url, headers=headers, timeout=8)
        lyr_soup = BeautifulSoup(lyr_res.text, "lxml")
        song_name = lyr_soup.select('dt[id="fsZx2"]')[0].text.strip(' ').split('(')[0].split('[')[0]
        print('Song Name:', song_name)
        lyrics_content = lyr_soup.select('dd[id="fsZx3"]')
        pattern = r"作詞：|作曲：|編曲：|監製：|主唱：|演唱：|\[|更多更詳盡歌詞"
        lyrics = ''
        for lyrics_slice in lyrics_content[0]:  # .split('\n'):
            if type(lyrics_slice) is not bs4.element.Tag:  # 略過<br>
                if not re.search(pattern, lyrics_slice):  # 略過非歌詞部分
                    sub_pattern = re.compile(r'.*[\w]+：')
                    lyrics_slice = re.sub(sub_pattern, '', lyrics_slice) # 把指定對象取代掉 女：,男：,合：
                    sub_pattern = re.compile(r'.*[\w]+:')
                    lyrics_slice = re.sub(sub_pattern, '', lyrics_slice)
                    lyrics += lyrics_slice + ' '
        lyrics = lyrics.strip(' ')
        # single lyrics document, id 採用歌名base64編碼
        encode_id = base64.b64encode(bytes(song_name, 'utf-8'))
        print('id', str(encode_id))
        # print(lyrics)
        # break
        doc = {'_id':str(encode_id),'song_name': song_name, 'lyrics': lyrics}
        # save to mongoDB: DB Name = lyrics
        mon.insert_document(collection, doc)
        time.sleep(10)

        


if __name__ == '__main__':
    lyrics_crawler()
