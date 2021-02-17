import csv
import re

import write_to_csv as wscv

with open('lyrics_assemble.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        for i in range(len(row)-1, -1, -1):
            row[i].strip()
            if row[i] in [' \u3000', '\u3000 ', ' \u3000 ', 'REPEAT＊', '(',  ')']:
                row.pop(i)
            elif re.search(r'.*REPEAT+.*|.*Repeat+.*', row[i]):
                row.pop(i)
            elif re.search(r'.*\-+.*|.*\＊+.*|.*\*+.*', row[i]):
                row.pop(i)
            elif re.search(r"\'\s+|\s+\'", row[i]): #TODO
                pattern = re.compile(r"\'\s+")
                re.sub(pattern, '', row[i])
                pattern2 = re.compile(r'\s+\'')
                re.sub(pattern2, '', row[i])
            elif re.search(r'[.#@+,<>%~`!$^&:;\?\(\)]+', row[i]):
                pattern = re.compile(r'[.#@+,<>%~`!$^&:;\?\(\)]+')
                re.sub(pattern, '', row[i])
            elif re.search(r'[a-zA-Z＃#]+', row[i]):
                row.pop(i)
            elif re.search(r'\s+', row[i]):
                pattern = re.compile(r'\s+')
                re.sub(pattern, '', row[i])
            row[i].strip()
        print(row)
        wscv.writeToCsv('lyrics_assemble_final', row)
