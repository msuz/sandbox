# coding: UTF-8

import re
from bs4 import BeautifulSoup
from kaigokensaku.detail_page import DetailPage

class OriginalPage(DetailPage):

    # 「その他」ページを解析してデータを取得する
    # @param1: HTMLテキスト
    # @return: dict型で整形したデータ
    @classmethod
    def parse(cls, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        if not soup.select_one('title'): return None # Error

        data = {} # 解析結果を格納するdict
        k = '都道府県もしくは政令指定都市ごとに設けている項目' # keyは固定値

        # <div id="originalBlock">内の<table>から値を取得する
        tables = soup.select('div#originalBlock table')
        if not tables: return data # 有効な表が無ければ空dictを返す

        # アラートメッセージ (例:<td class="warningCenter">現在、情報がありません。</td>)
        if tables[0].select('td.warningCenter'):
            v = cls.parse_td(tables[0].select_one('td.warningCenter')) # メッセージを返す
            data[k] = v
            return data

        # <table>に対して逐次処理
        for table in tables:
            # 複数ある場合はkeyに連番を割り振る
            new_key = cls.rename_duplicated_key(k, data.keys())
            v = cls.parse_table(table)
            if v is False: return False # エラー (Noneや{}は問題なし)
            data[new_key] = v

        return data
