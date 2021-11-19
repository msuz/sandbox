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
    @classmethod
    def parse_table(cls, trs):
        if not trs: return None

        # 変数を初期化
        data = {} # 結果を格納する
        unused_ths = [] # 前行で未使用の <th>
        rowspan_count = [] # rowspan <th> の利用可能残数
        rowspan_ths = [] # rowspan <th> の中身

        # <tr> 1行ごとに逐次処理
        for tr in trs:
            revised_ths = []

            # <th>からkeyを生成
            ths = tr.select('th')
            # テキストが空の <th> は削除する
            for i in reversed(range(len(ths))):
                if not ths[i].get_text().replace('\n','').strip(): del ths[i]
            if not ths: # 有効な <th> が無い場合、
                if rowspan_count: # rowspan <th> があれば、
                    revised_ths = rowspan_ths + [] # それを使う。参照渡しを避けるために空リストと結合
                elif unused_ths: # 前行で未使用の <th> があれば、
                    revised_ths = unused_ths + [] # それを使う。参照渡しを避けるために空リストと結合
            else: # 有効な <th> があれば
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

            # <td> からvalueを生成
            tds = tr.select('td')
            if not tds: # 有効な <td> が無い場合、
                unused_ths = ths # 前行で未使用の <th> の値を引き継ぐ
                continue # この行の処理は終了。次の行へ
            else:
                unused_ths = [] # 前行で未使用の <th> の値を引き継ぐのをやめる

            # 結果をdictに登録する
            revised_tds = [] # 出力対象 <td> リストを初期化
            for td in tds:
                revised_tds.append(td) # <td> の値を文字列に
                # ※以下のアルゴリズムは厳密さに欠けるので要注意
                if td.find_next_sibling() and td.find_next_sibling().name == 'th': # <td> のすぐ後ろに <th> 要素がある場合
                    k = cls.parse_ths(revised_ths[:-1]) # <th> の一番最後の要素以外をkeyとする
                    k = cls.rename_duplicated_key(k, data.keys()) # 名前が重複してたら連番を割り振る
                    v = cls.parse_tds(revised_tds) # ここまでの <td> の値をvalueとする
                    data[k] = v # dictに追加
                    revised_tds = [] # 出力対象 <td> リストを初期化
            k = cls.parse_ths(revised_ths) # <th> リストをkeyに
            k = cls.rename_duplicated_key(k, data.keys()) # 名前が重複してたら連番を割り振る
            v = cls.parse_tds(revised_tds) # <td> リストをvalueに
            data[k] = v # dictに追加

        return data

    # 名前が重複してたら連番を割り振る
    # @param1 key: キーとなる対象の文字列
    # @param2 keys: すでに存在している重複検査対象となる文字列のリスト
    # @return: 文字列
    @staticmethod
    def rename_duplicated_key(key, keys):
        if not key in keys: return key # 重複してなかったら何もしない
        for i in range(2, 10): # (2)〜(9) を
            new_key = '%s(%s)' % (key, i) # 末尾に付ける
            if not new_key in keys: return new_key # 重複してなかったらそれを返す
        return None # Error

    # <th>リストの値を文字列として返す
    # @param1 trs: BeautifulSoup().select()で取得した<th>タグのリスト
    # @return: 文字列
    @staticmethod
    def parse_ths(ths):
        if not ths: return None # Error
        l = [th.get_text().replace('\n',' ').strip() for th in ths]
        s = '__'.join(l) # 区切り文字は任意、ひとまずアンダースコア2つにしておく
        return s

    # <td>リストの値を文字列として返す
    # @param1 td: BeautifulSoup().select()で取得した<td>タグのリスト
    # @return: 文字列
    @classmethod
    def parse_tds(cls, tds):
        if not tds: return None # Error
        l = [cls.parse_td(td) for td in tds]
        s = ' '.join(filter(bool, l))
        return s

    # <td>の値を文字列として返す
    # @param1 td: BeautifulSoup().select()で取得した<td>タグ
    # @return: 文字列
    @staticmethod
    def parse_td(td):
        if not td: return None # Error
        # <br>等のタグと改行コードは半角スペース1つに変換する
        v = td.get_text(' ').replace('\n',' ').strip()
        # 画像があればalt値を取得。1つ目のみ、順番はテキストよりも前に固定する
        if td.select_one('img'):
            v = td.select_one('img').get('alt').strip() + ' ' + v
        # ムダなスペースは省略する
        v = re.sub('  +', ' ', v).strip()
        return v

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
