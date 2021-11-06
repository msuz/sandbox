# coding: UTF-8

# Script: send_dm.py
#   Ver1.0.0 2021/10/08 @msuz Initial release
#   Ver1.1.0 2021/10/08 @msuz Trello-14
#   Ver1.1.1 2021/10/14 @msuz Trello-31,33,38,48

# Usage:
#   TwitterConfigクラスとFinderConfigクラス内の定数を適宜書き換える
#   予め必要なライブラリ群はインストールしておく
#     $ pip3 install macos-tags requests requests_oauthlib natsort
#   ターミナル以下のコマンドを実行する
#     $ python send_dm.py
#   各女性会員に対して1件ずつDMが送られて、送信済みのファイルにタグ(青)が付く
#   このコマンドを5回実行すれば最大で5件ずつDMが届く
#     $ python -u send_dm.py --MAX_DM_COUNT=30 --FILE_EXPIRE_SECOND=$(expr 12 \* 60 \* 60)
#   -uを付けるとPythonの標準出力のバッファリングが無効になり、リアルタイムにログが出力される
#   --MAX_DM_COUNTでDM送信数の上限を指定できる
#   --FILE_EXPIRE_SECONDで送信対象ファイルの有効期限を指定できる。単位は秒。
#     ※もちろん数値をベタ書きしても良いが、上記のようにexprコマンドを使うと可読性が上がるのでオススメ

# Directory and Files:
#   workdir/
#     + send_dm.py
#     + woman001name_2000-01-01_@woman001twitter/
#       + @woman001twitter-@man001twitter-有料会員.png
#       + @woman001twitter-@man001twitter-有料会員.txt
#       + @woman001twitter-@man002twitter-有料会員.png
#       + @woman001twitter-@man002twitter-有料会員.txt
#       + @woman001twitter-@man003twitter-有料会員.png
#       + @woman001twitter-@man003twitter-有料会員.txt
#       + @woman001twitter.png
#       + @woman001twitter.txt
#       + @woman001twitter-@woman003twitter-有料会員.txt
#     + woman003name_1999-12-31_@woman001twitter/
#       + @woman002twitter-@man004twitter-有料会員.png
#       + @woman002twitter-@man004twitter-有料会員.txt
#       + @woman002twitter-@man005twitter-有料会員.png
#       + @woman002twitter-@man005twitter-有料会員.txt
#       + @woman002twitter.png
#       + @woman002twitter.txt

# Developer's Environment:
#   macOS Mojave ver 10.14.6
#   Python 3.9.6
#   macos-tags 1.5.1
#   requests 2.25.1
#   requests-oauthlib 1.3.0
#   natsort 7.1.1

#
# ライブラリの読み込み
#
import json
from requests_oauthlib import OAuth1Session
import macos_tags
import glob
import re
import os
import sys
import datetime
import time
from natsort import natsorted

#
# 設定値 (実行前に手動で書き換えるべし)
#

MAX_DM_COUNT = 10 # DM送信数の上限、コマンドライン引数で上書きできる
FILE_EXPIRE_SECOND = 7 * 24 * 60 * 60 # ファイルの有効期限(秒)、コマンドライン引数で上書きできる
CONSUMER_KEY = '__YOUR_CONSUMER_KEY__'
CONSUMER_SECRET = '__CONSUMER_SECRET__'
ACCESS_TOKEN = '__ACCESS_TOKEN__'
ACCESS_TOKEN_SECRET = '__ACCESS_TOKEN_SECRET__'

#
# クラスの定義 (別ファイルに切り出すと色々面倒なのでベタ書きするよ)
#

# コマンドライン引数を読み込むするクラス
class SysArgv:
    # インスタンス作成時にパラメタを解析
    def __init__(self):
        self.vars = {}
        pattern = '^\-\-([^=]+)=(.+)$'
        for arg in sys.argv:
            result = re.match(pattern, arg)
            if not result: continue
            self.vars[result.group(1)] = result.group(2)
        return

    # キーを指定して取得
    def get(self, k, v = None):
        if k in self.vars: return self.vars[k]
        return v

# TwitterAPIとやりとりするクラス
class Twitter:
    def __init__(self, ck="", cs="", at="", ats=""):
        self.CONSUMER_KEY = ck
        self.CONSUMER_SECRET = cs
        self.ACCESS_TOKEN = at
        self.ACCESS_TOKEN_SECRET = ats
        self.session = OAuth1Session(self.CONSUMER_KEY, self.CONSUMER_SECRET,
            self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        return

    # 表示名からIDを取得する
    def twitter_id_to_recipient_id(self, twitter_id):
        url = 'https://api.twitter.com/1.1/users/show.json'
        params = {'screen_name': twitter_id}
        response = self.session.get(url, params = params)
        if response.status_code != 200: return ""
        return json.loads(response.text)['id_str']

    # テキストデータを読み込み
    def message_file_to_text_data(self, message_file):
        f = open(message_file, 'r', encoding='UTF-8')
        data = f.read()
        f.close()
        return data

    # ファイルをアップロードする
    def upload_image_file(self, image_file):
        url = 'https://upload.twitter.com/1.1/media/upload.json'
        params = {
            'media': open(image_file, 'rb'),
            'media_category': 'dm_image',
            'media_data': ''
        }
        response = self.session.post(url, files = params)
        if response.status_code != 200: return ""
        return json.loads(response.text)['media_id_string']

    def send_direct_message(self, recipient_id, text_data, media_id):
        url = 'https://api.twitter.com/1.1/direct_messages/events/new.json'
        headers = {'content-type': 'application/json'}
        params = {
            'event': {
                'type': 'message_create',
                'message_create': {
                    'target': {'recipient_id': recipient_id},
                    'message_data': {
                        'text': text_data,
                        'attachment': {
                            'type': 'media',
                            'media': {
                                'id': media_id
                            }
                        }
                    }
                }
            }
        }
        response = self.session.post(url, headers = headers, data = json.dumps(params))
        if response.status_code != 200: return ""
        return json.loads(response.text)['event']['id']

# Finderとやりとりするクラス
class Finder:
    def __init__(self, sec=24*60*60):
        self.FILE_EXPIRE_SECOND = sec # グローバル変数
        self.BASE_PATH = "." # 走査対象となるディレクトリ
        self.MESSAGE_FILENAME_PATTERN = "@*-@*-*.txt" # 送信対象メッセージファイルの正規表現パターン
        self.IMAGE_FILE_EXT = ".png" # 送信対象画像ファイルの拡張し
        self.SEND_TAG = macos_tags.Tag(name='ブルー', color=macos_tags.Color.BLUE) # DM送信済みのファイルに付けるタグ
        self.EXCLUDE_TAGS = [macos_tags.Tag(name='レッド', color=macos_tags.Color.RED)]

        return

    # 女性会員のディレクトリ一覧を取得する
    def get_woman_list(self):
        files = natsorted(os.listdir(self.BASE_PATH))
        result = [f for f in files if os.path.isdir(os.path.join(self.BASE_PATH, f))]
        # ホントは正規表現でフィルタした方がいいけど略。運用で気をつけてね
        return result

    # 女性会員ディレクトリから送信対象のメッセージファイル名を1つ取得する
    def get_sending_message_file(self, woman_dir):
        # 表記ルールに一致するファイルを全て取得する
        pattern = os.path.join(self.BASE_PATH,
            woman_dir, self.MESSAGE_FILENAME_PATTERN)
        message_files = glob.glob(pattern)

        # ファイルの最終更新日時を比較して一番古いファイルを探す
        min_mtime = 1893423599.00000000 # 2029-12-31 23:59:59 のUnixtime
        min_file = "" # 送信対象のメッセージファイル名。見つからなかったら空のまま

        # 一定時間以上経過したファイルは使わない
        limit_mtime = time.time() - self.C_SECOND

        for m in message_files:
            # 日付が古かったら対象外。次のファイルへ
            if os.stat(m).st_mtime <= limit_mtime: continue
            # 日付が新しかったら対象外。次のファイルへ
            if os.stat(m).st_mtime >= min_mtime: continue
            # メッセージファイルの対となる画像ファイルが存在しなかったら対象外。次のファイルへ
            if not os.path.isfile(self.message_file_to_image_file(m)): continue
            # 除外対象のFinderタグが付いてたら対象外。次のファイルへ
            if self.has_exclude_tag(m): continue
            # 条件をクリアしたら対象ファイルと見なす。一時保存用変数に上書き
            min_mtime = os.stat(m).st_mtime
            min_file = m

        return min_file

    # 送信済みタグまたは除外対象タグが付いているかどうかを調べる
    def has_exclude_tag(self, message_file):
        tags = macos_tags.get_all(message_file)
        if self.SEND_TAG in tags: return True
        for exclude_tag in self.EXCLUDE_TAGS:
            if exclude_tag in tags: return True
        return False

    # ファイルにタグを付ける (成功:True/失敗:False)
    def set_send_tag(self, file):
        tag = self.SEND_TAG

        # メッセージファイル
        tags_before = macos_tags.get_all(file)
        macos_tags.add(tag, file=file)
        tags_after  = macos_tags.get_all(file)
        if not (len(tags_after) > len(tags_before)):
            # Trello-31: 稀にFinderタグの付与に失敗するため、デバッグ出力を強化
            # ホントはClass内ではprint()したくないんだけどLoggerめんどいからその場しのぎ
            print('    %s: before %s -> after %s' % (
                os.path.basename(file),
                [tags.name for tags in tags_before],
                [tags.name for tags in tags_after]
            ))
            return False

        return True

    # メッセージファイルと画像ファイルからすべてのタグを削除する
    def remove_all_tags(self, message_file):
        image_file = self.message_file_to_image_file(message_file)
        macos_tags.remove_all(message_file)
        macos_tags.remove_all(image_file)

    # メッセージファイル名からTwitter idを取得する
    def message_file_to_twitter_id(self, message_file):
        return os.path.basename(message_file).split('-')[0]

    # メッセージファイル名から画像ファイル名を取得する
    def message_file_to_image_file(self, message_file):
        return os.path.splitext(message_file)[0] + self.IMAGE_FILE_EXT

#
# メイン処理
#
def main():
    args = SysArgv()
    max_dm_count = int(args.get('MAX_DM_COUNT', MAX_DM_COUNT))
    file_expire_second = int(args.get('FILE_EXPIRE_SECOND', FILE_EXPIRE_SECOND))

    t = Twitter(ck=CONSUMER_KEY, cs=CONSUMER_SECRET, at=ACCESS_TOKEN, ats=ACCESS_TOKEN_SECRET)
    f = Finder(sec=file_expire_second)
    i = 0 # DM送信数

    # 女性会員のリストに対して逐次処理
    for woman_dir in f.get_woman_list():
        print("------------------------------------------------------------")
        # DM送信数が上限に達していたら処理を打ち切る
        if i >= max_dm_count:
            print("Warning! Max DM count [%d]" % max_dm_count)
            break

        print("Start process for woman directory [%s]" % woman_dir)

        # 送信対象のテキストファイル名を取得する
        print("  Searching target files.")
        message_file = f.get_sending_message_file(woman_dir)
        if not message_file:
            print("  Error!! No file.")
            continue
        print("    text file: [%s]" % message_file)

        # テキストファイルから画像ファイルとTwitterIDを取得する
        image_file = f.message_file_to_image_file(message_file)
        twitter_id = f.message_file_to_twitter_id(message_file)
        print("    image file: [%s]" % image_file)
        print("    twitter_id: [%s]" % twitter_id)

        print("  Getting Text data from file.")
        text_data = t.message_file_to_text_data(message_file)
        print("    text data: [%s ..]" % text_data[:30].replace('\n',''))

        print("  Getting Twitter recipient id from api.")
        recipient_id = t.twitter_id_to_recipient_id(twitter_id)
        if not recipient_id:
            print("  Error!! Twitter id is disabled.")
            continue
        print("    recipient_id: [%s]" % recipient_id)

        print("  Uploading image file via api.")
        media_id = t.upload_image_file(image_file)
        if not media_id:
            print("  Error!! File upload error.")
            continue
        print("    media_id: [%s]" % media_id)

        print("  Sending Twitter direct message.")
        event_id = t.send_direct_message(recipient_id, text_data, media_id)
        if not event_id:
            print("  Error!! Can't send DM.")
            continue
        print("    event id: [%s]" % event_id)

        # DMの送信数を加算して出力
        i += 1
        print("=== [%s], DM count: [%05d], file: [%s] ===" % (datetime.datetime.now(), i, message_file))

        # 送信済みのメッセージファイルと画像ファイルにタグを付ける
        print("  Adding Finder tags to files.")
        if not f.set_send_tag(message_file): print("    Error!! Can't add tag to message file.")
        if not f.set_send_tag(image_file  ): print("    Error!! Can't add tag to image file.")
        print("  Done.")


if __name__ == "__main__":
    main()
