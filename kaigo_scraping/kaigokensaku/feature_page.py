# coding: UTF-8

import re
import json
from bs4 import BeautifulSoup

class FeaturePage:

    # 「事業所の特色」ページを解析してデータを取得する
    # @param1: HTMLテキスト
    # @return: dict型で整形したデータ
    @staticmethod
    def parse(page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        if not soup.select_one('title'): return None # Error

        data = {} # 解析結果を格納するdict

        # チャート表示のためのJavaScript
        script = soup.select_one('script:-soup-contains("AmCharts.ready")')

        # <h2>タグを起点に対象データを探す
        h2s = soup.select('article h2')
        if not h2s: return data # empty
        for h2 in h2s:
            # 「お気に入り登録完了」のポップアップは無視する
            if bool(h2.get('class')) and ('modal-title' in h2.get('class')): continue

            # <h2>内のテキストをkeyにする
            k = h2.get_text().replace('\n', ' ').strip()

            # <h2>の周辺要素を元にvalueを生成する
            n = h2.find_next() # 次要素
            p_id = h2.find_parent().get('id') or '' # 親要素id
            l_id = n.select_one('.legenddiv').get('id') if n.select('.legenddiv') else '' # 次要素内のグラフ要素id
            if hasattr(FeaturePage, "parse_" + p_id): # 親要素idに対応する解析処理
                v = getattr(FeaturePage, "parse_" + p_id)(n)
            elif hasattr(FeaturePage, "parse_" + l_id): # チャート表示内容の解析処理
                v = getattr(FeaturePage, "parse_" + l_id)(l_id, script)
            else: # デフォルト：次要素のテキスト
                v = n.get_text().replace('\n', ' ').strip() # 改行コードはスペースに
                v = re.sub('  +', ' ', v).strip() # 余分なスペースは削除

            data[k] = v # dictに追加

        return data

    @staticmethod
    # 「賃金改善以外で取り組んでいる処遇改善の内容」の解析処理
    def parse_shoguuKaizenBlock(n):
        return {'key1': 'value1', 'key2': 'value2'} # TODO

    @staticmethod
    # 「従業員の男女比」シリアルチャートの解析処理
    def parse_legendSerialldiv_staff(l_id, script):
        return 'value' # TODO

    @staticmethod
    # 「従業員の年齢構成」パイチャートの解析処理
    def parse_legendPiediv_staff(l_id, script):
        return 'value' # TODO

    @staticmethod
    # 「利用者の男女比」シリアルチャートの解析処理
    def parse_legendSerialldiv_user(l_id, script):
        return 'value' # TODO

    @staticmethod
    # 「利用者の年齢構成」パイチャートの解析処理
    def parse_legendPiediv_user(l_id, script):
        return 'value' # TODO