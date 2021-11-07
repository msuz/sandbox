# coding: UTF-8

from unittest import TestCase
from kaigokensaku.kani_page import KaniPage
from bs4 import BeautifulSoup

class TestKaniPage(TestCase):

    def test_parse(self):
        f = open('testdata/kani.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        data = KaniPage.parse(page_text)

        self.assertEqual(data['prefCd'], '01')
        self.assertEqual(data['jigyosyoCd'], '0171000268-00')
        self.assertEqual(data['serviceCd'], '320')
        self.assertEqual(data['versionCd'], '022')

        self.assertEqual(data['radar_chart'], {
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

    def test_parse_basic_info(self):
        f = open('testdata/kani.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        data = KaniPage.parse_basic_info(soup)

        self.assertEqual(data['prefCd'], '01')
        self.assertEqual(data['jigyosyoCd'], '0171000268-00')
        self.assertEqual(data['serviceCd'], '320')
        self.assertEqual(data['versionCd'], '022')
        self.assertEqual(data['prefName'], '北海道')
        self.assertEqual(data['jigyosyoName'], 'グループホームほのぼのさくら')
        self.assertEqual(data['serviceName'], '認知症対応型共同生活介護')

        self.assertEqual(data['postalCode'], '067-0074')
        self.assertEqual(data['jigyosyoAddress'], '北海道江別市高砂町32番地の５　グループホームほのぼのさくら') # '　' = '\u3000
        self.assertEqual(data['latitudeLongitude'], '43.101892000000000,141.539210599999930')
        self.assertEqual(data['tel'], '011-384-0123')
        self.assertEqual(data['fax'], '011-384-0157')
        #self.assertEqual(data['homepage'], 'https://www.example.com/')

    def test_parse_kani_table01(self):
        f = open('testdata/kani_table01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        trs = soup.select('tr')
        data = KaniPage.parse_table(trs)
        self.assertEqual(data, {
            '運営方針': '利用者様の心に寄り添った介護・家族同様な生活',
            '事業開始年月日': '2005/10/24',
            '協力医療機関': '内藤クリニック'
        })

    def test_parse_radar_chart(self):
        f = open('testdata/kani_script01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        script = soup.select_one('script')
        data = KaniPage.parse_radar_chart(script)
        self.assertEqual(data, {
            '利用者の権利擁護': '5.0',
            'サービスの質の確保への取組': '5.0',
            '相談・苦情等への対応': '5.0',
            '外部機関等との連携': '5.0',
            '事業運営・管理': '5.0',
            '安全・衛生管理等': '5.0',
            '従業者の研修等': '4.0'
        })

    def test_parse_kani_table02(self):
        f = open('testdata/kani_table02.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        trs = soup.select('tr')
        data = KaniPage.parse_table(trs)
        self.assertEqual(data, {
            '短期利用認知症対応型共同生活介護の提供': 'なし',
            '入居条件': 'ない',
            '退居条件': '入院3ヶ月超えの場合',
            'サービスの特色': '利用者さんが介護職員と共に家族として介護を心がけている',
            '運営推進会議の開催状況__開催実績': '年6回',
            '運営推進会議の開催状況__延べ参加者数': '36人',
            '運営推進会議の開催状況__協議内容': '利用者さんの近況、レク、健康状況等'
        })

    def test_parse_kani_table03(self):
        f = open('testdata/kani_table03.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        trs = soup.select('tr')
        data = KaniPage.parse_table(trs)
        self.assertEqual(data, {
            '居室の状況__二人部屋': 'なし',
            '消火設備の有無': 'あり'
        })

    def test_parse_kani_table04(self):
        f = open('testdata/kani_table04.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        trs = soup.select('tr')
        data = KaniPage.parse_table(trs)
        self.assertEqual(data, {
            '家賃（月額）': '85,000円',
            '敷金': '円',
            '保証金（入居時前払金）の金額': '円',
            '保証金の保全措置の内容': '',
            '償却の有無': 'なし'
        })

    def test_parse_kani_table05(self):
        f = open('testdata/kani_table05.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        trs = soup.select('tr')
        data = KaniPage.parse_table(trs)
        self.assertEqual(data, {
            '総従業者数': '9人',
            '計画作成担当者数__常勤': '1人',
            '計画作成担当者数__非常勤': '0人',
            '介護職員数__常勤': '6人',
            '介護職員数__非常勤': '0人',
            '介護職員の退職者数__常勤': '2人',
            '介護職員の退職者数__非常勤': '0人',
            '看護師数__常勤': '0人',
            '看護師数__非常勤': '1人',
            '経験年数５年以上の介護職員の割合': '100％',
            '夜勤を行う従業者数': '3人',
        })

    def test_parse_kani_table06(self):
        f = open('testdata/kani_table06.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        trs = soup.select('tr')
        data = KaniPage.parse_table(trs)
        self.assertEqual(data, {
            '利用定員　※＜＞内の数値は都道府県平均': '1ユニット9人＜14.8人＞', # '　' = '\u3000'
            '入居率': '90％',
            '入居者の平均年齢': '82歳',
            '入居者の男女別人数': '男性：2人 女性：7人',
            '要介護度別入所者数__要支援２': '0人',
            '要介護度別入所者数__要介護１': '4人',
            '要介護度別入所者数__要介護２': '0人',
            '要介護度別入所者数__要介護３': '3人',
            '要介護度別入所者数__要介護４': '1人',
            '要介護度別入所者数__要介護５': '1人',
            '昨年度の退所者数': '2人'
        })