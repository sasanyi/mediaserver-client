from flask import Flask, flash, redirect, render_template, \
    request, url_for, Response
from ftplib import FTP

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return render_template("musics.html")


@app.route('/download', methods=['POST'])
def download():
    print(request.form['path'])
    host = 'mmnhu.ddns.net'
    user = 'r2sanyiclient'
    passwd = ''
    ftp = FTP()
    ftp.connect(host, 25)
    ftp.login(user, passwd)
    print(ftp.pwd())
    ftp.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=80)
