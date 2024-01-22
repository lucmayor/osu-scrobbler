import webbrowser
import requests

import hashlib

import os
import time
import json

USER_AGENT = "luc"
SECRET = None
API_KEY = None
SESSION_KEY = None

def method_sig(par):
    keys_org = sorted(par)
    sig = ""
    for key in keys_org:
        if key != 'format':
            if isinstance(par[key], list):
                for var in par[key]:
                    sig = sig + key + str(var)
            else:
                sig = sig + key + par[key]
    sig = sig + SECRET
    sig_md5 = hashlib.md5(sig.encode('utf-8')).hexdigest()
    return sig_md5

def api_get(load, needs_sig):
    head = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    load['api_key'] = API_KEY
    load['format'] = 'json'

    if needs_sig:
        load['api_sig'] = method_sig(load)

    return requests.get(url, headers = head, params=load)

def api_post(load):
    head = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    load['api_key'] = API_KEY
    load['api_sig'] = method_sig(load)

    return requests.post(url, headers = head, params=load)

def start_connection(key, secret):
    SECRET = secret
    API_KEY = key
    token_apiresp = api_get({
        'method': "auth.getToken"
    }, True).json()
    token = token_apiresp['token']

    # get session key
    session_key = ""
    if not os.path.exists("session.txt"):
        webbrowser.open("http://www.last.fm/api/auth/?api_key={api}&token={token}".format(api = API_KEY, token = token), 2)
        session_save = open("session.txt", "w")
        delay = input("Hit ENTER to continue.") #only used to delay the browser so we don't need the callback
        session_key = api_get({ 
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

def scrobble(track, artist, timestamp):
    api_post({
        'sk': SESSION_KEY,
        'method': "track.scrobble",
        'artist': [artist],
        'track': [track],
        'timestamp': [timestamp]
    })


# scrobble
# print(json.dumps(api_post({ 
#     'sk': session_key,
#     'method': "track.scrobble",
#     'artist': ["test"],
#     'track': ["test"],
#     'timestamp': [str(int(time.time() - 30))]
# }).text))

