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

        self.assertEqual(data, {'key': 'value'})

    def test_parse_kihon_table01(self):
        f = open('testdata/kihon_table01_01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        trs = soup.select('tr')
        data = KihonPage.parse_table(trs)
        self.maxDiff = None

        self.assertEqual(data, {
            '法人等の名称__法人等の種類': 'ＮＰＯ法人',
            '法人等の名称__（その他の場合、その名称）': '',
            '法人等の名称__名称__（ふりがな）': 'とくていひえいりかつどうほうじんたくみしょうや',
            '法人等の名称__名称__l1': '特定非営利活動法人匠笑屋',
            '法人等の名称__法人番号の有無': '法人番号あり（非公表）',
            '法人等の名称__法人番号': '',
            '法人等の主たる事務所の所在地': '〒067-0074',
            '法人等の主たる事務所の所在地__l1': '北海道江別市高砂町32番地の５',
            '法人等の連絡先__電話番号': '011-384-0123',
            '法人等の連絡先__ＦＡＸ番号': '011-384-0157',
            '法人等の連絡先__ホームページ': 'なし',
            '法人等の代表者の氏名及び職名__氏名': '小松田　久雄', # '　' = '\u3000'
            '法人等の代表者の氏名及び職名__職名': '理事長',
            '法人等の設立年月日': '2005/10/24'
        })