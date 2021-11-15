# coding: UTF-8

from unittest import TestCase
from kaigokensaku.original_page import OriginalPage
from bs4 import BeautifulSoup

class TestOriginalPage(TestCase):

    def test_parse(self):
        f = open('testdata/original.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        data = OriginalPage.parse(page_text)

        self.assertEqual(data, {'key': 'value'})
