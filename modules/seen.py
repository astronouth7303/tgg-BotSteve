#!/usr/bin/env python
"""
seen.py - Phenny Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import time, fnmatch
from decimal import *

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
        phenny.reply("No user provided!")
        return 
      
    #misc easter eggs
    if nick == "kyle":
        return phenny.reply("He's about this tall?  Seen Kyle?")
    if nick == phenny.nick.lower():
        return phenny.reply("I'm right here, actually.")
    
    nicks = []
    if nick in storage:
        channel, storedTime = storage[nick]
        nicks.append((nick, channel, storedTime))
    else:
        for n in fnmatch.filter(storage.keys(), nick):
            channel, storedTime = storage[n]
            nicks.append((n, channel, storedTime))
    
    nicks.sort(key=lambda i: -i[2])
    
    if not nicks:
        phenny.reply("Sorry, I haven't seen %s around." % nick)
    else:
        fmt = "I last saw %(nick)s %(formattedTimeDiff)s hours ago at %(t)s on %(channel)s.  Current time: %(currentTime)s"
        currentTime = time.strftime('%H:%M:%S UTC', time.gmtime())
        for nick, channel, storedTime in nicks[:5]:
            t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(storedTime))
            rawTimeDifference_hours = (time.time() - storedTime) / 3600
            formattedTimeDiff = Decimal(str(rawTimeDifference_hours)).quantize(Decimal('1.00'))
            
            #requires python 2.7
            #timeDifference_hr = timeDifference_sec.total_seconds() / 3600
              
            msg = fmt % locals()
            phenny.reply(msg)
            if len(nicks) > 1:
                fmt = "I last saw %(nick)s %(formattedTimeDiff)s hours ago at %(t)s on %(channel)s."
        
        if len(nicks) == 6:
            phenny.reply("(1 more nick found)")
        elif len(nicks) > 5:
            phenny.reply("(%i more nicks found)" % (len(nicks) - 5))
f_seen.rule = (['seen', 'lastseen'], r'(\S+)')

def f_note(phenny, input): 
    global storage
    try:
        if input.sender.startswith('#'): 
            storage[input.nick.lower()] = (input.sender, time.time())
    except:
        import traceback
        traceback.print_exc()
f_note.rule = r'(.*)'
f_note.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()
