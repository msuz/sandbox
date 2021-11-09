# coding: UTF-8

from unittest import TestCase
from kaigokensaku.unei_page import UneiPage
from bs4 import BeautifulSoup

class TestUneiPage(TestCase):

    def test_parse(self):
        f = open('testdata/unei.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        data = UneiPage.parse(page_text)

        self.assertEqual(data, {'dummy_key': 'dummy_value'})
