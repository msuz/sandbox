https://docs.djangoproject.com/ja/4.0/intro/tutorial01/

Start server

```
$ python manage.py runserver
```

Open url via web brawser

- http://localhost:8000/polls/
- http://localhost:8000/admin/
- http://localhost:8000/membersite/

Run test

```
$ python manage.py test polls
Found 10 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
WARNING:django.request:Not Found: /polls/1/
..........
----------------------------------------------------------------------
Ran 10 tests in 0.031s

OK
Destroying test database for alias 'default'...


$ python manage.py test polls.tests.QuestionDetailViewTests.test_future_question
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
WARNING:django.request:Not Found: /polls/1/
.
----------------------------------------------------------------------
Ran 1 test in 0.010s

OK
Destroying test database for alias 'default'...


$ python manage.py test polls/ --pattern="tests*.py"
```


Debug in shell as a test environment

```
$ python manage.py shell

from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import Client
client = Client()

res = client.get(reverse('polls:index'))

res.context['question']
```

Run command

```
$ python manage.py vote_summary
[1] What's up?
 - Not Much [2 votes]
 - The Sky [11 votes]
 - Just hacking again [4 votes]
[2] Where are you from?
[3] when do you drink tea?
 - morning [0 votes]
[4] Past question.
[5] My First Question
```
