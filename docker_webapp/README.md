$ docker build -t flask . 

$ docker run -p 5000:5000 -it flask
 * Serving Flask app "app"
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

```
$ curl http://127.0.0.1:5000
{
  "message": "hello"
}
```

ctrl+c, ctrl+d
