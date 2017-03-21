from flask import render_template, request
from flask.views import View
from wtforms import Form, StringField
import conversation


class WorkspaceView(View):
    def dispatch_request(self, workspace_id):
        workspace = conversation.workspace_info(workspace_id)

        if 'err' in workspace:
            return workspace['err']

        max_examples = 0
        all_examples = {}
        for intent in workspace['intents']:
            name = intent['intent']
            examples = intent['examples']
            max_examples = max(max_examples, len(examples))
            for example in examples:
                text = example['text'].lower()
                if text in all_examples:
                    all_examples[text].append(name)
                else:
                    all_examples[text] = [name]

        repeats = {}
        max_repeats = 0
        for example in all_examples:
            if len(all_examples[example]) > 1:
                repeats[example] = all_examples[example]
                max_repeats = max(max_repeats, len(repeats[example]))

        test_form = TestForm()

        utterance = request.args.get('utterance')
        test_response = conversation.message(workspace_id, utterance) if utterance else None

        intents = test_response['intents'] if utterance else None

        return render_template('workspace.html', workspace=workspace,
                                                 form=test_form, utterance=utterance,
                                                 intents=intents, max_examples=max_examples,
                                                 repeats=repeats, max_repeats=max_repeats)

class TestForm(Form):
    utterance = StringField('Utterance')
