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
        self.assertEqual(data['空き人数'], '空き数/定員 0/9人 定員9人中、現在の空き数0人です。（2021年10月29日時点）')
        self.assertEqual(data['サービスの内容に関する自由記述'], 'カラオケ・散歩と行っています・各レク・町内のお祭り参加・庭にてバーベキュー・花火大会等の実績があります')
        self.assertEqual(data['サービスの質の向上に向けた取組'], '他の施設のサービス等を参考により良いサービスを心掛けております。')
        self.assertEqual(data['賃金改善以外で取り組んでいる処遇改善の内容'], {'key1': 'value1', 'key2': 'value2'}) # TODO
        self.assertEqual(data['併設されているサービス'], '利用者さんの心に寄り添う介護を心掛けてます、家族と同様な生活を心掛けています。')
        self.assertEqual(data['保険外の利用料等に関する自由記述'], '理・美容やおむつ等は保険外としてサービスしております。')
        self.assertEqual(data['従業員の男女比'], {"male": 1, "female": 7})
        self.assertEqual(data['従業員の年齢構成'], {"20代": 2, "30代": 0, "40代": 0, "50代": 6, "60代〜": 0})
        self.assertEqual(data['従業員の特色に関する自由記述'], '当職員はベテラン者が多く介護のスキルはある方です。 ∴個々の利用者さんに合った介護ができることが当施設の特徴と思う')
        self.assertEqual(data['利用者の男女比'], {"male": 2, "female": 7})
        self.assertEqual(data['利用者の年齢構成'], {"〜64歳": 0, "65〜74歳": 2, "75〜84歳": 2, "85〜94歳": 5, "95歳〜": 0})
        self.assertEqual(data['利用者の特色に関する自由記述'], '利用者さんは皆さん仲が良く、洗濯物を干したり手伝ってくれます。')
        self.assertEqual(data['勤務時間'], '社員の都合に合わせてシフトを組んでおります。')
        self.assertEqual(data['賃金体系'], '周辺の施設等を参考にしております、処遇改善加算・特定処遇改善加算を取得しており職員には対応しています。')
        self.assertEqual(data['休暇制度の内容および取得状況'], '休暇は可能な限り連続でとれるように会社として努力しています、当施設の職員は全員１００％有給消化しております。')
        self.assertEqual(data['福利厚生の状況'], '社会保険等・懇親会など')
        self.assertEqual(data['離職率'], '当施設は≒２０％')
