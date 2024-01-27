import webbrowser
import requests

import hashlib

import os
import time
import json

class lastfm:
    def __init__(self, key, secret):
        self.USER_AGENT = "luc"
        self.API_SECRET = secret
        self.API_KEY = key
        self.SESSION_KEY = ""

    def method_sig(self, par):
        keys_org = sorted(par)
        sig = ""
        for key in keys_org:
            if key != 'format':
                if isinstance(par[key], list):
                    for var in par[key]:
                        sig = sig + key + str(var)
                else:
                    sig = sig + key + par[key]
        sig = sig + self.API_SECRET
        sig_md5 = hashlib.md5(sig.encode('utf-8')).hexdigest()
        return sig_md5

    def api_get(self, load, needs_sig):
        head = {'user-agent': self.USER_AGENT}
        url = 'https://ws.audioscrobbler.com/2.0/'

        load['api_key'] = self.API_KEY
        load['format'] = 'json'

        if needs_sig:
            load['api_sig'] = self.method_sig(load)

        return requests.get(url, headers = head, params=load)

    def api_post(self, load):
        head = {'user-agent': self.USER_AGENT}
        url = 'https://ws.audioscrobbler.com/2.0/'

        load['api_key'] = self.API_KEY
        load['api_sig'] = self.method_sig(load)

        return requests.post(url, headers = head, params=load)

    def start_connection(self):
        token_apiresp = self.api_get({
            'method': "auth.getToken"
        }, True).json()
        token = token_apiresp['token']

        # get session key
        session_arr = {}
        if os.path.exists("session.json"):
            session_arr = json.loads(open("session.json", 'r').read())
        else:
            session_arr['key'] = ""
            session_arr['last_auth'] = 0
        if time.time() - 43200 > session_arr['last_auth']:
            webbrowser.open("http://www.last.fm/api/auth/?api_key={api}&token={token}".format(api = self.API_KEY, token = token), 2)
            session_save = open("session.json", "w")
            delay = input("Hit ENTER to continue.") #only used to delay the browser so we don't need the callback
            self.SESSION_KEY = self.api_get({ 
                'method': "auth.getSession",
                'token': token
            }, True).json()['session']['key']
            session_arr['last_auth'] = time.time()
            session_arr['key'] = self.SESSION_KEY
            json.dump(session_arr, session_save)
            session_save.close()
        else:
            self.SESSION_KEY = session_arr['key']

        return self.SESSION_KEY

    def scrobble(self, track, artist, timestamp):
        response = self.api_post({
            'sk': self.SESSION_KEY,
            'method': "track.scrobble",
            'artist': [artist],
            'track': [track],
            'timestamp': [timestamp]
        })
        # *should* fix on japanese artists
        with open("responses.txt", 'a', encoding="utf-8") as file:
            file.write("Response from scrobble \"" + artist + " - " + track + "\": " + response.text)

# scrobble
# print(json.dumps(api_post({ 
#     'sk': session_key,
#     'method': "track.scrobble",
#     'artist': ["test"],
#     'track': ["test"],
#     'timestamp': [str(int(time.time() - 30))]
# }).text))

