#!/usr/bin/env python

import datetime
import json
import sys

import requests
import pytz
from twilio.rest import TwilioRestClient

import conf


def send(s):
    client.sms.messages.create(to=conf.TO, from_=conf.FROM, body=s)

# Use the first arg as the message to send, or use the default if not specified
default_message = "You haven't committed anything today!"
message = sys.argv[1] if len(sys.argv) > 1 else default_message

# Initialise twilio stuff
client = TwilioRestClient(conf.ACCOUNT_SID, conf.AUTH_TOKEN)

# Get Github contributions activity
url = 'https://github.com/users/%s/contributions_calendar_data' % conf.USERNAME
request = requests.get(url)
if request.ok:
    data = json.loads(request.text)

    # Set to epoch begin just in case this is a totally new account
    latest_contribution = datetime.datetime(1970, 1, 1, 0, 0)

    # Get data for the latest contribution
    for i in reversed(data):
        if i[1] > 0:
            latest_contribution = datetime.datetime.strptime(i[0], '%Y/%m/%d')
            break

    # Find out today's date in PST (since Github uses PST)
    today = datetime.datetime.now(pytz.timezone('US/Pacific'))

    # Haven't contributed anything today?
    if latest_contribution.date() < today.date():  
      send(message)
else:
    send('There was a problem accessing the Github API :(')
