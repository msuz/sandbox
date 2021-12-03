# 免責事項

利用は全て自己責任で行って下さい。
本プログラム、データ、コンテンツ等を利用した結果で生じたいかなる損害に対しても作者は責任は負いません。
一切の動作保証及び瑕疵担保義務も負いません。いかなる技術役務の提供義務は負いません。
本プログラムの一部または全部の公開を停止・中断したことにより生じたいかなる損害に対しても責任は負いません。

# usage

install packages
```
$ pip install requests bs4
```

get target urls from latest info page
```
$ python get_list.py > url_list.txt
```

or write target urls into the text file

absolute url
```
$ vi url_list.txt
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0113513220-00&ServiceCd=110
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0115012551-00&ServiceCd=110
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0151580024-00&ServiceCd=110
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0170100945-00&ServiceCd=110
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0170102362-00&ServiceCd=110
```

rerative url
```
$ vi url_list.txt
/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0113513220-00&ServiceCd=110
/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0115012551-00&ServiceCd=110
/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0151580024-00&ServiceCd=110
/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0170100945-00&ServiceCd=110
/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0170102362-00&ServiceCd=110
```

customize config in the script file
```
$ vi run.py
MAX_COUNT = 3
LOGGER_LEVEL = logging.INFO
```

execute command
```
$ cat url_list.txt | python run.py > result.csv 2> log.txt
```

see result file
```
$ less result.csv
```
