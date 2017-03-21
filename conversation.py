import os
from dotenv import *
from watson_developer_cloud import ConversationV1, WatsonException

load_dotenv(find_dotenv())

CONVERSATION_USERNAME = os.environ.get("CONVERSATION_USERNAME")
CONVERSATION_PASSWORD = os.environ.get("CONVERSATION_PASSWORD")

conversation = ConversationV1(
    username=CONVERSATION_USERNAME,
    password=CONVERSATION_PASSWORD,
    version='2017-02-03'
)


def workspaces():
    return conversation.list_workspaces()['workspaces']


def workspace_info(workspace_id):
    try:
        return conversation.get_workspace(workspace_id, True)
    except WatsonException as err:
        msg = err
        if 'unknown' in err.message.lower():
            msg = 'Rate limit reached for get_workspace call. Please try again in a few minutes.'
        print msg
        return {'err': msg}


def message(workspace_id, input_message):
    return conversation.message(
        workspace_id=workspace_id,
        message_input={'text': input_message}
    )
