from flask import render_template, request
from flask.views import View
from wtforms import Form, StringField
import conversation


class WorkspaceView(View):
    def dispatch_request(self, workspace_id):
        workspace = conversation.workspace_info(workspace_id)

        max_examples = 0
        for intent in workspace['intents']:
            max_examples = max(max_examples, len(intent['examples']))

        test_form = TestForm()

        utterance = request.args.get('utterance')
        test_response = conversation.message(workspace_id, utterance)['intents'] if utterance else None

        return render_template('workspace.html', workspace=workspace, max_examples=max_examples,
                                                 form=test_form, utterance=utterance, intents=test_response)


class TestForm(Form):
    utterance = StringField('Utterance')
