#!/usr/bin/python
#  Copyright (C) 2014  Sebastian Garcia
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# Author:
# Sebastian Garcia, sebastian.garcia@agents.fel.cvut.cz, sgarcia@exa.unicen.edu.ar, eldraco@gmail.com
#
# Changelog

# Description
# A command line tool to get information about any twitter account.
#
# TODO


# standard imports
import getopt
import sys
try:
    import tweepy
except ImportError:
    print 'You need the tweepy libraries. apt-get install python-tweepy'
import json
#import time
from datetime import datetime
#from datetime import timedelta
####################

# Global Variables
debug = 0
vernum = "0.1"
#########


# Print version information and exit
def version():
    print "+----------------------------------------------------------------------+"
    print "| twitter-stats.py Version "+ vernum +"                                        |"
    print "| This program is free software; you can redistribute it and/or modify |"
    print "| it under the terms of the GNU General Public License as published by |"
    print "| the Free Software Foundation; either version 2 of the License, or    |"
    print "| (at your option) any later version.                                  |"
    print "|                                                                      |"
    print "| Author: Garcia Sebastian, eldraco@gmail.com                          |"
    print "| UNICEN-ISISTAN, Argentina. CTU, Prague-ATG                           |"
    print "+----------------------------------------------------------------------+"
    print


# Print help information and exit:
def usage():
    print "+----------------------------------------------------------------------+"
    print "| twitter-stats.py Version "+ vernum +"                                        |"
    print "| This program is free software; you can redistribute it and/or modify |"
    print "| it under the terms of the GNU General Public License as published by |"
    print "| the Free Software Foundation; either version 2 of the License, or    |"
    print "| (at your option) any later version.                                  |"
    print "|                                                                      |"
    print "| Author: Garcia Sebastian, eldraco@gmail.com                          |"
    print "| UNICEN-ISISTAN, Argentina. CTU, Prague-ATG                           |"
    print "+----------------------------------------------------------------------+"
    print "\nusage: %s <options>" % sys.argv[0]
    print "options:"
    print "  -h, --help                 Show this help message and exit"
    print "  -D, --debug                Debug. Defaults to 0. The higher the number, the more information printed."
    print "  -n, --twitter-name         Twitter name."
    print "  -i, --twitter-id           Twitter numeric id."
    print "  -p, --get-profile          Get twitter profile from name or id."
    print "  -f, --get-followers        Get twitter followers from name or id."
    print "  -a, --auth-file            The name of the txt auth file with the twitter credentials. See https://dev.twitter.com/docs/auth/tokens-devtwittercom "
    print
    sys.exit(1)
   


class TwitterFunctions():
    """
    Basic twitter functions
    """
    def __init__(self):
        self.twitter_name = ""
        self.twitter_id = ""

    def print_json(self,json_text):
        """
        Get a json and print it nice
        """
        try:
            res = json.dumps(json_text, sort_keys=True, indent=4, separators=(',', ': '))
            print res
        except Exception as inst:          
            print 'Problem in print_json() in class TwitterFunctions'
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args    
            print inst           # __str__ allows args to printed directly
            exit(-1)

    def get_followers(self):
        """
        Get the twitter followers using the name or the id if the name is not available.
        """
        global debug
        try:
            if self.twitter_name:
                if debug > 1:
                    print 'Getting the followers for name {}'.format(self.twitter_name)

                # Get the api using the the auth
                self.get_api()          

                # Get the limits once
                self.get_limits()
                total = int(self.limits['resources']["followers"]["/followers/list"]["limit"])
                remaining = int(self.limits['resources']["followers"]["/followers/list"]["remaining"])
                
                if debug > 1:
                    print 'Checking limit for followers lookup...'
                    print 'Total: {}, Remaining: {}'.format(total, remaining)
                if not remaining:
                    print 'Warning, no more followers requests available. Total allowed:{}. Available:{}'.format(total, remaining)
                    print 'Wait 15 minutes and try again.'
                    sys.exit(-1)

                # Get the data and print it
                #date = datetime.now()
                #print date
                for user in tweepy.Cursor(self.api.followers, screen_name=self.twitter_name).items():
                        print user.screen_name

            elif self.twitter_id:
                if debug > 1:
                    print 'Getting the followers for id {}'.format(self.twitter_id)
            else:
                print 'No name or id given.'
                usage()
                sys.exit(-1)

        except Exception as inst:          
            print 'Problem in get_followers() in class TwitterFunctions'
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args    
            print inst           # __str__ allows args to printed directly
            exit(-1)


    def get_profile(self):
        """
        Get the twitter profile using the name or the id if the name is not available.
        """
        global debug
        try:
            if self.twitter_name:
                if debug > 1:
                    print 'Getting the profile for name {}'.format(self.twitter_name)

                # Get the api using the the auth
                self.get_api()          

                # Get the limits once
                self.get_limits()

                total = int(self.limits['resources']["users"]["/users/lookup"]["limit"])
                remaining = int(self.limits['resources']["users"]["/users/lookup"]["remaining"])
                
                if debug > 1:
                    print 'Checking limit for users lookup...'
                    print 'Total: {}, Remaining: {}'.format(total, remaining)
                if not remaining:
                    print 'Warning, no more users lookup requests available. Total allowed:{}. Available:{}'.format(total, remaining)
                    print 'Wait 15 minutes and try again.'
                    sys.exit(-1)

                # Get the data
                self.json_user_data = self.api.lookup_users(screen_names=self.twitter_name)
                #self.print_json(self.json_user_data)
                print self.json_user_data

            elif self.twitter_id:
                if debug > 1:
                    print 'Getting the profile for id {}'.format(self.twitter_id)
            else:
                print 'No name or id given.'
                usage()
                sys.exit(-1)

        except Exception as inst:          
            print 'Problem in get_profile() in class TwitterFunctions'
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args    
            print inst           # __str__ allows args to printed directly
            exit(-1)


    def get_limits(self):
        global debug
        try:
            if debug:
                print 'Trying to get the twitter limits'
            self.limits = self.api.rate_limit_status()
            if debug > 4:
                print 'Limits'
                self.print_json(self.limits)
                print
        except Exception as inst:          
            print 'Problem in get_limits() in class TwitterFunctions'
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args    
            print inst           # __str__ allows args to printed directly
            exit(-1)
            sys.exit(-1)


    def get_api(self):
        """
        Get the api info
        """
        global debug
        self.read_config_file()
        try:
            if debug:
                print 'Getting the twitter OAuthHandler'
            auth = tweepy.OAuthHandler(self.credentials["consumer_key"], self.credentials["consumer_secret"])
            auth.set_access_token(self.credentials["access_token"], self.credentials["access_token_secret"])
        except Exception as inst:          
            print 'Problem in get_api() in class TwitterFunctions'
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args    
            print inst           # __str__ allows args to printed directly
            exit(-1)
        try:
            # Makes use of a patch to tweepy which provides a default timeout value.
            if debug:
                print 'Getting the twitter API'
            api = tweepy.API(auth_handler=auth, timeout=10)
        except:
            # Makes use of standard tweepy.
            if debug > 2:
                print 'Don\'t know what happened' 
            api = tweepy.API(auth_handler=auth)

        if debug> 2:
            print '\tAPI obtained successfully'
        self.api = api


    def read_config_file(self):
        """
        Reads the conf file with the OAuth info
        """
        global debug
        try:
            if debug:
                print 'Using credentials in {}'.format(self.auth_file)
            fp = open(self.auth_file)
        except:
            if debug:
                print 'Need to provide a valid auth file which contains access token, access token secret, consumer key and consumer secret.'
            sys.exit(-1)

        self.credentials = {}
        for line in fp:
            key,value = line.strip().split('=')
            if key=="oauth.accessToken":
                self.credentials["access_token"] = value
            elif key=="oauth.accessTokenSecret":
                self.credentials["access_token_secret"] = value
            elif key=="oauth.consumerKey":
                self.credentials["consumer_key"] = value
            elif key=="oauth.consumerSecret":
                self.credentials["consumer_secret"] = value
        assert len(self.credentials)==4, "Improper auth file."
        if debug > 3:
            print '\tRead credentials: {}'.format(self.credentials)



 
def main():
    try:
        global debug
        opts, args = getopt.getopt(sys.argv[1:], "hvD:n:i:pfa:", ["help","verbose","debug=","twitter-name=","twitter-id=","get-profile","auth-file","get-followers"])
    except getopt.GetoptError: usage()

    tf = TwitterFunctions()

    get_profile = False
    get_followers = False

    for opt, arg in opts:
        if opt in ("-h", "--help"): usage()
        if opt in ("-D", "--debug"): debug = int(arg)
        if opt in ("-n", "--twitter-name"): tf.twitter_name = str(arg)
        if opt in ("-i", "--twitter-id"): tf.twitter_id = int(arg)
        if opt in ("-a", "--auth-file"): tf.auth_file = str(arg)
        if opt in ("-p", "--get-profile"): get_profile = True
        if opt in ("-f", "--get-followers"): get_followers = True
    try:
        try:
            if get_profile:
                tf.get_profile()
            elif get_followers:
                tf.get_followers()
            else:
                usage()
                sys.exit(-1)

            sys.exit(1)
        except Exception, e:
                print "misc. exception (runtime error from user callback?):", e
        except KeyboardInterrupt:
                sys.exit(1)


    except KeyboardInterrupt:
        # CTRL-C pretty handling.
        print "Keyboard Interruption!. Exiting."
        sys.exit(1)


if __name__ == '__main__':
    main()

