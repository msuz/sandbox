# coding: UTF-8

import re
import requests
from bs4 import BeautifulSoup

class DetailPages:
    #
    # インスタンス変数
    #
    urls = {}
    data = {}

    #
    # クラスメソッド
    #
    @classmethod
    def __init__(self, url):
        self.set_urls(url)
        return

    @classmethod
    def set_urls(self, url):
        self.urls = self.generate_urls(url)
        return True

    @classmethod
    def get_urls(self):
        return self.urls

    @classmethod
    def get_url(self, key):
        if not key in self.urls: return None
        return self.urls[key]

    @classmethod
    def set_data(self, data):
        self.data = data
        return True

    @classmethod
    def get_data(self):
        return self.data

    # 各ページからデータを取得しインスタンス変数に格納する
    # ※予めself.set_urls()を実行しておくこと
    @classmethod
    def load(self):
        for k, v in self.urls.items():
            page_text = self.get_page_text(v)
            if not page_text: return False # Error
            page_data = getattr(self, "parse_" + k + "_page")(page_text)
            if not page_data: return False # Error
            self.data.update(page_data)
        return True

    # 各ページからデータを取得しインスタンス変数に格納する
    # ※予めself.load()を実行しておくこと
    @classmethod
    def to_csv(self):
        # 出力項目の一覧 ※順序に注意
        keys = [
            'prefCd',
            'kani_detail',
            'feature_detail',
            'kihon_detail',
            'unei_detail',
            'original_detail'
        ]

        # %演算子用のフォーマット文字列
        template = ','.join(map(lambda k: '"%(' + k + ')s"', keys))

        # %演算子用のdict型引数
        # ※余分なkeyが存在するのは問題なし
        # ※必要なkeyが存在しないとKeyErrorになる
        items = dict.fromkeys(keys, "")
        items.update(self.data)

        return template % items

    #
    # 静的メソッド
    #

    # 「事業所の概要」ページのURLから他のページのURLを作成する
    @staticmethod
    def generate_urls(url):
        base = "https://www.kaigokensaku.mhlw.go.jp"
        kani_pattern = r"/([0-9]+)/.+_detail_([0-9]+)_kani.+JigyosyoCd=([0-9\-]+)&ServiceCd=([0-9]+)"
        m = re.search(kani_pattern, url)
        if not m: return None
        urls = {
            'kani'    : base + "/%s/index.php?action_kouhyou_detail_%s_kani=true&JigyosyoCd=%s&ServiceCd=%s"        %  m.group(1,2,3,4),
            'feature' : base + "/%s/index.php?action_kouhyou_detail_feature_index=true&JigyosyoCd=%s&ServiceCd=%s"  %  m.group(1  ,3,4),
            'kihon'   : base + "/%s/index.php?action_kouhyou_detail_%s_kihon=true&JigyosyoCd=%s&ServiceCd=%s"       %  m.group(1,2,3,4),
            'unei'    : base + "/%s/index.php?action_kouhyou_detail_%s_unei=true&JigyosyoCd=%s&ServiceCd=%s"        %  m.group(1,2,3,4),
            'original': base + "/%s/index.php?action_kouhyou_detail_original_index=true&JigyosyoCd=%s&ServiceCd=%s" %  m.group(1,  3,4)}
        return urls

    # Webページからデータを取得する
    @staticmethod
    def get_page_text(url):
        response = requests.get(url)
        if response.status_code != 200: return None # Error
        return response.text

    # 「事業所の概要」ページのHTMLを解析してデータを取得する
    @staticmethod
    def parse_kani_page(page_text):
        data = {'kani': True}
        # TODO: 実装
        soup = BeautifulSoup(page_text, 'html.parser')
        if not soup.select_one('title'): return None # Error

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

        data['kani_01'] = {
            '利用者の権利擁護': '5.0',
            'サービスの質の確保への取組': '5.0',
            '相談・苦情等への対応': '5.0',
            '外部機関等との連携': '5.0',
            '事業運営・管理': '5.0',
            '安全・衛生管理等': '5.0',
            '従業者の研修等': '4.0'
        } # TODO:修正

        # 詳細情報の表を動的に解析する
        for i in range(1,2):
            elements = soup.select('div#tableGroup-' + str(i) + ' table tr')
            if not elements: continue
            data['kani_table' + str(i)] = DetailPages.parse_kani_table(elements)

        return data


    # 「事業所の概要」ページに複数個存在する複雑な表を解析してデータを取得する
    # ※要件が複雑なのでバグる可能性が高い。要注意！要テスト！！
    # @param1 trs: BeautifulSoup().select()で取得した<tr>タグのリスト
    # @return: dict型で整形したデータ
    @staticmethod
    def parse_kani_table(trs):
        if not trs: return None

        # 変数を初期化
        data = {}
        rowspan_count = []
        rowspan_ths = []

        # <tr> 1行ごとに逐次処理
        for tr in trs:

            # <th>からkeyを生成、複数行にまたがるセルの値を引き回す
            local_ths = tr.select('th')
            if local_ths[0].get('rowspan'):
                rowspan_count.append(int(local_ths[0].get('rowspan')) - 1)
                revised_ths = rowspan_ths + local_ths
                rowspan_ths.append(local_ths[0])
            else:
                revised_ths = rowspan_ths + local_ths
            k = '__'.join([th.get_text().replace('\n',' ').strip() for th in revised_ths])

            # <td>からvalueを生成、テキストが空かつ画像があれば1つ目のalt値を取得する
            td = tr.select_one('td')
            v = td.get_text().replace('\n',' ').strip()
            if not v and td.select_one('img'): v = td.select_one('img').get('alt').strip()

            # dictに追加
            data[k] = v

        return data

    # 「事業所の特色」ページのHTMLを解析してデータを取得する
    @staticmethod
    def parse_feature_page(page_text):
        data = {'feature': True}
        # TODO: 実装
        if True == False: return None # Error
        return data

    # 「事業所の詳細」ページのHTMLを解析してデータを取得する
    @staticmethod
    def parse_kihon_page(page_text):
        data = {'kihon': True}
        # TODO: 実装
        if True == False: return None # Error
        return data

    # 「運営状況」ページのHTMLを解析してデータを取得する
    @staticmethod
    def parse_unei_page(page_text):
        data = {'unei': True}
        # TODO: 実装
        if True == False: return None # Error
        return data

    # 「その他」ページのHTMLを解析してデータを取得する
    @staticmethod
    def parse_original_page(page_text):
        data = {'original': True}
        # TODO: 実装
        if True == False: return None # Error
        return data

