# coding: UTF-8

import re
import json
from bs4 import BeautifulSoup

class KaniPage:

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

    # ページ上部に複数個存在する複雑な表を解析してデータを取得する
    # @param1 ページ全体のBeautifulSoupオブジェクト
    # @return: dict型で整形したデータ
    @staticmethod
    def parse_basic_info(soup):
        data = {}

        data['prefCd'] = soup.select_one('input[name="PrefCd"]')['value']
        data['prefName'] = soup.select_one('li.breadcrumb-item a[href="index.php"]').get_text()
        data['jigyosyoCd'] = soup.select_one('span#jigyosyoName')['data-jigyosyocd']
        data['jigyosyoName'] = soup.select_one('span#jigyosyoName').get_text()
        data['serviceCd'] = soup.select_one('div#serviceName')['data-servicecd']
        data['serviceName'] = soup.select_one('div#serviceName').get_text()
        data['versionCd'] = soup.select_one('div#serviceName')['data-versioncd']

        element = soup.select_one('div#shozaichiBlock table th:-soup-contains("所在地") ~ td div')
        # FutureWarning: The pseudo class ':contains' is deprecated, ':-soup-contains' should be used moving forward.
        if element:
            data['postalCode'] = element.get_text().split('\u3000')[0].replace('〒','')
            data['jigyosyoAddress'] = '\u3000'.join(element.get_text().split('\u3000')[1:])

        element = soup.select_one('a.btn-map')
        if element:
            data['latitudeLongitude'] = re.sub(r'^.*[\?&]q=([0-9\.,]+)&?.*$', r'\1', element['onclick'])

        element = soup.select_one('div#shozaichiBlock table th:-soup-contains("連絡先") ~ td div')
        if element:
            data['tel'] = re.sub(r'.*Tel：([0-9\-]+).*', r'\1', element.get_text().strip())
            data['fax'] = re.sub(r'.*Fax：([0-9\-]+).*', r'\1', element.get_text().strip())

        element = soup.select_one('a.btn-homepage')
        if element:
            data['homepage'] = re.sub(r"^.*window.open\('([^']+)'.*$", r'\1', element['onclick'])

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

    # ページ下部に複数個存在する複雑な表を解析してデータを取得する
    # ※要件が複雑なのでバグる可能性が高い。要注意！要テスト！！
    # @param1 trs: BeautifulSoup().select()で取得した<tr>タグのリスト
    # @return: dict型で整形したデータ
    @staticmethod
    def parse_table(trs):
        if not trs: return None

        # 変数を初期化
        data = {}
        rowspan_count = []
        rowspan_ths = []

        # <tr> 1行ごとに逐次処理
        for tr in trs:

            # <th>からkeyを生成
            ths = tr.select('th')
            for i in reversed(range(len(ths))):
                if not ths[i].get_text().replace('\n','').strip(): del ths[i]
            if not ths: continue # 有効な<th>が無かったらスキップして次の行へ
            # rowspanで複数行にまたがるセルを引き回す
            if ths[0].get('rowspan'):
                rowspan_count.append(int(ths[0].get('rowspan')))
                rowspan_ths.append(ths[0])
                ths = ths[1:]
            revised_ths = rowspan_ths + ths
            # rowspanで指定された回数に達したらセルの値を引き回すのをやめる
            for i in reversed(range(len(rowspan_count))):
                rowspan_count[i] -= 1
                if rowspan_count[i] <= 0: del rowspan_count[i], rowspan_ths[i]
            # 1つの文字列として結合する。区切り文字は任意、ひとまずアンダースコア2つにしておく
            k = '__'.join([th.get_text().replace('\n',' ').strip() for th in revised_ths])

            # <td>からvalueを生成
            td = tr.select_one('td')
            # <br>等のタグと改行コードは半角スペース1つに変換する
            v = td.get_text(' ').replace('\n',' ').strip()
            # 画像があればalt値を取得。1つ目のみ、順番はテキストよりも前に固定する
            if td.select_one('img'):
                v = td.select_one('img').get('alt').strip() + ' ' + v
            # ムダなスペースは省略する
            v = re.sub('  +', ' ', v).strip()

            # dictに追加
            data[k] = v

        return data
