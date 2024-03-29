# coding: UTF-8

from unittest import TestCase
from kaigokensaku.feature_page import FeaturePage
from bs4 import BeautifulSoup

class TestFeaturePage(TestCase):

    def test_parse(self):
        f = open('testdata/feature_01-0171000268-00-022.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        data = FeaturePage.parse(page_text)
        self.assertEqual(data['空き人数'], '空き数/定員 0/9人 定員9人中、現在の空き数0人です。（2021年10月29日時点）')
        self.assertEqual(data['サービスの内容に関する自由記述'], 'カラオケ・散歩と行っています・各レク・町内のお祭り参加・庭にてバーベキュー・花火大会等の実績があります')
        self.assertEqual(data['サービスの質の向上に向けた取組'], '他の施設のサービス等を参考により良いサービスを心掛けております。')
        self.assertEqual(data['賃金改善以外で取り組んでいる処遇改善の内容'], {
            '入職促進に向けた取組': '法人や事業所の経営理念やケア方針・人材育成方針、その実現のための施策・仕組みなどの明確化 他産業からの転職者、主婦層、中高年齢者等、経験者・有資格者等にこだわらない幅広い採用の仕組みの構築',
            '資質の向上やキャリアアップに向けた支援': '働きながら介護福祉士取得を目指す者に対する実務者研修受講支援や、より専門性の高い介護技術を取得しようとする者に対する喀痰吸引、認知症ケア、サービス提供責任者研修、中堅職員に対するマネジメント研修の受講支援等 エルダー・メンター（仕事やメンタル面のサポート等をする担当者）制度等導入 上位者・担当者等によるキャリア面談など、キャリアアップ等に関する定期的な相談の機会の確保',
            '両立支援・多様な働き方の推進': '職員の事情等の状況に応じた勤務シフトや短時間正規職員制度の導入、職員の希望に即した非正規職員から正規職員への転換の制度等の整備 有給休暇が取得しやすい環境の整備 業務や福利厚生制度、メンタルヘルス等の職員相談窓口の設置等相談体制の充実',
            '腰痛を含む心身の健康管理': '介護職員の身体の負担軽減のための介護技術の修得支援、介護ロボットやリフト等の介護機器等導入及び研修等による腰痛対策の実施 短時間勤務労働者等も受診可能な健康診断・ストレスチェックや、従業員のための休憩室の設置等健康管理対策の実施 雇用管理改善のための管理者に対する研修等の実施 事故・トラブルへの対応マニュアル等の作成等の体制の整備',
            '生産性向上のための業務改善の取組': 'タブレット端末やインカム等のＩＣＴ活用や見守り機器等の介護ロボットやセンサー等の導入による業務量の縮減 高齢者の活躍（居室やフロア等の掃除、食事の配膳・下膳などのほか、経理や労務、広報なども含めた介護業務以外の業務の提供）等による役割分担の明確化 業務手順書の作成や、記録・報告様式の工夫等による情報共有や作業負担の軽減',
            'やりがい・働きがいの醸成': 'ミーティング等による職場内コミュニケーションの円滑化による個々の介護職員の気づきを踏まえた勤務環境やケア内容の改善 地域包括ケアの一員としてのモチベーション向上に資する、地域の児童・生徒や住民との交流の実施 利用者本位のケア方針など介護保険や法人の理念等を定期的に学ぶ機会の提供 ケアの好事例や、利用者やその家族からの謝意等の情報を共有する機会の提供'
        })
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

    def test_parse_script_var(self):
        f = open('testdata/feature_script01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        script = soup.select_one('script')
        data = FeaturePage.parse_script_var(script, 'chartSeriallData_staff')
        self.assertEqual(data, [{'people': '', 'male': 1, 'female': 7}])
        data = FeaturePage.parse_script_var(script, 'chartSeriallData_user')
        self.assertEqual(data, [{'people': '', 'male': 2, 'female': 7}])

    def test_parse_chartSeriall(self):
        f = open('testdata/feature_script01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        script = soup.select_one('script')
        data = FeaturePage.parse_chartSeriall(script, 'chartSeriallData_staff')
        self.assertEqual(data, {"male": 1, "female": 7})
        data = FeaturePage.parse_chartSeriall(script, 'chartSeriallData_user')
        self.assertEqual(data, {"male": 2, "female": 7})

    def test_parse_legendSerialldiv_staff(self):
        f = open('testdata/feature_script01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        script = soup.select_one('script')
        data = FeaturePage.parse_legendSerialldiv_staff(script)
        self.assertEqual(data, {"male": 1, "female": 7})

    def test_parse_legendSerialldiv_user(self):
        f = open('testdata/feature_script01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        script = soup.select_one('script')
        data = FeaturePage.parse_legendSerialldiv_user(script)
        self.assertEqual(data, {"male": 2, "female": 7})

    def test_parse_chartPie(self):
        f = open('testdata/feature_script01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        script = soup.select_one('script')
        data = FeaturePage.parse_chartPie(script, 'chartPieData_staff')
        self.assertEqual(data, {"20代": 2, "30代": 0, "40代": 0, "50代": 6, "60代〜": 0})
        data = FeaturePage.parse_chartPie(script, 'chartPieData_user')
        self.assertEqual(data, {"〜64歳": 0, "65〜74歳": 2, "75〜84歳": 2, "85〜94歳": 5, "95歳〜": 0})

    def test_parse_legendPiediv_staff(self):
        f = open('testdata/feature_script01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        script = soup.select_one('script')
        data = FeaturePage.parse_legendPiediv_staff(script)
        self.assertEqual(data, {"20代": 2, "30代": 0, "40代": 0, "50代": 6, "60代〜": 0})

    def test_parse_legendPiediv_user(self):
        f = open('testdata/feature_script01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        script = soup.select_one('script')
        data = FeaturePage.parse_legendPiediv_user(script)
        self.assertEqual(data, {"〜64歳": 0, "65〜74歳": 2, "75〜84歳": 2, "85〜94歳": 5, "95歳〜": 0})
