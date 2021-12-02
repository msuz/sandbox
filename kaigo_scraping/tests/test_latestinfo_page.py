# coding: UTF-8

from unittest import TestCase
from kaigokensaku.latestinfo_page import LatestinfoPage
from bs4 import BeautifulSoup

class TestLatestinfoPage(TestCase):

    def test_get(self):
        data = LatestinfoPage.get(1)
        if data:
            self.assertEqual(type(data), list)
            self.assertTrue('url' in data[0].keys())
            self.assertTrue('url' in data[-1].keys())
        else:
            self.assertEqual(data is None)

    def test_parse(self):
        f = open('testdata/latestinfo.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('新着情報' in page_text)

        data = LatestinfoPage.parse(page_text)

        self.maxDiff = None # テスト結果のデバッグ出力強化

        self.assertEqual(len(data), 1910)
        self.assertEqual(data[0]['url'], '/01/index.php?action_kouhyou_detail_009_kani=true&JigyosyoCd=0111013561-00&ServiceCd=160')
        self.assertEqual(data[-1]['url'], '/01/index.php?action_kouhyou_detail_025_kani=true&JigyosyoCd=0171500283-00&ServiceCd=210')
