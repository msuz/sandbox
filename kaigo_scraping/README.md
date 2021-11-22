# usage

install packages
```
$ pip install requests bs4
```

write urls to scrape to the text file
```
$ vi url_list.txt

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
