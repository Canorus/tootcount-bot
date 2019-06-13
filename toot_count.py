import requests
import json
import unicodedata
import re
import os

base = os.path.dirname(os.path.abspath(__file__))+'/'
with open(base+'acc.txt') as f:
    acc = f.read().strip()
headers = {'Authorization':'Bearer '+acc}
instance = 'https://botsin.space'

# functions
def followback(u):
    print('requesting followback')
    requests.post(instance+'/api/v1/accounts/'+str(u)+'/follow',headers=headers)

def send_rep(message, toot_id):
    d = dict()
    d['status'] = message
    d['visibility'] = 'unlisted'
    d['in_reply_to_id'] = toot_id
    r = requests.post(instance+'/api/v1/statuses',headers=headers,data=d)
    return r.content.decode('utf-8')

uri = instance+'/api/v1/streaming/user'
r_user = requests.get(uri,headers=headers,stream=True)
for l in r_user.iter_lines():
    rt = 0
    dec = l.decode('utf-8')
    print(dec)
    if dec == 'event: notification':
        mode = 0
    elif dec == 'event: update':
        mode = 1
    elif dec == ':thump':
        mode = 1
    if mode:
        print('.')# something on normal timeline
    else: # notification
        try:
            newdec = json.loads(re.sub('data: ','',dec))
            print(newdec)
            if newdec['type'] == 'mention':
                print('is mention')
                nu = newdec['account']['statuses_count']
                print('statuses_count: '+str(nu))
                toot_id = newdec['status']['id']
                print('toot_id: '+str(toot_id))
                reply_to_account = newdec['account']['acct']
                print('reply_to_account: '+reply_to_account)
                if newdec['account']['display_name']:
                    username = newdec['account']['display_name']
                else:
                    username = newdec['account']['username']
                message = '@'+reply_to_account+' '+username+'님의 툿 수는 '+str(nu)+' 개 입니다.'
                send_rep(message,toot_id)
            elif newdec['type'] == 'follow':
                print('followed') # followback
                followback(newdec['account']['id'])
        except:
            print('error occured')
            pass
