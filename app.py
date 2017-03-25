import os
import conversation
from flask import Flask, render_template, url_for
from flask_sslify import SSLify
from workspace_view import WorkspaceView


app = Flask(__name__)
sslify = SSLify(app)


@app.route('/')
def index():
    return render_template('home.html', workspaces=conversation.workspaces())


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
    app.run()
