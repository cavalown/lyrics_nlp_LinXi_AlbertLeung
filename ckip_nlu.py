from ckiptagger import NER, POS, WS
from ckiptagger.api import main

import mongoServer as mon
import write_to_csv as wcsv



def ws_tool(text):
    ws = WS("./data")  # 斷詞
    ws_results = ws([text])
    print(ws_results[0])
    return ws_results[0]


def pos_tool(text, ws_results):
    pos = POS("./data")  # 詞性標記
    pos_results = pos(ws_results)
    print(pos_results)
    return pos_results


def ner_tool(text, ws_results, pos_results):
    ner = NER("./data")  # 命名實體識別
    ner_results = ner(ws_results, pos_results)
    for name in ner_results[0]:
        print(name)
    return ner_results


def lyrics_text(mongo_collection):
    lyrics_list = mongo_collection.find({}, {'lyrics': 1})
    # for lyrics_content in lyrics_list:
    #     print(lyrics_content['lyrics'])
    #     break
    return lyrics_list


if __name__ == '__main__':
    # mongo connection and collection
    client = mon.mongo_connection('linode1', 'mongo')
    collection = mon.mongo_collection(client, 'lyrics', 'linxi_mandarin')
    lyrics_list = lyrics_text(collection)
    lyrics_assemble = []
    for lyrics in lyrics_list:
        lyrics_content = lyrics['lyrics']
        ws_results = ws_tool(lyrics_content)
        for i in range(len(ws_results)-1, -1, -1):
            if ws_results[i] in [' ', ' \n', '\u3000']:
                ws_results.pop(i)
        lyrics_assemble += ws_results
    wcsv.writeToCsv('lyrics_assemble', lyrics_assemble)

    # # 斷詞
    # ws_results = ws_tool(text=text)

    # # 詞性標記
    # pos_results = pos_tool(text, ws_results)

    # # 命名實體識別
    # ner_tool(text, ws_results, pos_results)
