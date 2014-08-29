Twitter-stats
=============

This is a simple program to get information about any twitter account in your command line. 

Features so far
---------------
- Obtain the names of the followers of a given twitter account name.
- Works with Twitter API v1.1 (so far August 2014)


Usage
-----
To use this program you MUST have your twitter credentials and put them in a file.

Instructions are here also: https://dev.twitter.com/docs/auth/tokens-devtwittercom

1- Login to twitter.com

2- Go to https://dev.twitter.com/

3- Go to my applications

4- Create a new app

5- Generate the api keys

6- What is called "API key" should be put in a file as oauth.consumerKey

7- What is called "API key secret" should be put in a file as oauth.consumerKeySecret

8- The acccess token in the web page goes into oauth.accessToken

9- The acccess token secret in the web page goes into oauth.accessTokenSecret


You have an empty file called credentials.txt as an example to fill. Once you put the 4 values, you can run the program like this:

To get the followers of the user "test1234"

./twitter-stats.py -n test1234 -f -a credentials.txt


You can store the output in an external file every day and then compare them with diff.
