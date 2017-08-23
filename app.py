# /usr/bin/env python
import os
from flask import Flask, render_template, request, redirect, url_for
from flask import flash, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from werkzeug.utils import secure_filename
from functools import wraps

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database_setup import Base, User

import random
import string

from flask import make_response

engine = create_engine('sqlite:///user_info.db')
Base.metadata.bind = engine

db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()

admin = Admin(app)
admin.add_view(ModelView(User, db_session))


client = Client(account_sid, auth_token)

app = Flask(__name__)

# helper function to strip user input phone number to just numbers
def db_phone(user_input):
    new_number = ""
    numbers = [str(i) for i in range(0,10)]
    for ch in user_input:
        if ch in numbers:
            new_number += ch
        else:
            pass
    return new_number

#landing page for user registration and next-day rsvp
@app.route("/", methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        if request.form['submit'] == "Sign Me Up!":
            phone = db_phone(request.form['phone'])
            newUser = User(name=request.form['name'], phone=phone, email=request.form['email'])
            if request.form.get('tomorrow'):
                newUser.tomorrow = 1
                newUser.attendance = 1
            db_session.add(newUser)
            db_session.commit()
            return redirect(url_for('registration'))
        elif request.form['submit'] == "I'll be there!":
            phone = db_phone(request.form['rsvp_phone'])
            current_user = db_session.query(User).filter_by(phone=phone).one()
            current_user.tomorrow = 1
            current_user.attendance = current_user.attendance + 1
            db_session.add(current_user)
            db_session.commit()
            return redirect(url_for('registration'))
        return redirect(url_for('registration'))
    else:
        count = db_session.query(User).filter_by(tomorrow=1).count()
        return render_template('homepage.html', registration=count)

#admin page to reset counter for next day
@app.route("/admin", methods=['GET','POST'])
def reset_tomorrow():
    if request.method == 'POST':
        users = db_session.query(User).all()
        for user in users:
            user.tomorrow = 0
            db_session.add(user)
            db_session.commit()
        return redirect(url_for('registration'))

#unsubscribe page for users no longer participating
@app.route("/unsubscribe", methods=['GET','POST'])
def unsubscribe():
    if request.method == 'POST':
        phone = db_phone(request.form['phone'])
        user = db_session.query(User).filter_by(phone=phone).one()
        db_session.delete(user)
        db_session.commit()
        return redirect(url_for('registration'))
    else:
        return render_template('unsubscribe.html')

#sends text message to "to" with body "body" via Twilio API
@app.route("/broadcast", methods=['GET','POST'])
def broadcast():
    user_numbers = db_session.query(User.phone).all()
    count = db_session.query(User).filter_by(tomorrow=1).count()
    body = "We currently have " + count + "confirmed for tomorrow"
    for number in user_numbers:
        message = client.api.account.messages.create(to=number,
                                                     from_="XXXX",
                                                     body=body)
    return str(message)

@app.route("/sms_rsvp", methods=['POST'])
def sms_rsvp():
    """Respond to texter by name"""
    from_number = db_phone(request.values.get('From', None))
    registered_user = db_session.query(User).filter_by(phone=from_number).one()

    if registered_user:
        registered_user.tomorrow = 1
        message = "We can't wait to see you!"
    else:
        message = "Doesn't look like you're registered for our site," +
                    " once you register you can use text rsvp."

    resp = MessagingResponse()
    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)