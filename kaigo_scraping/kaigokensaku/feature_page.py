# coding: UTF-8

import re
from bs4 import BeautifulSoup

class FeaturePage:

    # 「事業所の特色」ページを解析してデータを取得する
    # @param1: HTMLテキスト
    # @return: dict型で整形したデータ
    @staticmethod
    def parse(page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        if not soup.select_one('title'): return None # Error

        data = {'key': 'value'} # TODO: 実装
        return data
