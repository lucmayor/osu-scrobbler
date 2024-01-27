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

import datetime

async def get_scores():
    new_scores = oss.user_scores(user.id, include_fails=True, type="recent")
    stats = {'last_scrobbled':0};
    if len(new_scores) == 0:
        log_file = open("log.txt", "a")
        print("Run error: See log file for errors. Continuing program...")
        log_file.write("ERROR (" + str(datetime.datetime.now()) + "): User \"" + user_player + "\" has no plays listed.\n")
        log_file.close()
        return
    for s in new_scores:
        stats["last_scrobbled"] = int(time.time())
        if not os.path.exists("last_read.json"):
            scrobble(s)
        else:
            with open('last_read.json', 'r') as file:
                f = json.loads(file.read())
                if s.created_at.timestamp() > f["last_scrobbled"]:
                    scrobble(s)
    with open("last_read.json", 'w') as f:
        json.dump(stats, f)

def scrobble(score):
    decon_score = [score.beatmapset.artist_unicode, score.beatmapset.title_unicode, score.created_at]
    score_hits = int(score.statistics.count_50) + int(score.statistics.count_100) + int(score.statistics.count_300) + (score.statistics.count_miss)
    map = score.beatmap
    total_hits = map.count_circles + map.count_sliders + map.count_spinners
    if (score_hits / total_hits) > .5:
        print("scrobbled " + decon_score[1] + " " + decon_score[0] + " at " + str(decon_score[2]))
        client.scrobble(track=decon_score[1], artist=decon_score[0], timestamp=decon_score[2].timestamp())
    else:
        print("did not scrobble \"" + decon_score[0] + " - " + decon_score[1] + "\" at " + str(decon_score[2]) + ": did not hit 50% of hits")

async def main():
    score_collect = asyncio.create_task(get_scores())
    await score_collect
    print("test iteration operated at " + str(datetime.datetime.now()))
    await asyncio.sleep(30) # optimal method is to either check for window name updates or using the msn live signal but i am too stupid, we use a sleep method                           

async def main_loop():
    while True:
        await main()

client = lfm(lastfm_key, lastfm_secret)
lastfm_session = client.start_connection()
user_player = input("Please input a username to track: ")
user = oss.user(user_player, key=UserLookupKey.USERNAME)
loop = asyncio.get_event_loop()
loop.run_until_complete(main_loop())

# needed: time, date, artist unicode, song unicode
# time+date: created_at (datetime format)
# artist: score.beatmapset.artist_unicode
# song: score.beatmapset.title_unicode

# methodology for score check
# use scrobble(), also grab beatmap object -> count_circles, count_spinners, count_sliders
# also add statistics -> add all values within such
# if > 50%, scrobble