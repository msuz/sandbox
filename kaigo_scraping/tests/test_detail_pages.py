# coding: UTF-8

from unittest import TestCase
from kaigokensaku.detail_pages import DetailPages
#import re
#import requests
from bs4 import BeautifulSoup

class TestDetailPages(TestCase):
    URL = 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0113513220-00&ServiceCd=110'
    URL_RELATIVE   = '/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0113513220-00&ServiceCd=110'
    URLS = {
        'kani': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0113513220-00&ServiceCd=110',
        'feature': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_feature_index=true&JigyosyoCd=0113513220-00&ServiceCd=110',
        'kihon': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kihon=true&JigyosyoCd=0113513220-00&ServiceCd=110',
        'unei': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_unei=true&JigyosyoCd=0113513220-00&ServiceCd=110',
        'original': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_original_index=true&JigyosyoCd=0113513220-00&ServiceCd=110'}
    URL_JIGYOSHO_NAME = '皆川病院訪問介護事業所みらく'

    def test_init_urls(self):
        d = DetailPages(self.URL) # set_urls() called
        self.assertEqual(d.get_urls(), self.URLS)
        self.assertEqual(d.get_url('original'), self.URLS['original'])
        self.assertEqual(d.get_url('__dummy__'), None) # error handling

    def test_generate_urls(self):
        urls = DetailPages.generate_urls(self.URL)
        self.assertEqual(urls, self.URLS)

        urls = DetailPages.generate_urls(self.URL_RELATIVE)
        self.assertEqual(urls, self.URLS)

        url = 'http://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_035_kani=true&JigyosyoCd=01B3700015-00&ServiceCd=551'
        urls = {
            'kani': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_035_kani=true&JigyosyoCd=01B3700015-00&ServiceCd=551',
            'feature': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_feature_index=true&JigyosyoCd=01B3700015-00&ServiceCd=551',
            'kihon': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_035_kihon=true&JigyosyoCd=01B3700015-00&ServiceCd=551',
            'unei': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_035_unei=true&JigyosyoCd=01B3700015-00&ServiceCd=551',
            'original': 'https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_original_index=true&JigyosyoCd=01B3700015-00&ServiceCd=551'}
        result = DetailPages.generate_urls(url)
        self.assertEqual(result, urls)

    def test_load(self):
        d = DetailPages(self.URL)
        result = d.load()
        self.assertTrue(result)
        data = d.get_data()
        self.assertEqual(data['kani'], True)
        self.assertEqual(data['feature'], True)
        self.assertEqual(data['kihon'], True)
        self.assertEqual(data['unei'], True)
        self.assertEqual(data['original'], True)
        self.assertEqual(data['latitudeLongitude'], '42.408990800000000,141.103421000000020')

    def test_get_csv_header(self):
        expect = '"prefCd","prefName","jigyosyoCd","jigyosyoName","serviceCd","serviceName","versionCd",'\
            '"postalCode","jigyosyoAddress","latitudeLongitude","tel","fax","homepage","uneiJokyo","jigyosyoTaiyou","serviceNaiyo","riyoryo","jugyoinInfo","riyosyaInfo","sonota",'\
            '"ukeireNinzu","serviceNaiyoText","serviceHinsitsuText","syoguKaizen","heisetsuService","hokengaiRiyoryoText","jugyoinSexRate","jugyoinAgeRate","jugyoinText","riyosyaSexRate","riyosyaAgeRate","riyosyaText",'\
            '"kihon_1","kihon_1_2","kihon_2","kihon_3","kihon_4","kihon_5",'\
            '"unei_1","unei_2","unei_3","unei_4","unei_5","unei_6","unei_7","unei_8","unei_9","unei_10",'\
            '"original"'
        result = DetailPages.get_csv_header()
        self.assertEqual(result, expect)

        keys = ['prefCd', '受け入れ可能人数', '４．介護サービスの内容に関する事項']
        expect = '"prefCd","ukeireNinzu","kihon_4"'
        result = DetailPages.get_csv_header(keys)
        self.assertEqual(result, expect)

    def test_to_csv(self):
        d = DetailPages(self.URL)
        keys = ['prefCd','jigyosyoCd']
        data = {'prefCd': '01'}
        expect = '"01",""'
        d.set_data(data)
        result = d.to_csv(keys)
        self.assertEqual(result, expect)

        keys = ['prefCd','jigyosyoCd']
        data = {'prefCd': '01', 'jigyosyoCd': {'a': '1'}}
        expect = '"01","{\'a\': \'1\'}"'
        d.set_data(data)
        result = d.to_csv(keys)
        self.assertEqual(result, expect)

    def test_get_page_text(self):
        d = DetailPages(self.URL)
        page_text = d.get_page_text(self.URLS['kani'])
        self.assertTrue(self.URL_JIGYOSHO_NAME in page_text)