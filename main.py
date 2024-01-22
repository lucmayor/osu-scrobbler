import asyncio, json, os, time
from ossapi import Ossapi, Scope, UserLookupKey, OssapiAsync, Score, Statistics, Beatmap
from lfm import lastfm as lfm

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

async def get_scores():
    new_scores = await oss.user_scores(user.id, include_fails=True, type="recent")
    for s in new_scores: # change this to check timestamp of recent scores, store "last scrobbled" based on unix time
        stats = {}
        stats["last_scrobbled"] = int(time.time())
        if not os.path.exists("last_read.json"):
            scrobble(s)
        else:
            with json.loads(open('last_read.json', 'r').read()) as file:
                if s.created_at.timestamp() > file.last_scrobbled:
                    scrobble(s)
        with open("last_read.json", 'w') as f:
            json.dump(stats, f)

def scrobble(score):
    decon_score = [score.beatmapset.artist_unicode, score.beatmapset.title_unicode, score.created_at]
    score_hits = int(score.count_50) + int(score.count_100) + int(score.count_300) + (score.count_miss)
    with score.beatmap as map:
        total_hits = map.count_circles + map.count_sliders + map.count_spinners
        if (score_hits / total_hits) > .5:
            lfm.scrobble(decon_score[1], decon_score[0], decon_score[2].timestamp())
        else:
            print("did not scrobble \"" + decon_score[0] + " - " + decon_score[1] + "\" at " + decon_score[2] + ": did not hit 50% of hits")

async def main():
    get_scores = asyncio.create_task(get_scores())
    await get_scores
    await asyncio.sleep(30) # optimal method is to either check for window name updates or using the msn live signal but i am too stupid, we use a sleep method                           
    main()

client = lfm()
lastfm_session = client.start_connection(lastfm_key, lastfm_secret)
user_player = input("Please input a username to track: ")
user = oss.user(user_player, key=UserLookupKey.USERNAME)
asyncio.run(main())

# needed: time, date, artist unicode, song unicode
# time+date: created_at (datetime format)
# artist: score.beatmapset.artist_unicode
# song: score.beatmapset.title_unicode

# methodology for score check
# use scrobble(), also grab beatmap object -> count_circles, count_spinners, count_sliders
# also add statistics -> add all values within such
# if > 50%, scrobble