# Watson Conversation Manager

Python Flask web application for managing Watson Conversation workspaces

### Installation

* Install package requirements with `pip install -r requirements.txt`
* Set environment variables `CONVERSATION_USERNAME` and `CONVERSATION_PASSWORD`
  * this can be set in a file named `.env` if desired (see [python-dotenv](https://github.com/theskumar/python-dotenv) for more details)
* Run application with `python app.py`

### Usage

Log in with your Conversation service credentials, e.g. `CONVERSATION_USERNAME` and `CONVERSATION_PASSWORD`

If you wish to use a different set of credentials to log into the app, set the environment variables `USERNAME` and `PASSWORD` to whatever you want.