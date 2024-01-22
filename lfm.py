import webbrowser
import requests

import hashlib

import os
import time
import json

class lastfm:
    def __init__(self):
        self.USER_AGENT = "luc"
        self.API_SECRET = None
        self.API_KEY = None
        self.SESSION_KEY = None

    def method_sig(self, par):
        keys_org = sorted(par)
        sig = ""
        print("test api_secret start:"+ self.API_SECRET)
        print("test api_key start:"+ self.API_KEY)
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

    def start_connection(self, key, secret):
        API_SECRET = secret
        API_KEY = key

        print("test api_secret start:"+API_SECRET)
        print("test api_key start:"+API_KEY)
        token_apiresp = self.api_get({
            'method': "auth.getToken"
        }, True).json()
        token = token_apiresp['token']

        # get session key
        session_key = ""
        if not os.path.exists("session.txt"):
            webbrowser.open("http://www.last.fm/api/auth/?api_key={api}&token={token}".format(api = API_KEY, token = token), 2)
            session_save = open("session.txt", "w")
            delay = input("Hit ENTER to continue.") #only used to delay the browser so we don't need the callback
            session_key = self.api_get({ 
                'method': "auth.getSession",
                'token': token
            }, True).json()['session']['key']
            print(session_key)
            session_save.write(session_key)
            session_save.close()
        else:
            session_save = open("session.txt", "r")
            session_key = session_save.read()

        return session_key

    def scrobble(self, track, artist, timestamp):
        response = self.api_post({
            'sk': self.SESSION_KEY,
            'method': "track.scrobble",
            'artist': [artist],
            'track': [track],
            'timestamp': [timestamp]
        })
        print("Response from scrobble \"" + artist + " - " + track + "\": " + response.text)

# scrobble
# print(json.dumps(api_post({ 
#     'sk': session_key,
#     'method': "track.scrobble",
#     'artist': ["test"],
#     'track': ["test"],
#     'timestamp': [str(int(time.time() - 30))]
# }).text))

