import os
import conversation
from flask import Flask, request, session, flash, redirect, render_template, url_for
from flask_sslify import SSLify
from workspace_view import WorkspaceView


app = Flask(__name__)
sslify = SSLify(app)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', workspaces=conversation.workspaces())


@app.route('/login', methods=['POST'])
def do_admin_login():
    if valid_creds():
        session['logged_in'] = True
    else:
        flash('wrong password!', 'danger')
    return redirect(url_for('home'))


def valid_creds():
    if 'USERNAME' in os.environ and 'PASSWORD' in os.environ:
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
    else:
        username = conversation.USERNAME
        password = conversation.PASSWORD
    return request.form['username'] == username and request.form['password'] == password


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


app.add_url_rule('/workspace/<workspace_id>', view_func=WorkspaceView.as_view('workspace'))


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    app.run(debug=('DEBUG' in os.environ and bool(os.environ['DEBUG'])))
