https://docs.djangoproject.com/ja/4.0/intro/tutorial01/

Start server

```
$ python manage.py runserver
```

Run test

```
$ python manage.py test polls
Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 0.025s

OK
Destroying test database for alias 'default'...
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
