from flask import render_template, request
from flask.views import View
from wtforms import Form, StringField
import conversation


class WorkspaceView(View):
    def dispatch_request(self, workspace_id):
        workspace = conversation.workspace_info(workspace_id)

        if 'err' in workspace:
            return workspace['err']

        repeat_examples = []
        all_examples = {}
        max_examples = 0
        max_repeats = 0
        for intent in workspace['intents']:
            name = intent['intent']
            examples = intent['examples']
            max_examples = max(max_examples, len(examples))
            for example in examples:
                text = example['text'].lower()
                if text in all_examples:
                    all_examples[text].append(name)
                    count = len(all_examples[text])
                    if count == 2: repeat_examples.append(text)
                    max_repeats = max(max_repeats, count)
                else:
                    all_examples[text] = [name]

        repeats = {ex: all_examples[ex] for ex in repeat_examples}

        test_form = TestForm()

        message = request.args.get('message')
        message_output = conversation.message(workspace_id, message) if message else None

        return render_template('workspace.html', workspace=workspace, max_examples=max_examples,
                                                 repeats=repeats, max_repeats=max_repeats,
                                                 form=test_form, message=message,
                                                 message_output=message_output, )


class TestForm(Form):
    message = StringField('Message')
