from flask import *
from db import db


app = Flask(__name__)

@app.route('/')
def hello():
    return "Don't worry. Nothing here. <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><b><br><br><br><br><br><b><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><a href='http://wx4.hellosinaimg.cn/a.html'>okay, I lied.</a>"


@app.route('/mw600/<name>')
def pic(name):
    image = db()
    return redirect(image)

@app.route('/large/<name>')
def largePic(name):
    image = db()
    return redirect(image)
    # mimetype = {
    #     '.jpeg': 'image/jpeg',
    #     '.jpg': 'image/jpeg',
    #     '.png': 'image/png',
    #     '.gif': 'image/gif'
    # }
    # return Response(image, mimetype=mimetype[type])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
