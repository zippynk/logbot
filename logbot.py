#!/usr/bin/python


#      This Source Code Form is subject to the
#            terms of the Mozilla Public License, v.
#                  2.0. If a copy of the MPL was not
#                        distributed with this file, You can
#                              obtain one at
#                                    http://mozilla.org/MPL/2.0/.
#                                       What in the world is going
#                                          on with my license notice?
#                                               Ugh, Vim.
from __future__ import print_function
from pyrcb.pyrcb import IrcBot
from datetime import datetime
import sys
import os

class LogBot(IrcBot):
    def on_message(self, message, nickname, target, is_query):
        if target == self.mainChannel:
            self.log("{0}:{1} <{2}> {3}".format(datetime.now().hour,datetime.now().minute,nickname,message))

    def on_join(self, nickname, channel, is_self):
        if channel == self.mainChannel:
            self.log("{0}:{1} -!- {2} has joined {3}".format(datetime.now().hour,datetime.now().minute,nickname,channel))
   
    def on_notice(self,message,nickname,target,is_query): 
        if target == self.mainChannel:
            self.log("{0}:{1} -{2}:{3}- {4}".format(datetime.now().hour,datetime.now().minute,nickname,target,message))
        
         
    def on_quit(self, nickname, message):
        self.log("{0}:{1} -!- {2} has quit [{3}]".format(datetime.now().hour,datetime.now().minute,nickname,message))

    def on_part(self, nickname, channel, message):
        if channel == self.mainChannel:
            self.log("{0}:{1} -!- {2} has parted {3} [{4}]".format(datetime.now().hour,datetime.now().minute,nickname,channel,message))

    def on_kick(self, nickname, channel, target, is_self):
        if channel == self.mainChannel:
            self.log("{0}:{1} -!- {2} has been kicked from {3} by {4} [{5}]".format(datetime.now().hour,datetime.now().minute,target,nickname,channel,message))

    def on_nick(self,nickname,new_nickname,is_self):
        self.log("{0}:{1} -!- {2} is now known as {3}".format(datetime.now().hour,datetime.now().minute,nickname,new_nickname))
    
    def on_names(self,channel,names):
        self.log("{0}:{1} People in {2}: {3}".format(datetime.now().hour,datetime.now().minute,channel,", ".join(names)))

    def log(self,message):
        if os.path.isfile(self.logFile()):
            temp1 = open(self.logFile(),"a")
        else:
            temp1 = open(self.logFile(),"wb")
        temp1.write(message +"\n")
        temp1.close()

    def logFile(self):
        return self.logFilePrefix + "_" + str(datetime.now().year) + "_" + str(datetime.now().month) + "_" + str(datetime.now().day)
def main():
    bot = LogBot(debug_print=True)
    bot.mainChannel = sys.argv[4]
    bot.logFilePrefix = sys.argv[5]
    bot.connect(sys.argv[1], int(sys.argv[2]))
    bot.register(sys.argv[3])
    if len(sys.argv) > 6:
        bot.password(sys.argv[7])
    bot.join(bot.mainChannel)
    # Blocking; will return when connection is lost.
    bot.listen()
    print("Disconnected from server.")

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python logbot.py <server> <port> <nick> <channel> <log filepath, will be appended with _YYYY_M(M)_D(D)> <password (optional)>")
        exit(1)
    main()
