import asyncio, json
from ossapi import Ossapi, Scope, UserLookupKey, GameMode, RankingType, OssapiAsync, Score

client_id = None
client_secret = None
oss = Ossapi(client_id, client_secret)

with open('secret.json', 'r') as secret:
    secrets = json.loads(secret)
    client_id = secrets["clientid-osu"]
    client_secret = secrets["secret-osu"]

user = oss.user("alkalde", key=UserLookupKey.USERNAME)
scrobbled_scores = []

async def get_scores():
    new_scores = await oss.user_scores(user.id, include_fails=True, type="recent")
    for s in new_scores: #change this to check timestamp of recent scores, store "last scrobbled" based on unix time
        if s not in scrobbled_scores:
            scrobble(s)


def scrobble(score):
    decon_score = [score.beatmapset.artist_unicode, score.beatmapset.title_unicode, score.created_at]
    #lfm api
    scrobbled_scores.append(decon_score)

async def main():
    asyncio.run(get_scores())
    await asyncio.wait(5) # replace for window check
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