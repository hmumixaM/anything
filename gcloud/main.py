# [START gae_python37_app]
from flask import *
from database import *
from google.cloud import storage

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__, template_folder="templates")
result, gif_num = find_gif(1)
result, javmost_num = find_javmost(1)
javmost_num = javmost_num // 12


@app.route('/')
def hello():
    return "<a href='gif/1'>gif page</a><br><a href='file'>NetDisk</a><br><a href='javmost/'>Javmost</a>"


@app.route('/file')
def file():
    return render_template('file.html')


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return 'No file uploaded.', 400
    gcs = storage.Client.from_service_account_json("key.json")
    bucket = gcs.get_bucket("ss.12450.xyz")
    blob = bucket.blob(uploaded_file.filename)
    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )
    return blob.public_url
    # return render_template('upload.html', filename=uploaded_file.filename, url=blob.public_url)


@app.errorhandler(404)
def error():
    return redirect(url_for('hello'))


@app.route('/gif')
def other_gif():
    return redirect(url_for('gif', page=1))


@app.route('/javmost')
def other_javmost():
    return redirect(url_for('javmost', page=1))


@app.route('/gif/')
def other_gif_again():
    return redirect(url_for('gif', page=1))


@app.route('/javmost/')
def other_javmost_again():
    return redirect(url_for('javmost', page=1))


@app.route('/gif/<page>')
def gif(page):
    if not page.isdigit():
        return redirect(url_for('gif', page=1))
    page = int(page)
    if page <= 0 or page > gif_num:
        return redirect(url_for('gif', page=1))
    result, max = find_gif(page - 1)
    title = result['title']
    gifs = result['link']
    if page <= 4:
        pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    elif page > gif_num - 7:
        pages = range(gif_num, gif_num + 1)
    else:
        pages = range(page - 3, page + 7)
    return render_template('gif.html', page=page, pages=pages, title=title, gifs=gifs)


@app.route('/javmost/<page>')
def javmost(page):
    if not page.isdigit():
        return redirect(url_for('javmost', page=1))
    page = int(page)
    if page <= 0 or page > javmost_num:
        return redirect(url_for('javmost', page=1))
    videos, max = find_javmost(page)
    if page <= 4:
        pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    elif page > javmost_num - 8:
        pages = range(javmost_num - 10, javmost_num)
    else:
        pages = range(page - 3, page + 7)
    return render_template('jav.html', page=page, pages=pages, videos=videos)


@app.route('/code/<code>/<order>')
def code(code, order):
    videos = find_video(code)
    if videos == 'error':
        return "No video here."
    return render_template('watch.html', code=code, link=videos['videos'], order=int(order),
                           length=len(videos['videos']))


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
