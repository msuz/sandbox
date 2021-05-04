$ docker build -t flask . 

$ docker run -p 5000:5000 -it flask /bin/sh

/projects # export FLASK_APP=/projects/app.py
/projects # flask run --host 0.0.0.0 --port 5000

```
$ curl http://127.0.0.1:5000
{
  "message": "hello"
}
```

ctrl+c, ctrl+d
