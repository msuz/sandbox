# coding: UTF-8

import re
from bs4 import BeautifulSoup
from kaigokensaku.detail_page import DetailPage

class UneiPage(DetailPage):

    # 「運営状況」ページを解析してデータを取得する
    # @param1: HTMLテキスト
    # @return: dict型で整形したデータ
    @classmethod
    def parse(cls, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        if not soup.select_one('title'): return None # Error

        data = {} # 解析結果を格納するdict

        # <div class="tab-content ui-tabs">内の<h2>を起点に対象データを探す
        h2s = soup.select('div.tab-content.ui-tabs h2')
        for h2 in h2s:
            k = cls.parse_h2(h2) # <h2>内のテキストをkeyにする
            # <table>からvalueを生成する
            tables = h2.find_next_sibling('div').select('table')
            if not tables: # <table>が無ければ
                # return False # エラー扱いにしちゃっても良いかもしれない
                data[k] = '' # 空文字を代入し
                continue # 次へ
            # 複数<table>に対して逐次処理 (実際には1つしか見たことないけど一応kihon_pageを踏襲しておく)
            for table in tables:
                # 複数ある場合はkeyに連番を割り振る
                new_key = cls.rename_duplicated_key(k, data.keys())
                v = cls.parse_checklist(table)
                if v is False: return False # エラー (Noneや{}は問題なし)
                data[new_key] = v
        return data

    # チェックリスト形式の<table>からデータを取得する
    # @param1 trs: BeautifulSoup().select_one()で取得した<table>タグ
    # @return: dict型で整形したデータ
    @classmethod
    def parse_checklist(cls, table):
        if not table: return None

        data = {} # 結果を格納するdict
        (k1, k2, k3) = [''] * 3 # key

        # <tr>に対して逐次処理
        trs = table.select('tr:not([class="isEtcRow"])') # 非表示行「その他」を除く
        for tr in trs:
            ths = tr.select('th')
            tds = tr.select('td')

            # 大見出し (例: <th>(1) サービス提供開始時のサービス内容の説明及び同意の取得状況</th>)
            if 'thead' in tr.get_attribute_list('class'):
                k1 = cls.parse_td(ths[0])
                if k1 in data.keys(): return False # keyが重複してたらエラー
                data[k1] = {} # keyに対する子dictを初期化
                continue # 次へ

            # 小見出し行 (例: <th>・利用を希望する者が自由に見られるようサービス提供契約前に、重要事項を記した文書のひな形を交付する仕組み等がある。</th>)
            elif bool(ths) and not bool(tds):
                k2 = cls.parse_td(ths[0])
                if k2 in data[k1].keys(): return False # keyが重複してたらエラー
                data[k1][k2] = {} # keyに対する子dictを初期化
                continue # 次へ

            # 各設問行 (例: <td>重要事項を記した文書の雛形の備え付け又は公開が確認できる。</td><td><img alt='○'></td>)
            elif len(tds) == 2:
                k3 = cls.parse_td(tds[0])
                if k3 in data[k1][k2].keys(): return False # keyが重複してたらエラー
                v = cls.parse_td(tds[1])
                data[k1][k2][k3] = v # dictに追加

            # 上記のいずれにも該当しなかったら
            else:
                return False # エラー

        return data
