# coding: UTF-8

# Usage: $ python main.py | tee result.csv

# ライブラリの読み込み
import requests
#import urllib2 # 依存関係解決できず利用不可
from bs4 import BeautifulSoup

# URLを読み込んでBeautifulSoupオブジェクトを返す
def get_soup_by_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# 一覧ページを読み込んでシネマIDのリストを取得
def get_cinema_ids(page):
    url = 'https://movies.yahoo.co.jp/movie/?page={}'.format(page)
    soup = get_soup_by_url(url)
    ul = soup.find('ul', id='list-module')
    lis = ul.find_all('li', class_="col")
    ids = list(map(lambda x: x['data-cinema-id'], lis))
    return ids

# 詳細ページを読み込んでシネマ情報を取得
def get_movie_data(id):
    url = 'https://movies.yahoo.co.jp/movie/{}/'.format(id)
    soup = get_soup_by_url(url)
    mv = soup.find('div', id='mv')
    title = mv.find('h1').find('span').text
    year = mv.find('h1').find('small').text
    return [id, title, year]


# メイン処理
def main():

    # 指定された範囲のページ番号に対して逐次処理
    for i in range(1, 4000 + 1): # TODO: コマンド引数化

        # 一覧ページを読み込んでシネマIDのリストを取得
        ids = get_cinema_ids(i)

        # シネマIDが存在しない場合、処理を終了する
        if not ids:
            break

        # シネマIDに対して逐次処理
        for id in ids:
            # 詳細ページを読み込んでシネマ情報を取得
            info = get_movie_data(id)
            # シネマ情報を出力
            print(id, *info, sep=',') # TODO: csvライブラリ利用

# 実行
main()
