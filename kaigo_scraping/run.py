# coding: UTF-8

# Script: run.py
#   与えられたURLリストに従ってWebページから取得した情報をファイルに出力する

# Usage:
#   予め必要なライブラリ群はインストールしておく
#     $ pip3 install requests bs4
#   対象施設のURLをテキストファイルとして用意する
#     $ head url_list.txt
#     https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0113513220-00&ServiceCd=110
#     https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0115012551-00&ServiceCd=110
#     https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0151580024-00&ServiceCd=110
#     https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0170100945-00&ServiceCd=110
#     https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0170102362-00&ServiceCd=110
#   ターミナルで以下のコマンドを実行。標準入力でったURLリストを渡し、標準出力結果をCSVに、エラー出力をログに保存する
#     $ cat url_list.txt | python run.py > result.csv 2> log.txt

# Developer's Environment:
#   macOS Mojave ver 10.14.6
#   Python 3.9.6
#   requests 2.25.1

#
# ライブラリの読み込み
#
import re
import json
import sys
import logging
from pprint import pprint as pp
import requests
from bs4 import BeautifulSoup
from kaigokensaku.detail_pages import DetailPages

#
# 設定値 (実行前に手動で書き換えるべし)
#
MAX_COUNT = 0 # 実行回数の上限。 0 = ∞
LOGGER_LEVEL = logging.INFO # CRITICAL:50, ERROR:40, WARNING:30, INFO:20, DEBUG:10, NOTSET:0

#
# メイン処理
#
def main():
    logger = logging.getLogger(__name__) # ログ出力
    logging.basicConfig(level=LOGGER_LEVEL) # logger.setLevel() が効かない

    i = 0 # 実行回数

    print(DetailPages.get_csv_header()) # CSVヘッダ

    # 標準入力に対して逐次処理
    for line in sys.stdin:
        # 実行回数が上限に達していたら処理を打ち切る
        if (MAX_COUNT > 0) & (i >= MAX_COUNT):
            logger.info("max count [%d]", i)
            break

        # 標準入力からURLを取得
        url = line.rstrip()
        logger.info("url: %s", url)

        # サイトからデータを取得
        dps = DetailPages(url)
        result = dps.load()
        # 取得できなかったらエラー出力
        if not result:
            logger.error("Can't get page data")
            continue # スキップ

        csv = dps.to_csv() # CSV形式で
        print(csv) # 標準出力

        # 実行回数を加算
        i += 1

if __name__ == "__main__":
    main()