# coding: UTF-8

import re
import json
from bs4 import BeautifulSoup
from kaigokensaku.detail_page import DetailPage

class KaniPage(DetailPage):

    # 「事業所の概要」ページを解析してデータを取得する
    # @param1: HTMLテキスト
    # @return: dict型で整形したデータ
    @staticmethod
    def parse(page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        if not soup.select_one('title'): return None # Error

        # 基本的な情報
        data = KaniPage.parse_basic_info(soup)

        # <script>からレーダーチャートの値を読み取る
        data['radar_chart'] = KaniPage.parse_radar_chart(soup.select_one('script:-soup-contains("chartRadarData")'))

        # <table>から詳細情報を動的に解析する
        for i in range(1,2):
            elements = soup.select('div#tableGroup-' + str(i) + ' table tr')
            if not elements: continue
            data['kani_table' + str(i)] = KaniPage.parse_table(elements)

        return data

    # JavaScriptを解析して運営状況レーダーチャートのデータを取得する
    # @param1 script: BeautifulSoup().select_one()で取得した<script>タグ
    # @return: dict型で整形したデータ
    @staticmethod
    def parse_radar_chart(script):
        if not script: return None
        code = script.get_text().replace('\n', ' ').strip()
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
