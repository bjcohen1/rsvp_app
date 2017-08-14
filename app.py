# /usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for
from flask import flash, jsonify
from werkzeug.utils import secure_filename
from functools import wraps

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User

import random
import string

from flask import make_response

app = Flask(__name__)

engine = create_engine('sqlite:///signedup.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession

account_sid = "XXXX"
auth_token = "XXXX"
client = Client(account_sid, auth_token)

# helper function to strip user input phone number to just numbers
def db_number(user_input):
    new_number = ""
    for ch in user_input:
        if ch in range(0,10):
            new_number.append(ch)
        else:
            pass

@app.route("/", methods=['GET','POST'])
def welcome():
    if request.method == 'POST':
        newUser = User(name=name, phone=db_number(phone), email=email)
        session.add(newUser)
        session.commit()
        #return redirect(thank you page)
    else:
        return render_template('homepage.html')

#sends text message to "to" with body "body"
@app.route("/broadcast", methods=['GET','POST'])
def broadcast():
    user_numbers = session.query(User).all()
    for number in user_numbers:
        message = client.api.account.messages.create(to=number,
                                                     from_="XXXX",
                                                     body="test")
    return str(message)

#add callers section to respond to personalize response to incoming text
#callers = {
#    "num1" : "name_1",
#    "num2" : "name_2",
#    "num3" : "name_3"
#}

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