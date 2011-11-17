#!/usr/bin/env python
"""
seen.py - Phenny Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import time
from tools import deprecated
from decimal import *
import os

storage = {} # Default value
# storage is a persistant value, automagically loaded and saved by the bot.

#def setup(self): 
#    pass

def f_seen(phenny, input):
    """.seen <nick> - Reports when <nick> was last seen."""
    global storage
     
    try:
        nick = input.group(2).lower()
    except AttributeError:
        self.msg(origin.sender, "No user provided!")
        return 
      
    #misc easter eggs
    if nick == "kyle":
        return self.reply("He's about this tall?  Seen Kyle?")
    if nick == phenny.nick.lower():
        return self.reply("I'm right here, actually.")
    
    if item: 
        channel, storedTime = storage[nick]
        t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(storedTime))
        currentTime = time.strftime('%H:%M:%S UTC', time.gmtime())
        rawTimeDifference_hours = (time.time() - storedTime) / 3600
        formattedTimeDiff = Decimal(str(rawTimeDifference_hours)).quantize(Decimal('1.00'))
        
        #requires python 2.7
        #timeDifference_hr = timeDifference_sec.total_seconds() / 3600
          
        msg = "I last saw %s %s hours ago at %s on %s.  Current time: %s" % (nick, formattedTimeDiff, t, channel, currentTime)
        phenny.reply(msg)
      
    #no record of user
    else: 
        phenny.reply("Sorry, I haven't seen %s around." % nick)
f_seen.rule = (['seen', 'lastseen'], r'(\S+)')

def f_note(phenny, input): 
    global storage
    try:
        if origin.sender.startswith('#'): 
            storage[origin.nick.lower()] = (origin.sender, time.time())
    except:
        import traceback
        traceback.print_exc()
f_note.rule = r'(.*)'
f_note.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()
