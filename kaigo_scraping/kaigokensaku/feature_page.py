# coding: UTF-8

import re
import json
from bs4 import BeautifulSoup
from kaigokensaku.detail_page import DetailPage

class FeaturePage(DetailPage):

    # 「事業所の特色」ページを解析してデータを取得する
    # @param1: HTMLテキスト
    # @return: dict型で整形したデータ
    @classmethod
    def parse(cls, page_text):
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
            k = cls.parse_h2(h2)

            # <h2>の周辺要素を元にvalueを生成する
            n = h2.find_next() # 次要素
            p_id = h2.find_parent().get('id') or '' # 親要素id
            l_id = n.select_one('.legenddiv').get('id') if n.select('.legenddiv') else '' # 次要素内のグラフ要素id

            # 専用の解析処理があればそれを使う、無ければデフォルト処理
            if hasattr(cls, "parse_" + p_id): # 親要素idに対応する解析処理
                v = getattr(cls, "parse_" + p_id)(n)
            elif hasattr(cls, "parse_" + l_id): # チャート表示内容の解析処理
                v = getattr(cls, "parse_" + l_id)(script)
            else: # デフォルト
                # 要素のテキスト
                v = n.get_text().replace('\n', ' ').replace('\r','').strip() # 改行コードはスペースに
                v = re.sub('  +', ' ', v).strip() # 余分なスペースは削除

            data[k] = v # dictに追加

        return data

    @staticmethod
    # 「賃金改善以外で取り組んでいる処遇改善の内容」の解析処理
    def parse_shoguuKaizenBlock(dl):
        if not dl: return None
        if dl.name != 'dl': return None
        dts = dl.select('dt')
        data = {}
        for dt in dts:
            # <dt>内のテキストをkeyにする
            k = dt.get_text().replace('\n', ' ').replace('\r','').strip()
            # <dd>内のテキストをvalueにする
            # ※<li>をリストにする手もあるが階層が深くなり過ぎるので文字列型に集約する
            v = dt.find_next().get_text(' ').replace('\n', ' ').replace('\r','').strip() # タグの区切りと改行コードはスペースに
            v = re.sub('  +', ' ', v).strip() # 余分なスペースは削除
            data[k] = v
        return data

    @classmethod
    # シリアルチャートの解析処理
    def parse_chartSeriall(cls, script, name):
        if not script: return None
        script_data = cls.parse_script_var(script, name)
        data = {k: v for k, v in script_data[0].items() if k != 'people'}
        return data

    @classmethod
    # パイチャートの解析処理
    def parse_chartPie(cls, script, name):
        if not script: return None
        script_data = cls.parse_script_var(script, name)
        data = {d['generation']: d['people'] for d in script_data}
        return data

    @classmethod
    # 「従業員の男女比」シリアルチャートの解析処理
    def parse_legendSerialldiv_staff(cls, script):
        return cls.parse_chartSeriall(script, 'chartSeriallData_staff')

    @classmethod
    # 「利用者の男女比」シリアルチャートの解析処理
    def parse_legendSerialldiv_user(cls, script):
        return cls.parse_chartSeriall(script, 'chartSeriallData_user')

    @classmethod
    # 「従業員の年齢構成」パイチャートの解析処理
    def parse_legendPiediv_staff(cls, script):
        return cls.parse_chartPie(script, 'chartPieData_staff')

    @classmethod
    # 「利用者の年齢構成」パイチャートの解析処理
    def parse_legendPiediv_user(cls, script):
        return cls.parse_chartPie(script, 'chartPieData_user')
