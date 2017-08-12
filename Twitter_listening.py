from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import MySQLdb
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect("localhost","pandey","  ","lol")

c = conn.cursor()

conn.set_character_set('utf8')

ckey="9VDSBBDXsXYRHlloCdrH6612O"
csecret="dmvLXOiv2Te4uMtu6x853MsQdd0dob9Kgw70wPShWy5iLMhw6U"
atoken="535319025-D3cirQ2QC5W5Epe7m5G1G5MVRDB8Cq4V7clofALs"
asecret="fXKoBQo8xJg1aSpQZ40dkT1VPQdDF6UlkmA9ARs3QIcQr"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

	try:
		tweet = all_data["text"]
		username = all_data["user"]["screen_name"]

		c.execute("INSERT INTO datas (time, username, tweet) VALUES (%s,%s,%s)",
		    (time.time(), username, tweet))

		conn.commit()

		print((username,tweet))

		return True

	except KeyError:
	    return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["modi"])
