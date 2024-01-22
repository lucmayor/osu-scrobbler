import asyncio, json
from ossapi import Ossapi, Scope, UserLookupKey, GameMode, RankingType, OssapiAsync, Score

lastfm_key = None
lastfm_secret = None
lastfm_session = None

client_id = None
client_secret = None

with open('secret.json', 'r') as secret:
    secrets = json.loads(secret.read())
    client_id = secrets["clientid-osu"]
    client_secret = secrets["secret-osu"]
    lastfm_key = secrets["api-lfm"]
    lastfm_secret = secrets["secret-lfm"]

oss = Ossapi(client_id, client_secret)
last_scrobbled = 0

user = oss.user("mrekk", key=UserLookupKey.USERNAME) # replace is user inpot later
scrobbled_scores = []

async def get_scores():
    new_scores = await oss.user_scores(user.id, include_fails=True, type="recent")
    for s in new_scores: # change this to check timestamp of recent scores, store "last scrobbled" based on unix time
        if s not in scrobbled_scores:
            scrobble(s)

def scrobble(score):
    decon_score = [score.beatmapset.artist_unicode, score.beatmapset.title_unicode, score.created_at]
    #lfm api
    scrobbled_scores.append(decon_score)

async def main():
    get_scores = asyncio.create_task(get_scores())
    await get_scores
    await asyncio.sleep(30) # optimal method is to either check for window name updates or using the msn live signal but i am too stupid, we use a sleep method                           
    main()

# whatever code is needed to store current scores, pretend this works for now
asyncio.run(main())

# needed: time, date, artist unicode, song unicode
# time+date: created_at (datetime format)
# artist: score.beatmapset.artist_unicode
# song: score.beatmapset.title_unicode

# methodology for score check
# use scrobble(), also grab beatmap object -> count_circles, count_spinners, count_sliders
# also add statistics -> add all values within such
# if > 50%, scrobble