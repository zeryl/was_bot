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
#            print ("Message from %s: Subject: %s: Body: %s" % (message.author.name, message.subject, message.body))
            s = message.body.split('|')
            qslmethod = s[2].strip()
            bands = s[3].strip()
            callsign = s[1].strip().upper()
            state = s[0].strip().upper()
            print ("%s | %s | /u/%s | %s | %s" % (state, callsign, message.author.name, qslmethod, bands))
            message.mark_as_read()
            message.reply("Thank you for your submission, it should be on the site soon!")
        else:
            print ("No signup command found %s" % (message.subject))
    else:
        print ("IGNORE MESSAGE (comment reply)")
