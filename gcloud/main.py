# [START gae_python37_app]
from flask import *
from database import find

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__, template_folder="templates")


@app.route('/')
def hello():
    return "<a href='gif/1'>gif page</a>"


@app.errorhandler(404)
def error():
    return redirect(url_for('hello'))


@app.route('/gif')
def other():
    return redirect(url_for('gif', page=1))


@app.route('/gif/<page>')
def gif(page):
    if not page.isdigit():
        return redirect(url_for('gif', page=1))
    page = int(page)
    if page <= 0 or page > 1188:
        return redirect(url_for('gif', page=1))
    result = find(page-1)
    title = result['title']
    gifs = result['gif']
    if page <= 4:
        pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    elif page > 1181:
        pages = range(1179, 1189)
    else:
        pages = range(page-3, page+7)
    return render_template('gif.html', page=page, pages=pages, title=title, gifs=gifs)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
