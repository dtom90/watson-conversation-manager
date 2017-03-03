import os
from dotenv import *
from watson_developer_cloud import ConversationV1

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
    return conversation.get_workspace(workspace_id, True)


def message(workspace_id, input_message):
    return conversation.message(
        workspace_id=workspace_id,
        message_input={'text': input_message}
    )
