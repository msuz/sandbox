# coding: UTF-8

import re
import requests
from bs4 import BeautifulSoup
from kaigokensaku.kani_page import KaniPage
#from kaigokensaku.feature_page import FeaturePage
#from kaigokensaku.kihon_page import KihonPage
#from kaigokensaku.unei_page import UneiPage
#from kaigokensaku.original_page import OriginalPage

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
            'jigyosyoCd'
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
        data = KaniPage.parse(page_text)
        if not data: return None
        data['kani'] = True
        return data

    # 「事業所の特色」ページのHTMLを解析してデータを取得する
    @staticmethod
    def parse_feature_page(page_text):
        data = {'key': 'value'} # TODO: 実装
        if not data: return None
        data['feature'] = True
        return data

    # 「事業所の詳細」ページのHTMLを解析してデータを取得する
    @staticmethod
    def parse_kihon_page(page_text):
        data = {'key': 'value'} # TODO: 実装
        if not data: return None
        data['kihon'] = True
        return data

    # 「運営状況」ページのHTMLを解析してデータを取得する
    @staticmethod
    def parse_unei_page(page_text):
        data = {'key': 'value'} # TODO: 実装
        if not data: return None
        data['unei'] = True
        return data

    # 「その他」ページのHTMLを解析してデータを取得する
    @staticmethod
    def parse_original_page(page_text):
        data = {'key': 'value'} # TODO: 実装
        if not data: return None
        data['original'] = True
        return data