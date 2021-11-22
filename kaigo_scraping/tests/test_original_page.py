# coding: UTF-8

from unittest import TestCase
from kaigokensaku.original_page import OriginalPage
from bs4 import BeautifulSoup

class TestOriginalPage(TestCase):

    def test_parse_empty(self):
        f = open('testdata/original_01-0171000268-00-022.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        data = OriginalPage.parse(page_text)

        self.assertEqual(data, {'都道府県もしくは政令指定都市ごとに設けている項目': '現在、情報がありません。'})


    def test_parse(self):
        f = open('testdata/original_37-3751180047-00-028.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('老人保健施設　さわやか荘' in page_text)
        data = OriginalPage.parse(page_text)

        self.assertEqual(data, {'都道府県もしくは政令指定都市ごとに設けている項目': {
            '処分・指導に関する情報 - 処分が行われた日': '-',
            '処分・指導に関する情報 - 当該処分に対する事業所の取組状況': '-',
            '処分・指導に関する情報 - 当該処分の内容': '-',
            '処分・指導に関する情報 - 当該行政指導に対する事業所の取組状況': '-',
            '処分・指導に関する情報 - 当該行政指導の内容': '-',
            '処分・指導に関する情報 - 行政指導（勧告を含む。以下同じ。）が行われた日': '-'
        }})