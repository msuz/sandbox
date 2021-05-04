$ docker build -t flask . 

$ docker run -p 5000:5000 -it flask
root@6d7292744354:/projects# flask run --host 0.0.0.0 --port 5000
 * Serving Flask app "app.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

```
$ curl http://127.0.0.1:5000
{"message":"hello"}
```

root@6d7292744354:/projects# exit

$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED         STATUS                        PORTS     NAMES
6d7292744354   flask     "bash"    2 minutes ago   Exited (130) 20 seconds ago             friendly_tu

$ docker start 6d7292744354 -i
root@6d7292744354:/projects# flask run --host 0.0.0.0 --port 5000


