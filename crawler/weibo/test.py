# https://pypi.org/project/weibo-scraper/
from weibopy import *
from weibo import Client

client_id= 1343270124,
client_secret="10476d48889135afbc4a5c85901c1ca8"
redirect_url="http://12450.xyz/callback"
client = WeiboOauth2(client_id,client_secret,redirect_url)

authorize_url = client.authorize_url
print(authorize_url)