import asyncio
from ossapi import Ossapi, Scope, UserLookupKey, GameMode, RankingType, OssapiAsync, Score

#testing making sure im on the right repo

client_id = 22219
client_secret = "socY7zpCMAXyCGi9TFP3In8mt0gPBD5N7Nc96LIl"
oss = Ossapi(client_id, client_secret)

user = oss.user("alkalde", key=UserLookupKey.USERNAME)
scores = oss.user_scores(user.id, include_fails=True, type="recent")
print(scores)
# needed: time, date, artist unicode, song unicode
# time+date: created_at (datetime format)
# artist: score.beatmapset.artist_unicode
# song: score.beatmapset.title_unicode
