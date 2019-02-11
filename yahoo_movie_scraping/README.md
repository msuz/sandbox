# yahoo_movie_scraping_py

## 使い方

```
$ python main.py | tee result.csv
```

## 注意点

1000リクエスト強でページが取得出来なくなった。
IP単位でabuse判定して別URLにリダイレクトされている模様。
低速化, IP分散, IP偽装などの対応が必要。
