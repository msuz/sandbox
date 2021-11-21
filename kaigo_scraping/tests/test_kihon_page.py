# coding: UTF-8

from unittest import TestCase
from kaigokensaku.kihon_page import KihonPage
from bs4 import BeautifulSoup

class TestKihonPage(TestCase):

    def test_parse(self):
        f = open('testdata/kihon_01-0171000268-00-022.html', 'r')
        page_text = f.read()
        f.close()
        self.assertTrue('グループホームほのぼのさくら' in page_text)
        data = KihonPage.parse(page_text)

        self.maxDiff = None # テスト結果のデバッグ出力強化
        self.assertEqual(list(data.keys()), [
            '１．事業所を運営する法人等に関する事項',
            '１．事業所を運営する法人等に関する事項(2)',
            '２．介護サービス（予防を含む）を提供し、又は提供しようとする事業所に関する事項',
            '３．事業所において介護サービス（予防を含む）に従事する従業者',
            '４．介護サービス（予防を含む）の内容に関する事項',
            '５．介護サービス（予防を含む）を利用するに当たっての利用料等に関する事項',
        ])
        self.assertEqual(
            data['１．事業所を運営する法人等に関する事項']['法人等の名称__法人等の種類'],
            'ＮＰＯ法人')
        self.assertEqual(
            data['１．事業所を運営する法人等に関する事項(2)']['訪問介護'],
            'なし')
        self.assertEqual(
            data['２．介護サービス（予防を含む）を提供し、又は提供しようとする事業所に関する事項']['事業所の名称'],
            'グループホームほのぼのさくら')
        self.assertEqual(
            data['３．事業所において介護サービス（予防を含む）に従事する従業者']['介護職員１人当たりの利用者数'],
            '1人')
        self.assertEqual(
            data['４．介護サービス（予防を含む）の内容に関する事項']['入院時費用'],
            'あり')
        self.assertEqual(
            data['５．介護サービス（予防を含む）を利用するに当たっての利用料等に関する事項']['敷金'],
            'なし')

    # １．事業所を運営する法人等に関する事項 
    def test_parse_kihon_table01_01(self):
        f = open('testdata/kihon_table01_01.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        table = soup.select_one('table')
        data = KihonPage.parse_table(table)

        self.maxDiff = None # テスト結果のデバッグ出力強化
        self.assertEqual(data, {
            '法人等の名称__法人等の種類': 'ＮＰＯ法人',
            '法人等の名称__（その他の場合、その名称）': '',
            '法人等の名称__名称__（ふりがな）': 'とくていひえいりかつどうほうじんたくみしょうや',
            '法人等の名称__名称': '特定非営利活動法人匠笑屋',
            '法人等の名称__法人番号の有無': '法人番号あり（非公表）',
            '法人等の名称__法人番号': '',
            '法人等の主たる事務所の所在地': '〒067-0074',
            '法人等の主たる事務所の所在地(2)': '北海道江別市高砂町32番地の５',
            '法人等の連絡先__電話番号': '011-384-0123',
            '法人等の連絡先__ＦＡＸ番号': '011-384-0157',
            '法人等の連絡先__ホームページ': 'なし',
            '法人等の代表者の氏名及び職名__氏名': '小松田　久雄', # '　' = '\u3000'
            '法人等の代表者の氏名及び職名__職名': '理事長',
            '法人等の設立年月日': '2005/10/24'
        })

    # １．事業所を運営する法人等に関する事項 後半
    def test_parse_kihon_table01_02(self):
        f = open('testdata/kihon_table01_02.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        table = soup.select_one('table')
        data = KihonPage.parse_table(table)

        self.maxDiff = None # テスト結果のデバッグ出力強化
        # 複数の <td> にまたがる値は半角スペース区切り
        self.assertEqual(data, {
            # ＜居宅サービス＞
            '訪問介護': 'なし',
            '訪問入浴介護': 'なし',
            '訪問看護': 'なし',
            '訪問リハビリテーション': 'なし',
            '居宅療養管理指導': 'なし',
            '通所介護': 'なし',
            '通所リハビリテーション': 'なし',
            '短期入所生活介護': 'なし',
            '短期入所療養介護': 'なし',
            '特定施設入居者生活介護': 'なし',
            '福祉用具貸与': 'なし',
            '特定福祉用具販売': 'なし',

            # ＜地域密着型サービス＞
            '定期巡回・随時対応型訪問介護看護': 'なし',
            '夜間対応型訪問介護': 'なし',
            '地域密着型通所介護': 'なし',
            '認知症対応型通所介護': 'なし',
            '小規模多機能型居宅介護': 'なし',
            '認知症対応型共同生活介護': 'あり 1 グループホームほのぼのさくら 北海道江別市高砂町32番地の５',
            '地域密着型特定施設入居者生活介護': 'なし',
            '地域密着型介護老人福祉施設入所者生活介護': 'なし',
            '看護小規模多機能型居宅介護（複合型サービス）': 'なし',

            # 居宅介護支援
            '居宅介護支援': 'なし',

            # ＜介護予防サービス＞
            '介護予防訪問入浴介護': 'なし',
            '介護予防訪問看護': 'なし',
            '介護予防訪問リハビリテーション': 'なし',
            '介護予防居宅療養管理指導': 'なし',
            '介護予防通所リハビリテーション': 'なし',
            '介護予防短期入所生活介護': 'なし',
            '介護予防短期入所療養介護': 'なし',
            '介護予防特定施設入居者生活介護': 'なし',
            '介護予防福祉用具貸与': 'なし',
            '特定介護予防福祉用具販売': 'なし',

            # ＜地域密着型介護予防サービス＞
            '介護予防認知症対応型通所介護': 'なし',
            '介護予防小規模多機能型居宅介護': 'なし',
            '介護予防認知症対応型共同生活介護': 'あり 1 グループホームほのぼのさくら 北海道江別市高砂町32番地の５',

            # 介護予防支援
            '介護予防支援': 'なし',

            # ＜介護保険施設＞
            '介護老人福祉施設': 'なし',
            '介護老人保健施設': 'なし',
            '介護医療院': 'なし',
            '介護療養型医療施設': 'なし',
            })

    # ２．介護サービス（予防を含む）を提供し、又は提供しようとする事業所に関する事項
    def test_parse_kihon_table02(self):
        f = open('testdata/kihon_table02.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        table = soup.select_one('table')
        data = KihonPage.parse_table(table)

        self.maxDiff = None # テスト結果のデバッグ出力強化
        self.assertEqual(data, {
            '事業所の名称__(ふりがな)': 'ぐるーぷほーむほのぼのさくら',
            '事業所の名称': 'グループホームほのぼのさくら',
            '事業所の所在地': '〒067-0074',
            '事業所の所在地__市区町村コード': '江別市',
            '事業所の所在地__（都道府県から番地まで）': '北海道江別市高砂町32番地の５',
            '事業所の所在地__（建物名・部屋番号等）': 'グループホームほのぼのさくら',
            '事業所の連絡先__電話番号': '011-384-0123',
            '事業所の連絡先__FAX番号': '011-384-0157',
            '事業所の連絡先__ホームページ': 'なし',
            '介護保険事業所番号': '0171000268',
            '事業所の管理者の氏名及び職名__氏名': '佐藤　道子', # '　' = '\u3000'
            '事業所の管理者の氏名及び職名__職名': '管理者',
            '事業の開始（予定）年月日': '2005/10/24',
            '指定の年月日__介護サービス': '2006/1/14',
            '指定の年月日__介護予防サービス': '2006/1/14',
            '指定の更新年月日（直近）__介護サービス': '2023/1/13',
            '指定の更新年月日（直近）__介護予防サービス': '2023/1/13',
            '生活保護法第５４条の２に規定する介護機関（生活保護の介護扶助を行う機関）の指定': 'なし',
            '社会福祉士及び介護福祉士法第４８条の３に規定する登録喀痰吸引等事業者': 'なし',
            '事業所までの主な利用交通手段': '自家用車'
        })

    # ３．事業所において介護サービス（予防を含む）に従事する従業者
    def test_parse_kihon_table03(self):
        f = open('testdata/kihon_table03.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        table = soup.select_one('table')
        data = KihonPage.parse_table(table)

        self.maxDiff = None # テスト結果のデバッグ出力強化
        self.assertEqual(data, {
            '管理者': '1人 0人 ― ― 1人 1人',
            '計画作成担当者': '0人 1人 0人 0人 1人 1人',
            '介護職員': '6人 0人 0人 0人 6人 6人',
            '看護職員': '0人 0人 0人 1人 1人 1人',
            'その他の従業者': '0人 0人 0人 0人 0人 0人',
            '１週間のうち、常勤の従業者が勤務すべき時間数': '160時間',
            '従業者である計画作成担当者のうち介護支援専門員の人数': '0人 1人 0人 0人',
            '介護福祉士': '2人 0人 0人 0人',
            '実務者研修': '0人 0人 0人 0人',
            '介護職員初任者研修': '5人 0人 0人 0人',
            '介護支援専門員': '0人 0人 1人 0人',
            '夜勤・宿直を行う従業者の人数__夜勤': '3人',
            '夜勤・宿直を行う従業者の人数__宿直': '0人',
            '管理者の他の職務との兼務の有無': 'あり',
            '管理者が有している当該報告に係る介護サービスに係る資格等': 'あり',
            '（資格等の名称）': '認知症管理者研修',
            '介護職員１人当たりの利用者数': '1人',
            '前年度の採用者数': '0人 0人 2人 0人',
            '前年度の退職者数': '0人 0人 2人 0人',
            '１年未満の者の人数': '0人 0人 0人 0人',
            '１年～３年未満の者の人数': '0人 0人 0人 0人',
            '３年～５年未満の者の人数': '0人 0人 0人 0人',
            '５年～１０年未満の者の人数': '0人 0人 1人 0人',
            '１０年以上の者の人数': '0人 1人 5人 0人',
            '従業者の健康診断の実施状況': 'あり',
            '（その内容）': '虐待・身体拘束等研修・お看取り当',
            'アセッサー（評価者）の人数': '0人',
            '段位取得者の人数': '人 人 人 人',
            '外部評価（介護プロフェッショナルキャリア段位制度）の実施状況': 'あり',
            '認知症介護指導者養成研修修了者の人数': '人',
            '認知症介護実践リーダー研修修了者の人数': '人',
            '認知症介護実践者研修修了者の人数': '人',
            'それ以外の認知症対応力の向上に関する研修を修了した者の人数（認知症介護基礎研修を除く）': '人'
        })

    # ４．介護サービス（予防を含む）の内容に関する事項
    def test_parse_kihon_table04(self):
        f = open('testdata/kihon_table04.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        table = soup.select_one('table')
        data = KihonPage.parse_table(table)

        self.maxDiff = None # テスト結果のデバッグ出力強化
        self.assertEqual(data, {
            '事業所の運営に関する方針': '利用者様の心に寄り添った介護・家族同様な生活',
            '介護予防および介護度進行予防に関する方針': '運動を取り入れたレク等・脳トレーニング等',
            '夜間支援体制加算（Ⅰ）': 'なし',
            '夜間支援体制加算（Ⅱ）': 'なし',
            '認知症行動・心理症状緊急対応加算': 'なし',
            '若年性認知症利用者（入居者・患者）受入加算': 'あり',
            '入院時費用': 'あり',
            '看取り介護加算（予防を除く）': 'あり',
            '医療連携体制加算（Ⅰ）（予防を除く）': 'なし',
            '医療連携体制加算（Ⅱ）（予防を除く）': 'あり',
            '医療連携体制加算（Ⅲ）（予防を除く）': 'なし',
            '退居時相談援助加算': 'なし',
            '認知症専門ケア加算（Ⅰ）': 'なし',
            '認知症専門ケア加算（Ⅱ）': 'なし',
            '生活機能向上連携加算（Ⅰ）': 'なし',
            '生活機能向上連携加算（Ⅱ）': 'なし',
            '栄養管理体制加算': 'なし',
            '口腔衛生管理体制加算': 'なし',
            '口腔・栄養スクリーニング加算': 'なし',
            '科学的介護推進体制加算': 'なし',
            'サービス提供体制強化加算（Ⅰ）': 'なし',
            'サービス提供体制強化加算（Ⅱ）': 'なし',
            'サービス提供体制強化加算（Ⅲ）': 'あり',
            '介護職員処遇改善加算（Ⅰ）': 'あり',
            '介護職員処遇改善加算（Ⅱ）': 'なし',
            '介護職員処遇改善加算（Ⅲ）': 'なし',
            '介護職員処遇改善加算（Ⅳ）': 'なし',
            '介護職員処遇改善加算（Ⅴ）': 'なし',
            '介護職員等特定処遇改善加算（Ⅰ）': 'なし',
            '介護職員等特定処遇改善加算（Ⅱ）': 'あり',
            '短期利用認知症対応型共同生活介護の提供': 'なし',
            '共用型指定認知症対応型通所介護の提供': 'なし',
            '協力医療機関の名称': '内藤クリニック',
            '（協力の内容）': '日常・休日・夜間の対応', # keyがイマイチ
            '協力歯科医療機関': 'なし',
            '（その名称）': '', # keyがイマイチ
            '（協力の内容）(2)': '', # keyがイマイチ
            '看護師の確保方法': '職員として配置',
            '（契約の場合、契約先の名称）': '', # keyがイマイチ
            'バックアップ施設の名称': '介護老人保健施設はるにれ・特別養護老人ホームひだまり大麻',
            '（協力の内容）(3)': '重度の利用者の受け入れ 災害時の受け入れ', # keyがイマイチ
            # 運営推進会議の開催状況（前年度）
            '（開催実績）': '年6回', # keyがイマイチ
            '（開催実績）__（参加者延べ人数）': '36人', # keyがイマイチ
            '（協議内容等）': '利用者さんの近況、レク、健康状況等', # keyがイマイチ
            '地域・市町村との連携状況': '災害時の避難協力等 お祭りの参加 町内会の参加',
            '利用に当たっての条件': 'ない',
            '退居に当たっての条件': '入院3ヶ月超えの場合',
            '入居定員': '1ユニット9人',
            # 認知症対応型共同生活介護の入居者の状況
            '６５歳以上７５歳未満': '0人 0人 0人 0人 0人 0人 0人',
            '６５歳未満': '0人 0人 0人 0人 0人 0人 0人',
            '７５歳以上８５歳未満': '0人 4人 0人 0人 0人 0人 4人',
            '８５歳以上': '0人 0人 0人 3人 1人 1人 5人',
            '入居者の平均年齢': '82歳',
            '入居者の男女別人数__男性': '2人', # keyがイマイチ
            '入居者の男女別人数__男性__女性': '7人', # keyがイマイチ
            '入居率（一時的に不在となっている者を含む）': '90％',
            # 認知症対応型共同生活介護を退居した者の人数（前年度）
            '自宅等': '0人 0人 0人 0人 0人 0人 0人',
            '介護保険施設': '0人 0人 0人 0人 0人 0人 0人',
            '特別養護老人ホーム以外の社会福祉施設': '0人 0人 0人 1人 0人 0人 1人',
            '医療機関': '0人 0人 0人 0人 1人 0人 1人',
            '死亡者': '0人 0人 0人 0人 0人 0人 0人',
            'その他': '0人 0人 0人 0人 0人 0人 0人',
            # 入居者の入居期間
            '入居者数': '1人 0人 3人 3人 2人 0人',
            '建物形態': '単独型',
            '建物構造': '簡易耐火構造造り1階建ての1階部分',
            '広さ等': '740.350㎡ 224.306㎡ 10.046㎡',
            '二人部屋の有無': 'なし',
            '共同便所の設置数__男子便所': '2か所',
            '共同便所の設置数__男子便所__（うち車いす等の対応が可能な数）': '2か所',
            '共同便所の設置数__女子便所': '2か所',
            '共同便所の設置数__女子便所__（うち車いす等の対応が可能な数）': '2か所',
            '共同便所の設置数__男女共用便所': '1か所',
            '共同便所の設置数__男女共用便所__（うち車いす等の対応が可能な数）': '1か所',
            '個室の便所の設置数': '0か所',
            '個室の便所の設置数__（うち車いす等の対応が可能な数）': '0か所',
            '個室の便所の設置数__（個室における便所の設置割合）': '0％',
            # 浴室の設備状況
            '浴室の総数': '1か所', # keyがイマイチ
            '個浴__大浴槽__特殊浴槽__リフト浴': '1か所 0か所 0か所 0か所', # keyがイマイチ
            'その他の浴室の設備の状況': 'なし',
            '居間、食堂、台所の設備状況': '居間・食堂兼用 台所１ヶ所',
            '入居者等が調理を行う設備状況': 'あり',
            'その他の共用施設の設備状況': 'あり',
            '（その内容）': '洗濯室。事務所', # keyがイマイチ
            # バリアフリーの対応状況
            '（その内容）(2)': '全室バリアフリー', # keyがイマイチ
            '消火設備等の状況': 'あり',
            '（その内容）(3)': '自火報設備・スプリンクラー設備・消防機関への自動通報装置・消火器', # keyがイマイチ
            '緊急通報装置の設置状況': 'なし',
            '外線電話回線の設置状況': '一部あり',
            'テレビ回線の設置状況': '各居室内にあり',
            # 事業所の敷地に関する事項
            '敷地の面積': '740.350㎡',
            '事業所を運営する法人が所有': 'なし',
            '抵当権の設定': 'なし',
            '貸借（借地）': 'あり',
            '契約期間__始': '2004/1/1',
            '契約期間__始__終': '2019/12/31',
            '契約の自動更新': 'なし',
            # 事業所の建物に関する事項
            '建物の延床面積': '224.306㎡',
            '事業所を運営する法人が所有(2)': 'なし', # keyがイマイチ
            '抵当権の設定(2)': 'なし', # keyがイマイチ
            '貸借（借家）': 'あり',
            '契約期間__始(2)': '2004/1/1', # keyがイマイチ
            '契約期間__始__終(2)': '2019/12/31', # keyがイマイチ
            '契約の自動更新(2)': 'なし', # keyがイマイチ
            # 利用者等からの苦情に対応する窓口等の状況
            '窓口の名称': 'グループホームほのぼのさくら',
            '電話番号': '011-384-0123',
            '対応している時間__平日': '9時00分～18時00分',
            '対応している時間__土曜': '9時00分～18時00分',
            '対応している時間__日曜': '9時00分～18時00分',
            '対応している時間__祝日': '9時00分～18時00分',
            '定休日': 'なし',
            '留意事項': '',
            # 介護サービスの提供により賠償すべき事故が発生したときの対応の仕組み
            '損害賠償保険の加入状況': 'あり',
            # 介護サービスの提供内容に関する特色等
            '（その内容）(4)': '利用者さんが介護職員と共に家族として介護を心がけている', # keyがイマイチ
            # 利用者等の意見を把握する体制、第三者による評価の実施状況等
            '利用者アンケート調査、意見箱等利用者の意見等を把握する取組の状況（記入日前１年間の状況）': 'なし',
            '当該結果の開示状況': 'あり',
            '地域密着型サービスの外部評価の実施状況': 'あり',
            '実施した直近の年月日（評価結果確定日）': '2020/08/14',
            '実施した評価機関の名称': '特定非営利活動法人福祉サービス評価機構Kネット',
            '当該結果の開示状況(2)': 'あり https://www.wam.go.jp/wamappl/hyoka/003hyoka/hyokekka.nsf/aOpen?OpenAgent&JNO=0171000268&SVC=0001096&BJN=00&OC=01', # keyがイマイチ
            'PDFファイル': ''
        })

    # ５．介護サービス（予防を含む）を利用するに当たっての利用料等に関する事項
    def test_parse_kihon_table05(self):
        f = open('testdata/kihon_table05.html', 'r')
        page_text = f.read()
        f.close()
        soup = BeautifulSoup(page_text, 'html.parser')
        table = soup.select_one('table')
        data = KihonPage.parse_table(table)

        self.maxDiff = None # テスト結果のデバッグ出力強化
        self.assertEqual(data, {
            # 利用料等（入居者の負担額）
            '家賃（月額）': '85,000円',
            '敷金': 'なし',
            '敷金__（その費用の額）': '円',
            '保証金の有無（前払金）': 'なし',
            '保証金の有無（前払金）__（その費用の額）': '円',
            '（保全措置の内容）': '',
            '（償却の有無）': 'なし',
            '食材料費': 'あり',
            '食材料費__（朝食）': '300円',
            '食材料費__（昼食）': '400円',
            '食材料費__（夕食）': '500円',
            '食材料費__（おやつ）': '0円',
            '食材料費__（又は1日）': '0円',
            # その他の費用
            '①理美容代': 'なし',
            '①理美容代__（その費用の額）': '円',
            '算定方法': '',
            '②おむつ代': 'なし',
            '②おむつ代__（その費用の額）': '円',
            '算定方法(2)': '',
            '③その他__（__）': '',
            '③その他__（__）(2)': 'なし',
            '③その他__（__）__（その費用の額）': '円',
            '算定方法(3)': '',
            '④その他__（__）': '',
            '④その他__（__）(2)': 'なし',
            '④その他__（__）__（その費用の額）': '円',
            '算定方法(4)': '',
            '⑤その他__（__）': '',
            '⑤その他__（__）(2)': 'なし',
            '⑤その他__（__）__（その費用の額）': '円',
            '算定方法(5)': ''
        })
