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

    def __test_load(self):
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
        expect = '"01","","","","",""'
        d.set_data(data)
        result = d.to_csv()
        self.assertEqual(result, expect)

        data = {'prefCd': '01', 'kani_detail': {'a': '1'}}
        expect = '"01","{\'a\': \'1\'}","","","",""'
        d.set_data(data)
        result = d.to_csv()
        self.assertEqual(result, expect)

    def __test_get_page_text(self):
        d = DetailPages(self.URL)
        page_text = d.get_page_text(self.URLS['kani'])
        self.assertTrue(self.URL_JIGYOSHO_NAME in page_text)

    def test_parse_kani_page(self):
        d = DetailPages(self.URL)
        f = open('testdata/kani.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        data = d.parse_kani_page(page_text)
        self.assertEqual(data['kani'], True)
        self.assertEqual(data['prefCd'], '01')
        self.assertEqual(data['jigyosyoCd'], '0171000268-00')
        self.assertEqual(data['serviceCd'], '320')
        self.assertEqual(data['versionCd'], '022')
        self.assertEqual(data['prefName'], '北海道')
        self.assertEqual(data['jigyosyoName'], 'グループホームほのぼのさくら')
        self.assertEqual(data['serviceName'], '認知症対応型共同生活介護')

        self.assertEqual(data['postalCode'], '067-0074')
        self.assertEqual(data['jigyosyoAddress'], '北海道江別市高砂町32番地の５　グループホームほのぼのさくら')
        self.assertEqual(data['latitudeLongitude'], '43.101892000000000,141.539210599999930')
        self.assertEqual(data['tel'], '011-384-0123')
        self.assertEqual(data['fax'], '011-384-0157')
        #self.assertEqual(data['homepage'], 'https://www.example.com/')

        self.assertEqual(data['kani_01'], {
            '利用者の権利擁護': '5.0',
            'サービスの質の確保への取組': '5.0',
            '相談・苦情等への対応': '5.0',
            '外部機関等との連携': '5.0',
            '事業運営・管理': '5.0',
            '安全・衛生管理等': '5.0',
            '従業者の研修等': '4.0'
        })

        self.assertEqual(data['kani_table1'], {
            '運営方針': '利用者様の心に寄り添った介護・家族同様な生活',
            '事業開始年月日': '2005/10/24',
            '協力医療機関': '内藤クリニック'
        })

    def test_parse_kani_table01(self):
        d = DetailPages(self.URL)
        f = open('testdata/kani_table01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        trs = soup.select('tr')
        data = d.parse_kani_table(trs)
        self.assertEqual(data, {
            '運営方針': '利用者様の心に寄り添った介護・家族同様な生活',
            '事業開始年月日': '2005/10/24',
            '協力医療機関': '内藤クリニック'
        })

    def test_parse_kani_table02(self):
        d = DetailPages(self.URL)
        f = open('testdata/kani_table02.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        trs = soup.select('tr')
        data = d.parse_kani_table(trs)
        self.assertEqual(data, {
            '短期利用認知症対応型共同生活介護の提供': 'なし',
            '入居条件': 'ない',
            '退居条件': '入院3ヶ月超えの場合',
            'サービスの特色': '利用者さんが介護職員と共に家族として介護を心がけている',
            '運営推進会議の開催状況__開催実績': '年6回',
            '運営推進会議の開催状況__延べ参加者数': '36人',
            '運営推進会議の開催状況__協議内容': '利用者さんの近況、レク、健康状況等'
        })

    def test_parse_feature_page(self):
        d = DetailPages(self.URL)
        f = open('testdata/feature.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        page_data = d.parse_feature_page(page_text)
        self.assertEqual(page_data['feature'], True)

    def test_parse_kihon_page(self):
        d = DetailPages(self.URL)
        f = open('testdata/kihon.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        page_data = d.parse_kihon_page(page_text)
        self.assertEqual(page_data['kihon'], True)

    def test_parse_unei_page(self):
        d = DetailPages(self.URL)
        f = open('testdata/unei.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        page_data = d.parse_unei_page(page_text)
        self.assertEqual(page_data['unei'], True)

    def test_parse_original_page(self):
        d = DetailPages(self.URL)
        f = open('testdata/original.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        page_data = d.parse_original_page(page_text)
        self.assertEqual(page_data['original'], True)
