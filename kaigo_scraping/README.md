# usage

install packages
```
$ pip install requests bs4
```

write target urls into the text file
```
$ vi url_list.txt
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0113513220-00&ServiceCd=110
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0115012551-00&ServiceCd=110
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0151580024-00&ServiceCd=110
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0170100945-00&ServiceCd=110
https://www.kaigokensaku.mhlw.go.jp/01/index.php?action_kouhyou_detail_001_kani=true&JigyosyoCd=0170102362-00&ServiceCd=110
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
