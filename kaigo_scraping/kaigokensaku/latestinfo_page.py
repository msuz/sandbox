# coding: UTF-8

import re
import json
import requests
from bs4 import BeautifulSoup, NavigableString

class LatestinfoPage:

    # 「新着情報」ページを解析してデータを取得する
    # @param1: 都道府県番号 1〜47
    # @return: dict型で整形したデータ
    @classmethod
    def get(cls, pref_no):
        if not(pref_no >= 1 and pref_no <= 47): return None # Error
        url = 'https://www.kaigokensaku.mhlw.go.jp/%02d/index.php?action_kouhyou_pref_latestinfo_list=true' % pref_no
        response = requests.get(url)
        if response.status_code != 200: return None # Error
        return cls.parse(response.text)

    # 「新着情報」ページを解析してデータを取得する
    # @param1: HTMLテキスト
    # @return: dict型で整形したデータ
    @classmethod
    def parse(cls, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        if not soup.select_one('title'): return None # Error

        trs = soup.select('div#newlist table tbody tr')
        if not trs: return [] # No contents
        data = [ cls.parse_tr(tr) for tr in trs ]
        return data

    # <tr>の値をdict型で返す
    # @param1 tr: BeautifulSoup().select_one()で取得した<tr>タグ
    # @return: dict型で整形したデータ
    @staticmethod
    def parse_tr(tr):
        if not tr: return None # Error
        a = tr.select_one('a.listJigyosyoName')
        if not a: return None # Error
        if not a.has_attr('onclick'): return None # Error
        onclick = a.get_attribute_list('onclick')[0]
        url_relative = re.sub(r"^.*location.href='(.*)'.*$", r'\1', onclick)
        return {'url': url_relative}
