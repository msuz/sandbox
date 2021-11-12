# coding: UTF-8

import re
import json
from bs4 import BeautifulSoup

class DetailPage:

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
            sufix = ''

            # <th>からkeyを生成
            ths = tr.select('th')
            for i in reversed(range(len(ths))):
                if not ths[i].get_text().replace('\n','').strip(): del ths[i]
            if not ths: # 有効な<th>が無い場合、
                if not rowspan_count: continue # rowspan <th>も無ければスキップして次の行へ
                revised_ths = rowspan_ths + [] # rowspan <th> があれば処理を継続
                sufix = '__l' + str(rowspan_count[-1]) # 名前が重複するのを避けるためのsufix
            else:
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
            k += sufix

            # <td>からvalueを生成
            td = tr.select_one('td')
            if not td: continue
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

    @staticmethod
    # JavaScript内で定義されている変数の値を取得する
    # ※ var __NAME__ = [__VALUE__]; の書式で記述されていることが条件
    # @param1 script:
    # @param2 name: JavaScript内で記述されている変数名
    # @return: JSONを解釈した変数。dict型のハズ
    def parse_script_var(script, name):
        code = script.get_text().replace('\n', ' ').strip()
        json_str = re.sub(r'^.*var ' + name + r' = (\[[^;]+\]);.*$', r'\1', code)
        data = json.loads(json_str)
        return data
