# coding: UTF-8

import re
import json
from bs4 import BeautifulSoup
from kaigokensaku.detail_page import DetailPage

class KaniPage(DetailPage):

    # 「事業所の概要」ページを解析してデータを取得する
    # @param1: HTMLテキスト
    # @return: dict型で整形したデータ
    @classmethod
    def parse(cls, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        if not soup.select_one('title'): return None # Error

        # 基本的な情報
        data = cls.parse_basic_info(soup)
        if not data: return None # Error

        # <div class="tab-content content-item">を起点に対象データを探す
        divs = soup.select('div.tab-content.content-item')
        if not divs: return data # empty
        for div in divs:
            # <h2>内のテキストをkeyにする
            h2 = div.select_one('h2')
            if not h2: continue # 無ければスキップ
            k = cls.parse_h2(h2)

            # コンテンツの種類によって処理を振り分ける
            if div.select('div#legendRaderdivWrap'): # レーダーチャートの場合、
                # <script>から値を読み取る
                script = soup.select_one('script:-soup-contains("chartRadarData")')
                v = cls.parse_radar_chart(script)
                data[k] = v
            elif div.select('table'): # <table>の場合、
                # <table>から値を読み取る
                tables = div.select('table')
                for table in tables:
                    # 複数ある場合はkeyに連番を割り振る
                    new_key = cls.rename_duplicated_key(k, data.keys())
                    v = cls.parse_table(table)
                    data[new_key] = v
            else: # 該当するものがなければ
                data[k] = '' # 空文字を代入

        return data


    # JavaScriptを解析して運営状況レーダーチャートのデータを取得する
    # @param1 script: BeautifulSoup().select_one()で取得した<script>タグ
    # @return: dict型で整形したデータ
    @staticmethod
    def parse_radar_chart(script):
        if not script: return None
        code = script.get_text().replace('\n', ' ').replace('\r','').strip()
        json_str = re.sub(r'^.*var chartRadarData = \[([^;]+)\];.*$', r'\1', code)
        json_str = json_str.replace(': jigyosyoName', ': "jigyosyoName"')
        json_str = json_str.replace(': prefName', ': "prefName"')
        json_data = json.loads(json_str)
        data = {}
        for x in json_data: data[x['checkHead']] = str(x['jigyosho'])
        # 以下のような書き方も出来るが可読性が下がるかつPython3.5+に依存するので没
        # from functools import reduce
        # reduce(lambda r,t:{**r, t['checkHead']:t['jigyosho']}, dict, {})
        return data
