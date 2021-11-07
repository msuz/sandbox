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

    def test_to_csv(self):
        d = DetailPages(self.URL)
        data = {'prefCd': '01'}
        expect = '"01",""'
        d.set_data(data)
        result = d.to_csv()
        self.assertEqual(result, expect)

        data = {'prefCd': '01', 'jigyosyoCd': {'a': '1'}}
        expect = '"01","{\'a\': \'1\'}"'
        d.set_data(data)
        result = d.to_csv()
        self.assertEqual(result, expect)

    def test_get_page_text(self):
        d = DetailPages(self.URL)
        page_text = d.get_page_text(self.URLS['kani'])
        self.assertTrue(self.URL_JIGYOSHO_NAME in page_text)