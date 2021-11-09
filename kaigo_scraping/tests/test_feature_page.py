# coding: UTF-8

from unittest import TestCase
from kaigokensaku.feature_page import FeaturePage
from bs4 import BeautifulSoup

class TestFeaturePage(TestCase):

    def test_parse(self):
        f = open('testdata/feature.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        data = FeaturePage.parse(page_text)

        self.assertEqual(data, {'dummy_key': 'dummy_value'})
