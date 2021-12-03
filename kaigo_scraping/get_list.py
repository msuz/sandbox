# coding: UTF-8

# Script: get_list.py
#   直近更新された施設情報ページのURLリストを取得して標準出力する

# Usage:
#   予め必要なライブラリ群はインストールしておく
#     $ pip3 install requests bs4
#   ターミナルで以下のコマンドを実行
#     $ python get_list.py > url_list.txt

# Developer's Environment:
#   macOS Mojave ver 10.14.6
#   Python 3.9.6
#   requests 2.25.1

#
# ライブラリの読み込み
#
import logging
from pprint import pprint as pp
from kaigokensaku.latestinfo_page import LatestinfoPage

#
# 設定値 (実行前に手動で書き換えるべし)
#
LOGGER_LEVEL = logging.INFO # CRITICAL:50, ERROR:40, WARNING:30, INFO:20, DEBUG:10, NOTSET:0
PREF_NO_MIN = 1 # 1:北海道〜47:沖縄
PREF_NO_MAX = 47 # 1:北海道〜47:沖縄

#
# メイン処理
#
def main():
    logger = logging.getLogger(__name__) # ログ出力
    logging.basicConfig(level=LOGGER_LEVEL) # logger.setLevel() が効かない

    # 都道府県ごとに逐次処理
    for i in range(PREF_NO_MIN, PREF_NO_MAX + 1):
        logger.info("pref_cd: %02d", i) # 都道府県番号をINFO出力

        data = LatestinfoPage.get(i) # 取得
        if not data: # データが無かったら
            logger.warning("data not found") # WARNINGを出して
            continue # スキップ

        logger.info("  count: %d", len(data)) # データ件数をINFO出力
        for row in data: # 逐次
            print(row['url']) # URLを標準出力

if __name__ == "__main__":
    main()
