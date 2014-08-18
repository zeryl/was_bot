import praw
import re
import yaml

settings = yaml.load(open("settings.yaml"))

r = praw.Reddit(user_agent='amateurradio checker - /u/zeryl')
r.login(settings['reddit-user'], settings['reddit-pass'])

print ("Checking Messages....")

regex_signup = re.compile("(REDDIT WAS)", re.IGNORECASE)

for message in r.get_unread(limit=None):
    if (not message.was_comment):
        if (regex_signup.search(message.subject)):
            message.body = message.body.encode("ascii", "xmlcharrefreplace").decode("ascii", "xmlcharredreplace")
            print ("Message from %s: Subject: %s: Body: %s" % (message.author.name, message.subject, message.body))
            qslmethod = ""
            bands = ""
            callsign = ""
            print ("%s | %s | /u/%s | %s | %s" % ("MO", callsign, message.author.name, qslmethod, bands))
        else:
            print ("No signup command found %s" % (message.subject))
    else:
        print ("IGNORE MESSAGE (comment reply)")
