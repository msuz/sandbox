# coding: UTF-8

import re
from bs4 import BeautifulSoup
from kaigokensaku.detail_page import DetailPage

class KihonPage(DetailPage):

    # 「事業所の詳細」ページを解析してデータを取得する
    # @param1: HTMLテキスト
    # @return: dict型で整形したデータ
    @classmethod
    def parse(cls, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        if not soup.select_one('title'): return None # Error

        data = {} # 解析結果を格納するdict

        # <div class="tab-pane">を起点に対象データを探す
        divs = soup.select('div.tab-pane')
        if not divs: return data # empty
        for div in divs:
            # <h2>内のテキストをkeyにする
            h2 = div.select_one('h2')
            if not h2: continue # 無ければスキップ
            k = cls.parse_h2(h2)
            # <table>からvalueを生成する
            tables = div.select('table')
            if not tables: # <table>が無ければ
                data[k] = '' # 空文字を代入し
                continue # 次へ
            for table in tables:
                # 複数ある場合はkeyに連番を割り振る
                new_key = cls.rename_duplicated_key(k, data.keys())
                trs = table.select('tr')
                v = cls.parse_table(trs)
                data[new_key] = v
        return data
