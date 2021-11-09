# coding: UTF-8

from unittest import TestCase
from kaigokensaku.kihon_page import KihonPage
from bs4 import BeautifulSoup

class TestKihonPage(TestCase):

    def test_parse(self):
        f = open('testdata/kihon.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        data = KihonPage.parse(page_text)

        self.assertEqual(data, {'dummy_key': 'dummy_value'})
