import sys
# import you_get
import os
import csv
import requests


def download(url, filename):
    video_path = filename + ".mp4"
    html = requests.get(url)
    # content返回的是bytes型也就是二进制的数据。
    html = html.content
    with open(video_path, 'wb') as f:
        f.write(html)


if __name__ == '__main__':
    # 视频网站的地址
    sFileName = 'link.csv'
    json = {}
    with open(sFileName, newline='', encoding='UTF-8') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            print(row[0] + '=====' + row[1])
            download(row[1], row[0])
