# coding: UTF-8

import re
import json
from bs4 import BeautifulSoup
from kaigokensaku.detail_page import DetailPage

class FeaturePage(DetailPage):

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

            # 専用の解析処理があればそれを使う、無ければデフォルト処理
            if hasattr(FeaturePage, "parse_" + p_id): # 親要素idに対応する解析処理
                v = getattr(FeaturePage, "parse_" + p_id)(n)
            elif hasattr(FeaturePage, "parse_" + l_id): # チャート表示内容の解析処理
                v = getattr(FeaturePage, "parse_" + l_id)(script)
            else: # デフォルト
                # 要素のテキスト
                v = n.get_text().replace('\n', ' ').strip() # 改行コードはスペースに
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
            k = dt.get_text().replace('\n', ' ').strip()
            # <dd>内のテキストをvalueにする
            # ※<li>をリストにする手もあるが階層が深くなり過ぎるので文字列型に集約する
            v = dt.find_next().get_text(' ').replace('\n', ' ').strip() # タグの区切りと改行コードはスペースに
            v = re.sub('  +', ' ', v).strip() # 余分なスペースは削除
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
