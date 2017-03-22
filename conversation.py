import os
from dotenv import *
from watson_developer_cloud import ConversationV1, WatsonException
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

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
    ws = cache.get(workspace_id)
    if ws is None:
        ws = update_workspace(workspace_id)
    else:
        min_ws = conversation.get_workspace(workspace_id)
        if min_ws['updated'] != ws['updated']:
            ws = update_workspace(workspace_id)
    return ws


def update_workspace(workspace_id):
    try:
        ws = conversation.get_workspace(workspace_id, True)
        cache.set(workspace_id, ws, timeout=5 * 60)
        return ws
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
