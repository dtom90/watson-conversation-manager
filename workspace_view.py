from flask import render_template
from flask.views import View
import conversation


class WorkspaceView(View):
    def dispatch_request(self, workspace_id):
        workspace = conversation.workspace_info(workspace_id)
        max_examples = 0
        for intent in workspace['intents']:
            max_examples = max(max_examples, len(intent['examples']))
        print(max_examples)
        return render_template('workspace.html', workspace=workspace, max_examples=max_examples)
