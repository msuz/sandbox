# coding: UTF-8

import re
import requests
from bs4 import BeautifulSoup
from kaigokensaku.kani_page import KaniPage
from kaigokensaku.feature_page import FeaturePage
from kaigokensaku.kihon_page import KihonPage
from kaigokensaku.unei_page import UneiPage
from kaigokensaku.original_page import OriginalPage

class DetailPages:
    #
    # インスタンス変数
    #
    urls = {}
    data = {}
    csv_column_names = {
        # kani_page
        'prefCd': 'prefCd',
        'prefName': 'prefName',
        'jigyosyoCd': 'jigyosyoCd',
        'jigyosyoName': 'jigyosyoName',
        'serviceCd': 'serviceCd',
        'serviceName': 'serviceName',
        'versionCd': 'versionCd',
        'postalCode': 'postalCode',
        'jigyosyoAddress': 'jigyosyoAddress',
        'latitudeLongitude': 'latitudeLongitude',
        'tel': 'tel',
        'fax': 'fax',
        'homepage': 'homepage',
        '運営状況：レーダーチャート\u3000（ ）': 'uneiJokyo',
        '事業所概要': 'jigyosyoTaiyou',
        'サービス内容': 'serviceNaiyo',
        '利用料': 'riyoryo',
        '従業者情報': 'jugyoinInfo',
        '利用者情報': 'riyosyaInfo',
        'その他': 'sonota',
        # feature_page
        '受け入れ可能人数': 'ukeireNinzu',
        'サービスの内容に関する自由記述': 'serviceNaiyoText',
        'サービスの質の向上に向けた取組': 'serviceHinsitsuText',
        '賃金改善以外で取り組んでいる処遇改善の内容': 'syoguKaizen',
        '併設されているサービス': 'heisetsuService',
        '保険外の利用料等に関する自由記述': 'hokengaiRiyoryoText',
        '従業員の男女比': 'jugyoinSexRate',
        '従業員の年齢構成': 'jugyoinAgeRate',
        '従業員の特色に関する自由記述': 'jugyoinText',
        '利用者の男女比': 'riyosyaSexRate',
        '利用者の年齢構成': 'riyosyaAgeRate',
        '利用者の特色に関する自由記述': 'riyosyaText',
        # kihon_page
        '１．事業所を運営する法人等に関する事項': 'kihon_1',
        '１．事業所を運営する法人等に関する事項(2)': 'kihon_1_2',
        '２．介護サービスを提供し、又は提供しようとする事業所に関する事項': 'kihon_2',
        '３．事業所において介護サービスに従事する従業者に関する事項': 'kihon_3',
        '４．介護サービスの内容に関する事項': 'kihon_4',
        '５．介護サービスを利用するに当たっての利用料等に関する事項': 'kihon_5',
        # unei_page
        '1．利用者の権利擁護のための取組': 'unei_1',
        '2．利用者本位の介護サービスの提供': 'unei_2',
        '3．相談、苦情等の対応のために講じている措置': 'unei_3',
        '4．サービスの内容の評価や改善等': 'unei_4',
        '5．サービスの質の確保、透明性の確保等のための外部機関等との連携': 'unei_5',
        '6．適切な事業運営の確保': 'unei_6',
        '7．事業所の運営管理、業務分担、情報の共有等': 'unei_7',
        '8．安全管理及び衛生管理': 'unei_8',
        '9．情報の管理、個人情報保護等': 'unei_9',
        '10．その他、介護サービスの質の確保のために行っていること': 'unei_10',
        # original_page
        '都道府県もしくは政令指定都市ごとに設けている項目': 'original'
    }

    #
    # インスタンスメソッド
    #
    def __init__(self, url):
        self.set_urls(url)
        return

    def set_urls(self, url):
        self.urls = self.generate_urls(url)
        return True

    def get_urls(self):
        return self.urls

    def get_url(self, key):
        if not key in self.urls: return None
        return self.urls[key]

    def set_data(self, data):
        self.data = data
        return True

    def get_data(self):
        return self.data

    # 各ページからデータを取得しインスタンス変数に格納する
    # ※予めself.set_urls()を実行しておくこと
    # @params: なし
    # @return: bool (True:成功 / False:失敗)
    def load(self):
        for k, v in self.urls.items():
            # 各ページに対応するパーサーを動的に識別して呼び出すための準備
            # 例) KaniPage, FeaturePage,,
            cls = globals().get(k.capitalize() + 'Page')
            if not cls: return False # Error

            # Webページからデータを取得する
            page_text = self.get_page_text(v)
            if not page_text: return False # Error

            # ページを解析してデータを取得する
            page_data = cls.parse(page_text)
            if not page_data: page_data = {} # Not Error

            # インスタンス変数に値を追加する
            self.data[k] = True
            self.data.update(page_data)
        return True

    # 各ページから取得したデータをCSV形式で返す
    # ※予めself.load()を実行しておくこと
    # ※カラムの順序に注意。Python3.7以上であればdictの順序が保持される
    def to_csv(self, keys=[]):
        if not keys: # 出力項目の指定が無ければ
            keys = self.csv_column_names.keys() # 全カラム

        # %演算子用のフォーマット文字列
        template = ','.join(map(lambda k: '"%(' + k + ')s"', keys))

        # %演算子用のdict型引数
        # ※余分なkeyが存在するのは問題なし
        # ※必要なkeyが存在しないとKeyErrorになる
        items = dict.fromkeys(keys, '')
        items.update(self.data)

        return template % items

    #
    # 静的メソッド
    #

    # CSVヘッダを取得
    @classmethod
    def get_csv_header(cls, keys=[]):
        if keys:
            vs = [ v for k, v in cls.csv_column_names.items() if k in keys]
        else:
            vs = cls.csv_column_names.values()

        return ','.join(['"%s"' % k for k in vs])

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

