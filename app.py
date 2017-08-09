# /usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for
from flask import flash, jsonify
from werkzeug.utils import secure_filename
from functools import wraps

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Category, ListItem, User

from flask import session as login_session
import random
import string

#import httplib2
#import json
from flask import make_response
#import requests

app = Flask(__name__)

account_sid = "XXXX"
auth_token = "XXXX"
client = Client(account_sid, auth_token)

@app.route("/", methods=['GET'])
def welcome():
    return "Welcome to the homepage"

#sends text message to "to" with body "body"
@app.route("/broadcast", methods=['GET','POST'])
def broadcast():
    message = client.api.account.messages.create(to="XXXX",
                                                 from_="XXXX",
                                                 body="test")
    return str(message)

#add callers section to respond to personalize response to incoming text
callers = {
    "num1" : "name_1",
    "num2" : "name_2",
    "num3" : "name_3"
}

@app.route("/sms_answer", methods=['GET','POST'])
def sms_respond():
    """Respond to texter by name"""

    from_number = request.values.get('From', None)
    if from_number in callers:
        message = callers[from_number] + ", thanks for the message!"
    else:
        message = "Hey friend, thanks for the message!"

    resp = MessagingResponse()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)