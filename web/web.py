# import sys, os
# os.environ['SPARK_HOME'] = '/usr/local/Cellar/apache-spark/2.0.2'
# sys.path.insert(1, '/usr/local/Cellar/apache-spark/2.0.2/libexec/python')
# sys.path.insert(2, '/usr/local/Cellar/apache-spark/2.0.2/libexec/python/lib/py4j-0.10.3-src.zip')

from flask import Flask
from flask import request, g, send_from_directory
import json


userDict = {}
with open("cache.jl") as f:
    for line in f:
        d = json.loads(line)
        userDict[d[0]] = json.dumps({
            "status": "succ",
            "uid": d[0],
            "business": d[1],
            "users": d[2],
            "taste": d[3]
        })
f.close()


app = Flask(__name__, static_url_path='')


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route('/result')
def result():
    return app.send_static_file('index.html')

@app.route('/api/recommendation', methods=['GET'])
def api():
    try:
        uid = int(request.args.get('uid'))
        if uid in userDict:
            return userDict[uid]
        else:
            return json.dumps({
                    "status": "fail",
                    "message": "UID %d havn't been calculated."%uid
                })
    except Exception as e:
        return json.dumps({
                "status": "fail",
                "message": e.message
            })

if __name__ == "__main__":
    import click
    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='127.0.0.1')
    @click.argument('PORT', default=8080, type=int)
    def run(debug, threaded, host, port):
        HOST, PORT = host, port
        print "running on %s:%d" % (HOST, PORT)
        threaded = True
        print "Threaded %s" % threaded
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
